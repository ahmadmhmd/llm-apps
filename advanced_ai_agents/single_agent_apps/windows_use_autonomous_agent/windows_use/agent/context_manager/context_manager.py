"""
🧠 PHASE 6: CONTEXT-AWARE INTELLIGENCE
Track context, learn user habits, optimize based on system state
"""

import json
import os
import psutil
import win32gui
import win32process
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
from collections import defaultdict, Counter
import threading
import time

class ContextManager:
    """
    Context-aware intelligence system that:
    - Tracks current app and recent actions
    - Learns user habits and patterns
    - Monitors system state
    - Provides smart suggestions
    """
    
    def __init__(self, memory_path: Optional[str] = None):
        if memory_path is None:
            memory_path = os.path.join(
                os.path.expanduser("~"),
                "Documents",
                "PowerAgent",
                "Context"
            )
        
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.context_file = self.memory_path / "context.json"
        self.habits_file = self.memory_path / "habits.json"
        self.app_history_file = self.memory_path / "app_history.json"
        
        # Current context
        self.context = {
            "current_app": None,
            "previous_app": None,
            "recent_actions": [],
            "active_files": [],
            "clipboard_history": [],
            "system_state": {},
            "session_start": datetime.now().isoformat(),
            "focus_duration": {}
        }
        
        # User habits
        self.habits = self._load_habits()
        
        # App usage tracking
        self.app_history = self._load_app_history()
        
        # Start background monitoring
        self.monitoring = True
        self._start_monitoring()
    
    def _load_habits(self) -> Dict:
        """Load learned user habits"""
        if self.habits_file.exists():
            with open(self.habits_file, 'r') as f:
                return json.load(f)
        return {
            "daily_patterns": {},
            "weekly_patterns": {},
            "app_sequences": {},
            "preferred_times": {},
            "typical_durations": {}
        }
    
    def _save_habits(self):
        """Save user habits"""
        with open(self.habits_file, 'w') as f:
            json.dump(self.habits, f, indent=2)
    
    def _load_app_history(self) -> List:
        """Load app usage history"""
        if self.app_history_file.exists():
            with open(self.app_history_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_app_history(self):
        """Save app usage history"""
        # Keep only last 1000 entries
        if len(self.app_history) > 1000:
            self.app_history = self.app_history[-1000:]
        
        with open(self.app_history_file, 'w') as f:
            json.dump(self.app_history, f, indent=2)
    
    def _start_monitoring(self):
        """Start background monitoring threads"""
        
        # Monitor active window
        def monitor_active_window():
            while self.monitoring:
                try:
                    self._update_active_window()
                    time.sleep(2)  # Check every 2 seconds
                except:
                    pass
        
        # Monitor system state
        def monitor_system_state():
            while self.monitoring:
                try:
                    self._update_system_state()
                    time.sleep(30)  # Check every 30 seconds
                except:
                    pass
        
        # Start threads
        threading.Thread(target=monitor_active_window, daemon=True).start()
        threading.Thread(target=monitor_system_state, daemon=True).start()
    
    def _update_active_window(self):
        """Update current active window/app"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            process = psutil.Process(pid)
            app_name = process.name()
            window_title = win32gui.GetWindowText(hwnd)
            
            # Update context if app changed
            if app_name != self.context["current_app"]:
                self.context["previous_app"] = self.context["current_app"]
                self.context["current_app"] = app_name
                
                # Log app transition
                self._log_app_transition(app_name, window_title)
                
                # Update focus duration
                if self.context["previous_app"]:
                    app = self.context["previous_app"]
                    if app not in self.context["focus_duration"]:
                        self.context["focus_duration"][app] = 0
                    # Would track actual duration in real implementation
        
        except Exception as e:
            pass
    
    def _update_system_state(self):
        """Update system state information"""
        try:
            # Battery
            battery = psutil.sensors_battery()
            battery_info = {
                "percent": battery.percent if battery else 100,
                "plugged_in": battery.power_plugged if battery else True,
                "time_left": battery.secsleft if battery and battery.secsleft != -1 else None
            }
            
            # Memory
            memory = psutil.virtual_memory()
            memory_info = {
                "percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2)
            }
            
            # CPU
            cpu_info = {
                "percent": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count()
            }
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_info = {
                "percent": disk.percent,
                "free_gb": round(disk.free / (1024**3), 2)
            }
            
            # Network
            net_io = psutil.net_io_counters()
            network_info = {
                "connected": net_io.bytes_sent > 0 or net_io.bytes_recv > 0
            }
            
            self.context["system_state"] = {
                "battery": battery_info,
                "memory": memory_info,
                "cpu": cpu_info,
                "disk": disk_info,
                "network": network_info,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            pass
    
    def _log_app_transition(self, app_name: str, window_title: str):
        """Log app transition for pattern learning"""
        entry = {
            "app": app_name,
            "title": window_title,
            "timestamp": datetime.now().isoformat(),
            "day_of_week": datetime.now().strftime("%A"),
            "hour": datetime.now().hour
        }
        
        self.app_history.append(entry)
        self._save_app_history()
        
        # Learn patterns
        self._learn_app_patterns()
    
    def _learn_app_patterns(self):
        """Learn patterns from app usage"""
        if len(self.app_history) < 10:
            return
        
        # Analyze recent sequences (last 100 transitions)
        recent = self.app_history[-100:]
        
        # App sequences (what typically follows what)
        for i in range(len(recent) - 1):
            current = recent[i]["app"]
            next_app = recent[i + 1]["app"]
            
            if current not in self.habits["app_sequences"]:
                self.habits["app_sequences"][current] = Counter()
            
            self.habits["app_sequences"][current][next_app] += 1
        
        # Daily patterns (what apps used at what hour)
        for entry in recent:
            hour = entry["hour"]
            app = entry["app"]
            
            hour_key = f"hour_{hour}"
            if hour_key not in self.habits["daily_patterns"]:
                self.habits["daily_patterns"][hour_key] = Counter()
            
            self.habits["daily_patterns"][hour_key][app] += 1
        
        # Weekly patterns
        for entry in recent:
            day = entry["day_of_week"]
            app = entry["app"]
            
            if day not in self.habits["weekly_patterns"]:
                self.habits["weekly_patterns"][day] = Counter()
            
            self.habits["weekly_patterns"][day][app] += 1
        
        self._save_habits()
    
    def record_action(self, action: str, details: Dict):
        """Record a user action"""
        action_entry = {
            "action": action,
            "details": details,
            "app": self.context["current_app"],
            "timestamp": datetime.now().isoformat()
        }
        
        self.context["recent_actions"].append(action_entry)
        
        # Keep only last 50 actions
        self.context["recent_actions"] = self.context["recent_actions"][-50:]
    
    def get_context(self) -> Dict:
        """Get current context"""
        return self.context
    
    def get_smart_suggestions(self) -> List[Dict]:
        """
        Provide context-aware smart suggestions
        """
        suggestions = []
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime("%A")
        
        # Suggest based on time patterns
        hour_key = f"hour_{current_hour}"
        if hour_key in self.habits["daily_patterns"]:
            common_apps = self.habits["daily_patterns"][hour_key].most_common(3)
            if common_apps:
                suggestions.append({
                    "type": "time_pattern",
                    "message": f"You usually use these apps around this time:",
                    "apps": [app for app, _ in common_apps],
                    "confidence": 0.8
                })
        
        # Suggest based on app sequence
        current_app = self.context["current_app"]
        if current_app and current_app in self.habits["app_sequences"]:
            next_apps = self.habits["app_sequences"][current_app].most_common(2)
            if next_apps:
                suggestions.append({
                    "type": "sequence_pattern",
                    "message": f"After {current_app}, you typically switch to:",
                    "apps": [app for app, _ in next_apps],
                    "confidence": 0.75
                })
        
        # Suggest based on system state
        battery = self.context["system_state"].get("battery", {})
        if battery.get("percent", 100) < 20 and not battery.get("plugged_in", True):
            suggestions.append({
                "type": "system_warning",
                "message": "Low battery! Consider postponing heavy tasks.",
                "action": "avoid_heavy_operations",
                "confidence": 1.0
            })
        
        memory = self.context["system_state"].get("memory", {})
        if memory.get("percent", 0) > 80:
            suggestions.append({
                "type": "system_warning",
                "message": "High memory usage. Consider closing unused apps.",
                "action": "optimize_memory",
                "confidence": 0.9
            })
        
        # Suggest based on day of week
        if current_day in self.habits["weekly_patterns"]:
            common_tasks = self.habits["weekly_patterns"][current_day].most_common(2)
            if common_tasks:
                suggestions.append({
                    "type": "weekly_pattern",
                    "message": f"On {current_day}s, you typically work with:",
                    "apps": [app for app, _ in common_tasks],
                    "confidence": 0.7
                })
        
        return suggestions
    
    def should_proceed_with_task(self, task_type: str) -> Dict:
        """
        Determine if task should proceed based on context
        """
        system_state = self.context["system_state"]
        
        # Battery considerations
        battery = system_state.get("battery", {})
        if battery.get("percent", 100) < 20 and not battery.get("plugged_in", True):
            if task_type in ["video_processing", "large_file_operation", "backup"]:
                return {
                    "proceed": False,
                    "reason": "Low battery - task may drain power",
                    "suggestion": "Connect to power source or wait until charged"
                }
        
        # Memory considerations
        memory = system_state.get("memory", {})
        if memory.get("percent", 0) > 85:
            if task_type in ["open_multiple_apps", "large_file_operation"]:
                return {
                    "proceed": False,
                    "reason": "High memory usage - task may cause slowdown",
                    "suggestion": "Close unused applications first"
                }
        
        # Disk space considerations
        disk = system_state.get("disk", {})
        if disk.get("free_gb", 100) < 5:
            if task_type in ["download", "backup", "screenshot"]:
                return {
                    "proceed": False,
                    "reason": "Low disk space",
                    "suggestion": "Free up disk space before proceeding"
                }
        
        # Network considerations
        network = system_state.get("network", {})
        if not network.get("connected", True):
            if task_type in ["web_search", "download", "cloud_sync"]:
                return {
                    "proceed": False,
                    "reason": "No network connection",
                    "suggestion": "Connect to internet first"
                }
        
        return {
            "proceed": True,
            "reason": "All conditions favorable"
        }
    
    def get_habit_insights(self) -> Dict:
        """Get insights about user habits"""
        
        # Most used apps
        app_counts = Counter()
        for entry in self.app_history[-500:]:  # Last 500 transitions
            app_counts[entry["app"]] += 1
        
        most_used = app_counts.most_common(10)
        
        # Peak hours
        hour_counts = Counter()
        for entry in self.app_history[-500:]:
            hour_counts[entry["hour"]] += 1
        
        peak_hours = hour_counts.most_common(3)
        
        # Most productive days
        day_counts = Counter()
        for entry in self.app_history[-500:]:
            day_counts[entry["day_of_week"]] += 1
        
        productive_days = day_counts.most_common(3)
        
        return {
            "most_used_apps": [
                {"app": app, "usage_count": count}
                for app, count in most_used
            ],
            "peak_hours": [
                {"hour": f"{hour}:00", "activity_count": count}
                for hour, count in peak_hours
            ],
            "productive_days": [
                {"day": day, "activity_count": count}
                for day, count in productive_days
            ],
            "total_app_transitions": len(self.app_history),
            "session_duration": self._calculate_session_duration()
        }
    
    def _calculate_session_duration(self) -> str:
        """Calculate current session duration"""
        start = datetime.fromisoformat(self.context["session_start"])
        duration = datetime.now() - start
        
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        return f"{hours}h {minutes}m"
    
    def predict_next_action(self) -> Optional[Dict]:
        """Predict what user might do next"""
        current_app = self.context["current_app"]
        current_hour = datetime.now().hour
        
        predictions = []
        
        # Based on app sequence
        if current_app and current_app in self.habits["app_sequences"]:
            next_apps = self.habits["app_sequences"][current_app].most_common(1)
            if next_apps:
                predictions.append({
                    "type": "app_switch",
                    "prediction": f"Switch to {next_apps[0][0]}",
                    "confidence": 0.7,
                    "basis": "sequence_pattern"
                })
        
        # Based on time
        hour_key = f"hour_{current_hour}"
        if hour_key in self.habits["daily_patterns"]:
            common_apps = self.habits["daily_patterns"][hour_key].most_common(1)
            if common_apps:
                predictions.append({
                    "type": "time_based",
                    "prediction": f"You might want to open {common_apps[0][0]}",
                    "confidence": 0.6,
                    "basis": "time_pattern"
                })
        
        return predictions[0] if predictions else None
    
    def get_cross_app_context(self) -> Dict:
        """
        Track context across different applications
        """
        recent_apps = []
        if len(self.app_history) >= 5:
            recent_apps = [entry["app"] for entry in self.app_history[-5:]]
        
        # Detect workflow patterns
        workflow_detected = None
        if recent_apps:
            # Example: Word → Excel → PowerPoint = "presentation prep"
            if any("WORD" in app.upper() for app in recent_apps) and \
               any("EXCEL" in app.upper() for app in recent_apps):
                workflow_detected = {
                    "workflow": "document_preparation",
                    "apps_involved": recent_apps,
                    "suggestion": "Might need to create charts or reports"
                }
            
            # Email → Browser = "research and communicate"
            if any("OUTLOOK" in app.upper() or "MAIL" in app.upper() for app in recent_apps) and \
               any("CHROME" in app.upper() or "FIREFOX" in app.upper() for app in recent_apps):
                workflow_detected = {
                    "workflow": "research_and_email",
                    "apps_involved": recent_apps,
                    "suggestion": "Research tasks followed by communication"
                }
        
        return {
            "recent_app_sequence": recent_apps,
            "current_app": self.context["current_app"],
            "workflow_detected": workflow_detected,
            "session_context": {
                "duration": self._calculate_session_duration(),
                "actions_count": len(self.context["recent_actions"]),
                "app_switches": len(self.app_history)
            }
        }
    
    def get_temporal_awareness(self) -> Dict:
        """
        Provide temporal context and predictions
        """
        now = datetime.now()
        
        return {
            "current_time": {
                "hour": now.hour,
                "day": now.strftime("%A"),
                "date": now.strftime("%Y-%m-%d")
            },
            "typical_behavior": self._get_typical_behavior_for_time(now),
            "upcoming_patterns": self._predict_upcoming_patterns(now)
        }
    
    def _get_typical_behavior_for_time(self, time: datetime) -> Dict:
        """What does user typically do at this time?"""
        hour_key = f"hour_{time.hour}"
        day = time.strftime("%A")
        
        typical = {}
        
        if hour_key in self.habits["daily_patterns"]:
            apps = self.habits["daily_patterns"][hour_key].most_common(3)
            typical["apps"] = [app for app, _ in apps]
        
        if day in self.habits["weekly_patterns"]:
            tasks = self.habits["weekly_patterns"][day].most_common(3)
            typical["tasks"] = [task for task, _ in tasks]
        
        return typical
    
    def _predict_upcoming_patterns(self, time: datetime) -> List[Dict]:
        """Predict what user might do in next hour"""
        next_hour = (time + timedelta(hours=1)).hour
        hour_key = f"hour_{next_hour}"
        
        predictions = []
        
        if hour_key in self.habits["daily_patterns"]:
            apps = self.habits["daily_patterns"][hour_key].most_common(2)
            for app, count in apps:
                predictions.append({
                    "time": f"{next_hour}:00",
                    "likely_app": app,
                    "confidence": 0.6
                })
        
        return predictions
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
