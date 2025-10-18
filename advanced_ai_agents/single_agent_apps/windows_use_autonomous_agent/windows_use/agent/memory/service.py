"""
Agent Memory Service - Natural Language Memory & Task Templates
Remembers conversations, saves workflows, and provides context
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class AgentMemory:
    """Manages agent memory, history, and task templates"""
    
    def __init__(self, memory_dir: str = None):
        """Initialize memory system"""
        if memory_dir is None:
            # Default to user's Documents folder
            memory_dir = os.path.join(
                os.path.expanduser("~"),
                "Documents",
                "PowerAgent",
                "Memory"
            )
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Memory files
        self.history_file = self.memory_dir / "command_history.json"
        self.templates_file = self.memory_dir / "task_templates.json"
        self.context_file = self.memory_dir / "context.json"
        
        # Load existing memory
        self.command_history: List[Dict] = self._load_json(self.history_file, [])
        self.task_templates: Dict = self._load_json(self.templates_file, {})
        self.context: Dict = self._load_json(self.context_file, {})
        
    def _load_json(self, file_path: Path, default: Any) -> Any:
        """Load JSON file or return default"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️ Could not load {file_path.name}: {e}")
        return default
    
    def _save_json(self, file_path: Path, data: Any):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save {file_path.name}: {e}")
    
    def add_command(self, command: str, result: str, tools_used: List[str] = None):
        """Add command to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "result": result,
            "tools_used": tools_used or [],
            "success": "error" not in result.lower() and "failed" not in result.lower()
        }
        
        self.command_history.append(entry)
        
        # Keep only last 100 commands to prevent file bloat
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
        
        self._save_json(self.history_file, self.command_history)
    
    def get_recent_commands(self, n: int = 5) -> List[Dict]:
        """Get N most recent commands"""
        return self.command_history[-n:] if self.command_history else []
    
    def search_history(self, query: str, n: int = 5) -> List[Dict]:
        """Search command history for matching entries"""
        query_lower = query.lower()
        matches = [
            entry for entry in self.command_history
            if query_lower in entry["command"].lower() 
            or query_lower in entry["result"].lower()
        ]
        return matches[-n:] if matches else []
    
    def save_template(self, name: str, command: str, description: str = ""):
        """Save a task template for reuse"""
        self.task_templates[name] = {
            "command": command,
            "description": description,
            "created": datetime.now().isoformat(),
            "usage_count": 0
        }
        self._save_json(self.templates_file, self.task_templates)
        return f"✅ Template '{name}' saved successfully!"
    
    def get_template(self, name: str) -> Optional[str]:
        """Get a saved task template"""
        if name in self.task_templates:
            template = self.task_templates[name]
            template["usage_count"] += 1
            template["last_used"] = datetime.now().isoformat()
            self._save_json(self.templates_file, self.task_templates)
            return template["command"]
        return None
    
    def list_templates(self) -> List[Dict]:
        """List all saved templates"""
        return [
            {
                "name": name,
                "description": data["description"],
                "command": data["command"],
                "usage_count": data.get("usage_count", 0)
            }
            for name, data in self.task_templates.items()
        ]
    
    def delete_template(self, name: str) -> str:
        """Delete a task template"""
        if name in self.task_templates:
            del self.task_templates[name]
            self._save_json(self.templates_file, self.task_templates)
            return f"✅ Template '{name}' deleted"
        return f"❌ Template '{name}' not found"
    
    def set_context(self, key: str, value: Any):
        """Save context information"""
        self.context[key] = {
            "value": value,
            "updated": datetime.now().isoformat()
        }
        self._save_json(self.context_file, self.context)
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context information"""
        if key in self.context:
            return self.context[key]["value"]
        return default
    
    def get_last_command(self) -> Optional[Dict]:
        """Get the most recent command"""
        return self.command_history[-1] if self.command_history else None
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        total_commands = len(self.command_history)
        successful = sum(1 for entry in self.command_history if entry["success"])
        failed = total_commands - successful
        
        # Most used tools
        tool_usage = {}
        for entry in self.command_history:
            for tool in entry.get("tools_used", []):
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        most_used_tools = sorted(
            tool_usage.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        return {
            "total_commands": total_commands,
            "successful": successful,
            "failed": failed,
            "success_rate": f"{(successful/total_commands*100):.1f}%" if total_commands > 0 else "0%",
            "templates_saved": len(self.task_templates),
            "most_used_tools": most_used_tools
        }
    
    def clear_history(self):
        """Clear command history"""
        self.command_history = []
        self._save_json(self.history_file, self.command_history)
        return "✅ Command history cleared"
    
    def export_history(self, output_path: str = None) -> str:
        """Export command history to file"""
        if output_path is None:
            output_path = self.memory_dir / f"history_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.command_history, f, indent=2, ensure_ascii=False)
            return f"✅ History exported to: {output_path}"
        except Exception as e:
            return f"❌ Export failed: {e}"
