"""Main application controller - handles all business logic."""

import customtkinter as ctk
from typing import Dict, Callable, Optional
from datetime import datetime
from pathlib import Path
import speech_recognition as sr
from models import AppState, UserSettings, AgentManager
from config import MODE_COLORS


class AppController:
    """Central controller for the application."""
    
    def __init__(self):
        self.state = AppState()
        
        # Settings file path
        settings_dir = Path.home() / ".windows_use_agent"
        settings_dir.mkdir(exist_ok=True)
        settings_path = settings_dir / "settings.json"
        self.settings = UserSettings(settings_path)
        
        # Initialize Windows Use Agent
        print("🤖 Initializing Windows Use Agent...")
        self.agent_manager = AgentManager()
        
        # Voice recognition
        self.recognizer = sr.Recognizer()
        
        # View references (set by main window)
        self.console_view = None
        self.workflows_view = None
        self.main_window = None
        
        # Callbacks
        self.on_command_execute: Optional[Callable] = None
        self.on_view_change: Optional[Callable] = None
        
        # Print agent status
        if self.agent_manager.is_ready():
            print("✅ Agent ready!")
        else:
            print(f"❌ Agent initialization failed: {self.agent_manager.get_error()}")
    
    # ========== Console View Methods ==========
    
    def on_mode_change(self, mode: str):
        """Handle mode change."""
        self.state.current_mode = mode
        if self.console_view:
            self.console_view.update_mode(mode)
        print(f"Mode changed to: {mode}")
    
    def on_example_selected(self, example: str):
        """Handle example selection."""
        if self.console_view and example != "Choose an example ▾":
            self.console_view.command_entry.delete(0, "end")
            self.console_view.command_entry.insert(0, example)
    
    def on_voice_toggle(self):
        """Handle voice input toggle."""
        print("Voice input activated...")
        if self.console_view:
            self.console_view.transcription_label.configure(text="🎤 Listening...")
        
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                
                if self.console_view:
                    self.console_view.command_entry.delete(0, "end")
                    self.console_view.command_entry.insert(0, text)
                    self.console_view.transcription_label.configure(
                        text=f"✅ Transcribed: {text}"
                    )
        except Exception as e:
            if self.console_view:
                self.console_view.transcription_label.configure(
                    text=f"❌ Error: {str(e)}"
                )
    
    def on_execute(self):
        """Handle command execution."""
        if not self.console_view:
            return
        
        command = self.console_view.get_command()
        if not command:
            return
        
        # Add processing card
        self.console_view.add_response_card(
            summary="⏳ Processing command...",
            body=f"Command: {command}\nMode: {self.state.current_mode}",
            status="processing",
            mode=self.state.current_mode
        )
        
        # Clear input immediately
        self.console_view.clear_command()
        
        # Execute command with agent in background thread
        import threading
        
        def execute_in_background():
            result = self.agent_manager.execute_command(
                command=command,
                mode=self.state.current_mode
            )
            
            # Update UI on main thread
            if self.console_view:
                self.console_view.after(0, lambda: self.console_view.add_response_card(
                    summary=result.get("message", "Command completed"),
                    body=result.get("response", "No response"),
                    status=result.get("status", "success"),
                    duration=result.get("duration", "-"),
                    mode=self.state.current_mode
                ))
        
        # Run in background to avoid blocking UI
        thread = threading.Thread(target=execute_in_background, daemon=True)
        thread.start()
    
    def on_quick_command(self, command: str):
        """Handle quick command button."""
        if self.console_view:
            self.console_view.command_entry.delete(0, "end")
            self.console_view.command_entry.insert(0, command)
            self.on_execute()
    
    # ========== Workflows View Methods ==========
    
    def on_new_workflow(self):
        """Handle new workflow creation."""
        print("Creating new workflow...")
    
    def on_import_workflow(self):
        """Handle workflow import."""
        print("Importing workflow...")
    
    def on_filter_workflows(self, filter_type: str):
        """Handle workflow filtering."""
        print(f"Filtering workflows: {filter_type}")
    
    def on_run_workflow(self, name: str):
        """Handle workflow execution."""
        print(f"Running workflow: {name}")
    
    def on_edit_workflow(self, name: str):
        """Handle workflow editing."""
        print(f"Editing workflow: {name}")
    
    def on_export_workflow(self, name: str):
        """Handle workflow export."""
        print(f"Exporting workflow: {name}")
    
    def on_delete_workflow(self, name: str):
        """Handle workflow deletion."""
        print(f"Deleting workflow: {name}")
    
    def load_workflows(self):
        """Load workflows from storage."""
        # Sample workflows
        if self.workflows_view:
            workflows = [
                {
                    "name": "Morning Routine",
                    "description": "Opens email, calendar, and task manager",
                    "status": "active",
                    "steps": 5,
                    "last_run": "Today",
                    "success_rate": "98%"
                },
                {
                    "name": "Report Generator",
                    "description": "Generates weekly sales reports",
                    "status": "active",
                    "steps": 8,
                    "last_run": "2 days ago",
                    "success_rate": "95%"
                },
            ]
            
            for wf in workflows:
                self.workflows_view.add_workflow_card(**wf)
    
    # ========== Integrations View Methods ==========
    
    def on_connect_gmail(self):
        """Handle Gmail connection."""
        print("Connecting to Gmail...")
    
    def on_toggle_auto_send(self):
        """Handle auto-send toggle."""
        print("Auto-send toggled")
    
    def on_add_webhook(self):
        """Handle webhook addition."""
        print("Adding webhook...")
    
    # ========== Context View Methods ==========
    
    def on_refresh_context(self):
        """Handle context refresh."""
        print("Refreshing context insights...")
    
    # ========== Security View Methods ==========
    
    def on_security_scan(self):
        """Handle security scan."""
        print("Running security scan...")
    
    # ========== Settings View Methods ==========
    
    def on_theme_change(self, theme: str):
        """Handle theme change."""
        self.settings.set("theme", theme)
        print(f"Theme changed to: {theme}")
    
    def on_reset_settings(self):
        """Handle settings reset."""
        print("Resetting settings to defaults...")
    
    # ========== Logs View Methods ==========
    
    def on_clear_logs(self):
        """Handle logs clearing."""
        print("Clearing logs...")
    
    def on_export_logs(self):
        """Handle logs export."""
        print("Exporting logs...")
    
    # ========== Help View Methods ==========
    
    def on_help_topic(self, topic: str):
        """Handle help topic selection."""
        print(f"Showing help for: {topic}")
    
    # ========== Navigation Methods ==========
    
    def navigate_to(self, view: str):
        """Handle navigation to different views."""
        self.state.current_view = view
        if self.on_view_change:
            self.on_view_change(view)
