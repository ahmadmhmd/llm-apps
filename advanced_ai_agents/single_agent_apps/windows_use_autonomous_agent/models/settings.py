"""User settings management."""

import json
from pathlib import Path
from typing import Dict, Any


class UserSettings:
    """Manages user settings and preferences."""

    def __init__(self, settings_path: Path):
        self.settings_path = settings_path
        self.settings: Dict[str, Any] = {}
        self.load()
        
    def load(self) -> Dict[str, Any]:
        """Load settings from file."""
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
            except Exception as e:
                print(f"Failed to load settings: {e}")
                self.settings = self._default_settings()
        else:
            self.settings = self._default_settings()
        return self.settings
    
    def save(self):
        """Save settings to file."""
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
    
    def update(self, data: Dict[str, Any]):
        """Update multiple settings."""
        self.settings.update(data)
    
    def _default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            "theme": "System",
            "language": "English",
            "notifications": "Toast",
            "microphone": "Default",
            "voice_feedback": True,
            "auto_run_on_enter": True,
            "context_tracking": True,
            "data_retention_days": 30,
            "google_api_key": "",
        }
