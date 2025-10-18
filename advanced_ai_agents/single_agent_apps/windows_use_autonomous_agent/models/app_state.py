"""Application state management."""

from typing import Dict, List, Optional, Any
import customtkinter as ctk


class AppState:
    """Manages the application's runtime state."""

    def __init__(self):
        # Current state
        self.current_mode: str = "Basic"
        self.current_view: str = "Command Console"
        self.is_listening: bool = False
        self.voice_enabled: bool = False
        self.agent_ready: bool = False
        self.agent_error: Optional[str] = None
        self.advanced_features: bool = False
        self.sidebar_collapsed: bool = False
        
        # Command history
        self.history: List[Dict[str, str]] = []
        
        # Workflow state
        self.selected_workflow: Optional[str] = None
        self.workflow_cards: Dict[str, ctk.CTkFrame] = {}
        
        # UI components tracking
        self.response_cards: List[ctk.CTkFrame] = []
        self.quick_buttons: List[ctk.CTkButton] = []
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        
        # Cache
        self.help_content_cache: Dict[str, str] = {}
        
        # Placeholder rotation
        self.placeholder_index: int = 0
        self.placeholder_job: Optional[str] = None
        
    def add_to_history(self, command: str, result: str, status: str = "success"):
        """Add a command to history."""
        self.history.append({
            "command": command,
            "result": result,
            "status": status,
            "timestamp": str(time.time())
        })
        
    def clear_history(self):
        """Clear command history."""
        self.history.clear()
        
    def get_recent_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent command history."""
        return self.history[-limit:] if self.history else []
