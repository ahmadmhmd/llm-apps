"""
🚀 PHASE 5: AUTONOMOUS WORKFLOW ENGINE
Smart workflow detection, execution, and optimization
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
import threading
import time

class SmartWorkflowEngine:
    """
    Autonomous workflow engine that can:
    - Auto-detect user intent
    - Execute conditional workflows
    - Self-optimize based on success patterns
    - Record and replay workflows
    """
    
    def __init__(self, memory_path: Optional[str] = None):
        if memory_path is None:
            memory_path = os.path.join(
                os.path.expanduser("~"), 
                "Documents", 
                "PowerAgent", 
                "Workflows"
            )
        
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.workflows_file = self.memory_path / "workflows.json"
        self.patterns_file = self.memory_path / "patterns.json"
        self.performance_file = self.memory_path / "performance.json"
        
        self.workflows = self._load_workflows()
        self.patterns = self._load_patterns()
        self.performance_data = self._load_performance()
        
        # Event listeners for triggers
        self.event_listeners = {}
        self.is_recording = False
        self.current_recording = []
    
    def _load_workflows(self) -> Dict:
        """Load saved workflows"""
        if self.workflows_file.exists():
            with open(self.workflows_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_workflows(self):
        """Save workflows to disk"""
        with open(self.workflows_file, 'w') as f:
            json.dump(self.workflows, f, indent=2)
    
    def _load_patterns(self) -> Dict:
        """Load learned patterns"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r') as f:
                return json.load(f)
        return {
            "intent_patterns": {},
            "sequence_patterns": {},
            "success_patterns": {}
        }
    
    def _save_patterns(self):
        """Save learned patterns"""
        with open(self.patterns_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def _load_performance(self) -> Dict:
        """Load performance metrics"""
        if self.performance_file.exists():
            with open(self.performance_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_performance(self):
        """Save performance metrics"""
        with open(self.performance_file, 'w') as f:
            json.dump(self.performance_data, f, indent=2)
    
    def auto_detect_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Automatically detect user intent and suggest workflow
        
        Examples:
        - "Prepare my report" → [research, analyze, format, share]
        - "Backup my files" → [check space, compress, copy, verify]
        - "Morning routine" → [check weather, open apps, read calendar]
        """
        
        user_input_lower = user_input.lower()
        
        # Built-in intent patterns
        intent_map = {
            "report": {
                "intent": "create_report",
                "steps": ["gather_data", "analyze", "format", "export"],
                "confidence": 0.8
            },
            "backup": {
                "intent": "backup_files",
                "steps": ["check_storage", "select_files", "compress", "copy", "verify"],
                "confidence": 0.9
            },
            "morning": {
                "intent": "morning_routine",
                "steps": ["check_weather", "open_apps", "read_calendar", "check_emails"],
                "confidence": 0.85
            },
            "presentation": {
                "intent": "prepare_presentation",
                "steps": ["gather_content", "create_slides", "add_visuals", "practice"],
                "confidence": 0.8
            },
            "email": {
                "intent": "manage_email",
                "steps": ["open_email", "read_unread", "respond_priority", "archive"],
                "confidence": 0.9
            },
            "research": {
                "intent": "conduct_research",
                "steps": ["search_topic", "collect_sources", "summarize", "save_notes"],
                "confidence": 0.85
            },
            "meeting": {
                "intent": "prepare_meeting",
                "steps": ["check_calendar", "gather_documents", "create_agenda", "send_invites"],
                "confidence": 0.8
            }
        }
        
        # Check learned patterns first
        for pattern_name, pattern_data in self.patterns["intent_patterns"].items():
            if any(keyword in user_input_lower for keyword in pattern_data["keywords"]):
                return {
                    "intent": pattern_name,
                    "steps": pattern_data["steps"],
                    "confidence": pattern_data["success_rate"],
                    "source": "learned"
                }
        
        # Check built-in patterns
        for keyword, intent_data in intent_map.items():
            if keyword in user_input_lower:
                return {
                    **intent_data,
                    "source": "builtin"
                }
        
        # No pattern matched
        return {
            "intent": "unknown",
            "steps": [],
            "confidence": 0.0,
            "source": "none",
            "suggestion": "Try: 'record workflow' to teach me this task"
        }
    
    def create_workflow(self, name: str, steps: List[Dict[str, Any]], 
                       conditions: Optional[List[Dict]] = None,
                       description: str = "") -> Dict:
        """
        Create a new workflow
        
        Args:
            name: Workflow name
            steps: List of steps [{"action": "screenshot", "params": {...}}]
            conditions: Optional conditions [{"if": "battery < 20", "then": "skip"}]
            description: Workflow description
        """
        
        workflow = {
            "name": name,
            "description": description,
            "steps": steps,
            "conditions": conditions or [],
            "created_at": datetime.now().isoformat(),
            "execution_count": 0,
            "success_count": 0,
            "average_duration": 0
        }
        
        self.workflows[name] = workflow
        self._save_workflows()
        
        return {
            "status": "success",
            "message": f"Workflow '{name}' created with {len(steps)} steps",
            "workflow": workflow
        }
    
    def execute_workflow(self, name: str, agent: Any, 
                        variables: Optional[Dict] = None) -> Dict:
        """
        Execute a saved workflow
        
        Args:
            name: Workflow name
            agent: Agent instance to execute actions
            variables: Variables to substitute in workflow
        """
        
        if name not in self.workflows:
            return {
                "status": "error",
                "message": f"Workflow '{name}' not found",
                "available_workflows": list(self.workflows.keys())
            }
        
        workflow = self.workflows[name]
        start_time = time.time()
        results = []
        success = True
        
        try:
            for i, step in enumerate(workflow["steps"]):
                # Check conditions before each step
                if not self._check_conditions(workflow.get("conditions", []), step):
                    results.append({
                        "step": i + 1,
                        "status": "skipped",
                        "reason": "condition_not_met"
                    })
                    continue
                
                # Substitute variables
                params = self._substitute_variables(step.get("params", {}), variables or {})
                
                # Execute step
                try:
                    # This would call the actual agent tools
                    result = self._execute_step(agent, step["action"], params)
                    results.append({
                        "step": i + 1,
                        "action": step["action"],
                        "status": "success",
                        "result": result
                    })
                except Exception as e:
                    results.append({
                        "step": i + 1,
                        "action": step["action"],
                        "status": "error",
                        "error": str(e)
                    })
                    
                    # Attempt error recovery
                    recovery_result = self._attempt_recovery(agent, step, e)
                    if recovery_result["recovered"]:
                        results[-1]["recovery"] = recovery_result
                    else:
                        success = False
                        break
            
            duration = time.time() - start_time
            
            # Update workflow statistics
            workflow["execution_count"] += 1
            if success:
                workflow["success_count"] += 1
            
            # Update average duration
            old_avg = workflow["average_duration"]
            workflow["average_duration"] = (
                (old_avg * (workflow["execution_count"] - 1) + duration) / 
                workflow["execution_count"]
            )
            
            self._save_workflows()
            
            # Learn from execution
            self._learn_from_execution(name, success, duration)
            
            return {
                "status": "success" if success else "partial",
                "workflow": name,
                "steps_completed": sum(1 for r in results if r["status"] == "success"),
                "total_steps": len(workflow["steps"]),
                "duration": duration,
                "results": results
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "results": results
            }
    
    def _check_conditions(self, conditions: List[Dict], step: Dict) -> bool:
        """Check if conditions are met for step execution"""
        if not conditions:
            return True
        
        # Simple condition evaluation
        for condition in conditions:
            if "if" in condition:
                # Parse condition (simplified)
                cond_str = condition["if"]
                
                # Example: "battery < 20"
                if "battery" in cond_str:
                    import psutil
                    battery = psutil.sensors_battery()
                    if battery:
                        battery_percent = battery.percent
                        if "<" in cond_str:
                            threshold = int(cond_str.split("<")[1].strip())
                            if battery_percent < threshold:
                                return False
                
                # Add more condition types as needed
        
        return True
    
    def _substitute_variables(self, params: Dict, variables: Dict) -> Dict:
        """Substitute variables in parameters"""
        result = {}
        for key, value in params.items():
            if isinstance(value, str) and value.startswith("$"):
                var_name = value[1:]
                result[key] = variables.get(var_name, value)
            else:
                result[key] = value
        return result
    
    def _execute_step(self, agent: Any, action: str, params: Dict) -> Any:
        """Execute a single workflow step"""
        # This would integrate with your actual agent
        # For now, placeholder
        return {"status": "executed", "action": action, "params": params}
    
    def _attempt_recovery(self, agent: Any, step: Dict, error: Exception) -> Dict:
        """Attempt to recover from step failure"""
        recovery_strategies = {
            "FileNotFoundError": ["check_alternate_path", "create_file"],
            "PermissionError": ["request_admin", "use_temp_folder"],
            "TimeoutError": ["retry_with_backoff", "skip_step"],
            "ConnectionError": ["check_internet", "use_cached_data"]
        }
        
        error_type = type(error).__name__
        strategies = recovery_strategies.get(error_type, ["retry_once"])
        
        for strategy in strategies:
            try:
                # Attempt recovery (simplified)
                if strategy == "retry_once":
                    time.sleep(1)
                    self._execute_step(agent, step["action"], step.get("params", {}))
                    return {"recovered": True, "strategy": strategy}
            except:
                continue
        
        return {"recovered": False, "attempted_strategies": strategies}
    
    def _learn_from_execution(self, workflow_name: str, success: bool, duration: float):
        """Learn patterns from workflow execution"""
        if workflow_name not in self.performance_data:
            self.performance_data[workflow_name] = {
                "executions": [],
                "success_rate": 0,
                "avg_duration": 0
            }
        
        perf = self.performance_data[workflow_name]
        perf["executions"].append({
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "duration": duration
        })
        
        # Keep only last 100 executions
        perf["executions"] = perf["executions"][-100:]
        
        # Update success rate
        successes = sum(1 for e in perf["executions"] if e["success"])
        perf["success_rate"] = successes / len(perf["executions"])
        
        # Update avg duration
        perf["avg_duration"] = sum(e["duration"] for e in perf["executions"]) / len(perf["executions"])
        
        self._save_performance()
    
    def start_recording(self) -> Dict:
        """Start recording a workflow"""
        self.is_recording = True
        self.current_recording = []
        return {
            "status": "recording",
            "message": "Workflow recording started. Perform your actions..."
        }
    
    def record_action(self, action: str, params: Dict):
        """Record an action during workflow recording"""
        if self.is_recording:
            self.current_recording.append({
                "action": action,
                "params": params,
                "timestamp": datetime.now().isoformat()
            })
    
    def stop_recording(self, workflow_name: str, description: str = "") -> Dict:
        """Stop recording and save workflow"""
        if not self.is_recording:
            return {
                "status": "error",
                "message": "No recording in progress"
            }
        
        self.is_recording = False
        
        if not self.current_recording:
            return {
                "status": "error",
                "message": "No actions recorded"
            }
        
        # Create workflow from recording
        result = self.create_workflow(
            name=workflow_name,
            steps=self.current_recording,
            description=description
        )
        
        self.current_recording = []
        
        return result
    
    def add_trigger(self, trigger_type: str, condition: Dict, 
                   workflow_name: str) -> Dict:
        """
        Add event-driven trigger for workflow
        
        Trigger types:
        - "file_change": Watch for file modifications
        - "time": Schedule based on time
        - "system_event": Battery, network, etc.
        """
        
        trigger_id = f"{trigger_type}_{workflow_name}_{datetime.now().timestamp()}"
        
        trigger = {
            "id": trigger_id,
            "type": trigger_type,
            "condition": condition,
            "workflow": workflow_name,
            "enabled": True,
            "created_at": datetime.now().isoformat()
        }
        
        if trigger_type not in self.event_listeners:
            self.event_listeners[trigger_type] = []
        
        self.event_listeners[trigger_type].append(trigger)
        
        # Start listening thread for this trigger type
        if trigger_type == "time":
            self._start_time_trigger(trigger)
        elif trigger_type == "file_change":
            self._start_file_watcher(trigger)
        
        return {
            "status": "success",
            "message": f"Trigger {trigger_id} added",
            "trigger": trigger
        }
    
    def _start_time_trigger(self, trigger: Dict):
        """Start time-based trigger"""
        def check_time():
            while trigger["enabled"]:
                # Check if time condition met
                # Execute workflow if yes
                time.sleep(60)  # Check every minute
        
        thread = threading.Thread(target=check_time, daemon=True)
        thread.start()
    
    def _start_file_watcher(self, trigger: Dict):
        """Start file change watcher"""
        # Use watchdog library or polling
        pass
    
    def get_workflow_stats(self) -> Dict:
        """Get statistics about workflows"""
        total_workflows = len(self.workflows)
        total_executions = sum(w["execution_count"] for w in self.workflows.values())
        total_successes = sum(w["success_count"] for w in self.workflows.values())
        
        success_rate = (total_successes / total_executions * 100) if total_executions > 0 else 0
        
        # Most used workflows
        most_used = sorted(
            self.workflows.items(),
            key=lambda x: x[1]["execution_count"],
            reverse=True
        )[:5]
        
        return {
            "total_workflows": total_workflows,
            "total_executions": total_executions,
            "total_successes": total_successes,
            "success_rate": f"{success_rate:.1f}%",
            "most_used_workflows": [
                {
                    "name": name,
                    "executions": data["execution_count"],
                    "success_rate": f"{(data['success_count'] / data['execution_count'] * 100):.1f}%" if data["execution_count"] > 0 else "N/A"
                }
                for name, data in most_used
            ]
        }
    
    def optimize_workflow(self, workflow_name: str) -> Dict:
        """
        Self-optimize workflow based on performance data
        """
        if workflow_name not in self.workflows:
            return {"status": "error", "message": "Workflow not found"}
        
        if workflow_name not in self.performance_data:
            return {"status": "error", "message": "No performance data available"}
        
        workflow = self.workflows[workflow_name]
        perf = self.performance_data[workflow_name]
        
        optimizations = []
        
        # Analyze failed steps
        failed_steps = []
        for execution in perf["executions"]:
            if not execution.get("success"):
                failed_steps.append(execution)
        
        if failed_steps:
            optimizations.append({
                "type": "error_handling",
                "recommendation": "Add retry logic for frequently failing steps"
            })
        
        # Analyze duration
        if perf["avg_duration"] > 30:  # Longer than 30 seconds
            optimizations.append({
                "type": "performance",
                "recommendation": "Consider parallelizing independent steps"
            })
        
        # Suggest workflow improvements
        return {
            "status": "success",
            "workflow": workflow_name,
            "current_performance": {
                "success_rate": f"{perf['success_rate'] * 100:.1f}%",
                "avg_duration": f"{perf['avg_duration']:.2f}s"
            },
            "optimizations": optimizations
        }
