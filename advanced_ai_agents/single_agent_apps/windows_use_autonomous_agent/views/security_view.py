"""Professional security center view."""

import customtkinter as ctk
from typing import Dict


class SecurityView(ctk.CTkFrame):
    """Modern security settings and controls."""
    
    def __init__(
        self,
        parent,
        palette: Dict[str, tuple],
        controller
    ):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.palette = palette
        self.controller = controller
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the professional security UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Security status
        status = self._build_status()
        status.pack(fill="x", padx=24, pady=(0, 20))
        
        # Settings sections
        settings = self._build_settings()
        settings.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the security header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(
            header,
            text="🔒 Security Center",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Manage permissions and sandbox settings",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        return header
    
    def _build_status(self) -> ctk.CTkFrame:
        """Build security status card."""
        card = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=2,
            border_color="#10b981",
        )
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=16)
        content.grid_columnconfigure(0, weight=1)
        
        status_info = ctk.CTkFrame(content, fg_color="transparent")
        status_info.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            status_info,
            text="🛡️ Security Status: Protected",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#10b981",
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            status_info,
            text="All security features are active and configured",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        # Scan button
        ctk.CTkButton(
            content,
            text="🔍 Run Security Scan",
            width=160,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=self.controller.on_security_scan,
        ).grid(row=0, column=1, sticky="e", padx=(12, 0))
        
        return card
    
    def _build_settings(self) -> ctk.CTkScrollableFrame:
        """Build security settings."""
        scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        
        # Permissions section
        self._add_section(scroll, "🔑 Permissions", [
            ("File System Access", "Allow reading and writing files", True),
            ("Network Access", "Allow internet connections", True),
            ("System Commands", "Allow executing system commands", True),
            ("Registry Access", "Allow modifying Windows Registry", False),
        ])
        
        # Sandbox section
        self._add_section(scroll, "📦 Sandbox Mode", [
            ("Enable Sandbox", "Run commands in isolated environment", False),
            ("Auto-rollback", "Undo changes if errors occur", True),
            ("Backup Before Execute", "Create restore point", True),
        ])
        
        # Monitoring section
        self._add_section(scroll, "👁️ Monitoring", [
            ("Activity Logging", "Record all command executions", True),
            ("Alert on Suspicious", "Notify about unusual activity", True),
            ("Weekly Reports", "Email security summaries", False),
        ])
        
        return scroll
    
    def _add_section(self, parent, title: str, settings: list):
        """Add a settings section."""
        # Section header
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 12))
        
        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        # Settings cards
        for name, description, default_value in settings:
            card = ctk.CTkFrame(
                parent,
                corner_radius=14,
                fg_color=self.palette["surface_alt"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.pack(fill="x", padx=20, pady=6)
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=16, pady=12)
            content.grid_columnconfigure(0, weight=1)
            
            info = ctk.CTkFrame(content, fg_color="transparent")
            info.grid(row=0, column=0, sticky="w")
            
            ctk.CTkLabel(
                info,
                text=name,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.palette["text"],
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info,
                text=description,
                font=ctk.CTkFont(size=11),
                text_color=self.palette["text_soft"],
            ).pack(anchor="w", pady=(2, 0))
            
            switch = ctk.CTkSwitch(
                content,
                text="",
                command=lambda: None,
            )
            if default_value:
                switch.select()
            switch.grid(row=0, column=1, sticky="e", padx=(12, 0))
