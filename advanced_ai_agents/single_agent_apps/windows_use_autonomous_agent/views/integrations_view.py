"""Professional integrations management view."""

import customtkinter as ctk
from typing import Dict, Callable


class IntegrationsView(ctk.CTkFrame):
    """Modern integrations with tabbed interface."""
    
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
        """Build the professional integrations UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Tabbed content
        tabs = self._build_tabs()
        tabs.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the integrations header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(
            header,
            text="🔌 Integrations",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Connect external services and storage",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        return header
    
    def _build_tabs(self) -> ctk.CTkTabview:
        """Build the tabbed interface."""
        tabview = ctk.CTkTabview(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        
        # Create tabs
        gmail_tab = tabview.add("📧 Gmail")
        storage_tab = tabview.add("☁️ Storage")
        webhook_tab = tabview.add("🔗 Webhooks")
        
        # Build tab content
        self._build_gmail_tab(gmail_tab)
        self._build_storage_tab(storage_tab)
        self._build_webhook_tab(webhook_tab)
        
        return tabview
    
    def _build_gmail_tab(self, parent):
        """Build Gmail integration tab."""
        # Connection status card
        status_card = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        status_card.pack(fill="x", padx=20, pady=20)
        
        header = ctk.CTkFrame(status_card, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(14, 12))
        
        ctk.CTkLabel(
            header,
            text="📧 Gmail Connection",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        self.gmail_status = ctk.CTkLabel(
            header,
            text="🔴 Not Connected",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ef4444",
        )
        self.gmail_status.pack(side="right")
        
        # Connect button
        self.gmail_connect_btn = ctk.CTkButton(
            status_card,
            text="🔑 Connect Gmail",
            height=44,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ea4335",
            hover_color="#c5221f",
            command=self.controller.on_connect_gmail,
        )
        self.gmail_connect_btn.pack(padx=16, pady=(0, 14))
        
        # Settings section
        settings_card = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        settings_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            settings_card,
            text="⚙️ Email Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w", padx=16, pady=(14, 12))
        
        # Auto-send toggle
        auto_send_frame = ctk.CTkFrame(settings_card, fg_color="transparent")
        auto_send_frame.pack(fill="x", padx=16, pady=8)
        
        ctk.CTkLabel(
            auto_send_frame,
            text="Auto-send emails",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        self.auto_send_switch = ctk.CTkSwitch(
            auto_send_frame,
            text="",
            command=self.controller.on_toggle_auto_send,
        )
        self.auto_send_switch.pack(side="right")
    
    def _build_storage_tab(self, parent):
        """Build storage integration tab."""
        # Available storage providers
        providers = [
            ("📁 Google Drive", "#4285f4", "Connect Google Drive for file storage"),
            ("📦 Dropbox", "#0061ff", "Connect Dropbox for cloud sync"),
            ("☁️ OneDrive", "#0078d4", "Connect Microsoft OneDrive"),
            ("🗄️ Box", "#0061d5", "Enterprise file storage"),
        ]
        
        for idx, (name, color, desc) in enumerate(providers):
            card = ctk.CTkFrame(
                parent,
                corner_radius=16,
                fg_color=self.palette["surface_alt"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.pack(fill="x", padx=20, pady=(20 if idx == 0 else 12))
            
            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(fill="x", padx=16, pady=14)
            content.grid_columnconfigure(0, weight=1)
            
            info = ctk.CTkFrame(content, fg_color="transparent")
            info.grid(row=0, column=0, sticky="w")
            
            ctk.CTkLabel(
                info,
                text=name,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.palette["text"],
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info,
                text=desc,
                font=ctk.CTkFont(size=11),
                text_color=self.palette["text_soft"],
            ).pack(anchor="w", pady=(2, 0))
            
            ctk.CTkButton(
                content,
                text="Connect",
                width=100,
                height=36,
                corner_radius=10,
                font=ctk.CTkFont(size=12),
                fg_color=color,
                hover_color=color + "CC",
            ).grid(row=0, column=1, sticky="e", padx=(12, 0))
    
    def _build_webhook_tab(self, parent):
        """Build webhooks integration tab."""
        # Header
        header_card = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        header_card.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            header_card,
            text="🔗 Webhook Endpoints",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w", padx=16, pady=(14, 8))
        
        ctk.CTkLabel(
            header_card,
            text="Receive data from external services via HTTP endpoints",
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", padx=16, pady=(0, 14))
        
        # Add webhook button
        ctk.CTkButton(
            parent,
            text="➕ Add Webhook",
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=self.controller.on_add_webhook,
        ).pack(padx=20, pady=(0, 12))
        
        # Webhooks list
        self.webhook_list = ctk.CTkScrollableFrame(
            parent,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.webhook_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def update_gmail_status(self, connected: bool):
        """Update Gmail connection status."""
        if connected:
            self.gmail_status.configure(
                text="🟢 Connected",
                text_color="#10b981"
            )
            self.gmail_connect_btn.configure(text="🔌 Disconnect Gmail")
        else:
            self.gmail_status.configure(
                text="🔴 Not Connected",
                text_color="#ef4444"
            )
            self.gmail_connect_btn.configure(text="🔑 Connect Gmail")
