"""Sidebar navigation component."""

import customtkinter as ctk
from typing import Dict, Callable, Optional
from config import NAV_ITEMS
from utils import CTkToolTip


class Sidebar(ctk.CTkFrame):
    """Professional sidebar with navigation and status."""
    
    def __init__(
        self,
        parent,
        palette: Dict[str, tuple],
        on_navigate: Callable,
        user_profile: Dict[str, Optional[str]]
    ):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=palette["sidebar"]
        )
        
        self.palette = palette
        self.on_navigate = on_navigate
        self.user_profile = user_profile
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        self.collapsed = False
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the sidebar UI."""
        # Header with branding
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(24, 18))
        
        # App brand
        brand = ctk.CTkLabel(
            header,
            text="⚡ Windows Use\nEnterprise AI",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="left",
            text_color=self.palette["text"],
        )
        brand.pack(anchor="w")
        
        # Version badge
        version = ctk.CTkLabel(
            header,
            text="v2.0",
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
        )
        version.pack(anchor="w", pady=(4, 0))
        
        # Status card with glassmorphism effect
        status = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        status.pack(fill="x", padx=20, pady=(0, 20))
        
        # Status header
        status_header = ctk.CTkFrame(status, fg_color="transparent")
        status_header.pack(fill="x", padx=16, pady=(14, 8))
        
        ctk.CTkLabel(
            status_header,
            text="🔥 System Status",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        self.status_badge = ctk.CTkLabel(
            status_header,
            text="● Ready",
            font=ctk.CTkFont(size=11),
            text_color="#10b981",
        )
        self.status_badge.pack(side="right")
        
        # Status message
        self.status_message = ctk.CTkLabel(
            status,
            text="All systems operational",
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
        )
        self.status_message.pack(anchor="w", padx=16, pady=(0, 8))
        
        # User info
        user_name = self.user_profile.get("name", "User")
        ctk.CTkLabel(
            status,
            text=f"👤 {user_name}",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", padx=16, pady=(0, 4))
        
        # Location with icon
        location = self.user_profile.get("location", "Unknown")
        self.location_label = ctk.CTkLabel(
            status,
            text=f"📍 {location}",
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
        )
        self.location_label.pack(anchor="w", padx=16, pady=(0, 14))
        
        # Divider
        divider = ctk.CTkFrame(self, height=1, fg_color=self.palette["stroke"])
        divider.pack(fill="x", padx=20, pady=(0, 16))
        
        # Navigation buttons with modern design
        nav_label = ctk.CTkLabel(
            self,
            text="NAVIGATION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.palette["muted"],
        )
        nav_label.pack(anchor="w", padx=20, pady=(0, 12))
        
        for name, icon, tooltip in NAV_ITEMS:
            btn = ctk.CTkButton(
                self,
                text=f"{icon}  {name}",
                anchor="w",
                height=48,
                corner_radius=12,
                fg_color="transparent",
                text_color=self.palette["text"],
                hover_color=self.palette["surface_alt"],
                border_width=0,
                font=ctk.CTkFont(size=13),
                command=lambda view=name: self.on_navigate(view),
            )
            btn.pack(fill="x", padx=20, pady=3)
            CTkToolTip(btn, tooltip)
            self.nav_buttons[name] = btn
        
        # Footer with modern styling
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            footer_frame,
            text="Enterprise Edition",
            font=ctk.CTkFont(size=10),
            text_color=self.palette["muted"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            footer_frame,
            text="© 2025 Adaptive AI",
            font=ctk.CTkFont(size=9),
            text_color=self.palette["muted"],
        ).pack(anchor="w", pady=(2, 0))
    
    def update_status(self, status: str, message: str = "Ready"):
        """Update the status badge and message."""
        # Status colors
        status_colors = {
            "online": "#10b981",
            "offline": "#ef4444",
            "busy": "#f59e0b",
            "away": "#6b7280",
        }
        color = status_colors.get(status.lower(), "#10b981")
        
        self.status_badge.configure(text=f"● {status.title()}", text_color=color)
        self.status_message.configure(text=message)
    
    def highlight_nav(self, view_name: str):
        """Highlight the active navigation button."""
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.configure(
                    fg_color=self.palette["surface"],
                    border_width=1,
                    border_color=self.palette["stroke"],
                    text_color=self.palette["text"],
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    border_width=0,
                    text_color=self.palette["text"],
                )
