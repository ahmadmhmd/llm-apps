"""Main application window - coordinates all views."""

import customtkinter as ctk
from typing import Dict
from config import COLOR_PALETTE, NAV_ITEMS
from views import (
    Sidebar, ConsoleView, WorkflowsView, IntegrationsView,
    ContextView, SecurityView, SettingsView, LogsView, HelpView
)
from controllers import AppController


class MainWindow(ctk.CTk):
    """Main application window with MVC architecture."""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("⚡ Windows Use Enterprise AI")
        self.geometry("1400x900")
        
        # Color palette - Dark theme (index 1)
        self.current_theme = "dark"
        self.palette = {
            "name": self.current_theme,
            "background": COLOR_PALETTE["background"][1],
            "sidebar": COLOR_PALETTE["sidebar"][1],
            "surface": COLOR_PALETTE["surface"][1],
            "surface_alt": COLOR_PALETTE["surface_alt"][1],
            "surface_subtle": COLOR_PALETTE["surface_subtle"][1],
            "stroke": COLOR_PALETTE["stroke"][1],
            "muted": COLOR_PALETTE["muted"][1],
            "text": COLOR_PALETTE["text"][1],
            "text_soft": COLOR_PALETTE["text_soft"][1],
        }
        
        # Set appearance
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        # Controller
        self.controller = AppController()
        self.controller.main_window = self
        self.controller.on_view_change = self._switch_view
        
        # Build UI
        self._build_ui()
        
        # Show initial view
        self._switch_view("Console")
        
        # Update sidebar status
        self.sidebar.update_status("online", "Ready")
    
    def _build_ui(self):
        """Build the main UI structure."""
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # User profile data
        user_profile = {
            "name": "User",
            "role": "Administrator",
            "location": None
        }
        
        # Sidebar
        self.sidebar = Sidebar(
            self,
            self.palette,
            self.controller.navigate_to,
            user_profile
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Main content area
        self.content_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.palette["background"]
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create all views
        self._create_views()
    
    def _create_views(self):
        """Create all view instances."""
        self.views: Dict[str, ctk.CTkFrame] = {}
        
        # Console View
        self.views["Console"] = ConsoleView(
            self.content_frame,
            self.palette,
            self.controller,
            self.controller.state.current_mode
        )
        self.controller.console_view = self.views["Console"]
        
        # Workflows View
        self.views["Workflows"] = WorkflowsView(
            self.content_frame,
            self.palette,
            self.controller
        )
        self.controller.workflows_view = self.views["Workflows"]
        
        # Integrations View
        self.views["Integrations"] = IntegrationsView(
            self.content_frame,
            self.palette,
            self.controller
        )
        
        # Context View
        self.views["Context"] = ContextView(
            self.content_frame,
            self.palette,
            self.controller
        )
        
        # Security View
        self.views["Security"] = SecurityView(
            self.content_frame,
            self.palette,
            self.controller
        )
        
        # Settings View
        self.views["Settings"] = SettingsView(
            self.content_frame,
            self.palette,
            self.controller
        )
        
        # Logs View
        self.views["Logs"] = LogsView(
            self.content_frame,
            self.palette,
            self.controller
        )
        
        # Help View
        self.views["Help"] = HelpView(
            self.content_frame,
            self.palette,
            self.controller
        )
    
    def _switch_view(self, view_name: str):
        """Switch to a different view."""
        # Hide all views
        for view in self.views.values():
            view.grid_forget()
        
        # Show selected view
        if view_name in self.views:
            self.views[view_name].grid(row=0, column=0, sticky="nsew")
            
            # Update sidebar highlight
            self.sidebar.highlight_nav(view_name)
            
            # Load data if needed
            if view_name == "Workflows":
                self.controller.load_workflows()
    
    def run(self):
        """Start the application."""
        self.mainloop()
