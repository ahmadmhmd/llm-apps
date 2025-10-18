"""Professional help and documentation view."""

import customtkinter as ctk
from typing import Dict


class HelpView(ctk.CTkFrame):
    """Modern help center with searchable docs."""
    
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
        """Build the professional help UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Quick links
        quick_links = self._build_quick_links()
        quick_links.pack(fill="x", padx=24, pady=(0, 20))
        
        # Documentation content
        content = self._build_content()
        content.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the help header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid_columnconfigure(0, weight=1)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="❓ Help Center",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Find answers and learn how to use Windows Use Agent",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        # Search
        search = ctk.CTkFrame(header, fg_color="transparent")
        search.grid(row=0, column=1, sticky="e", padx=(16, 0))
        
        self.search_entry = ctk.CTkEntry(
            search,
            placeholder_text="🔍 Search documentation...",
            width=300,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.search_entry.pack()
        
        return header
    
    def _build_quick_links(self) -> ctk.CTkFrame:
        """Build quick links section."""
        links = ctk.CTkFrame(self, fg_color="transparent")
        links.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        quick_items = [
            ("🚀 Getting Started", "#3b82f6", "quick-start"),
            ("📖 User Guide", "#10b981", "user-guide"),
            ("💡 Examples", "#f59e0b", "examples"),
            ("🐛 Report Bug", "#ef4444", "bug-report"),
        ]
        
        for idx, (text, color, action) in enumerate(quick_items):
            btn = ctk.CTkButton(
                links,
                text=text,
                height=50,
                corner_radius=14,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=color,
                hover_color=color + "CC",
                command=lambda a=action: self.controller.on_help_topic(a),
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=6)
        
        return links
    
    def _build_content(self) -> ctk.CTkFrame:
        """Build documentation content."""
        container = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        
        # Sidebar navigation
        sidebar = self._build_help_sidebar(container)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Content area
        self.content_scroll = ctk.CTkScrollableFrame(
            container,
            corner_radius=0,
            fg_color="transparent",
        )
        self.content_scroll.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Default content
        self._show_getting_started()
        
        return container
    
    def _build_help_sidebar(self, parent) -> ctk.CTkFrame:
        """Build help sidebar navigation."""
        sidebar = ctk.CTkFrame(
            parent,
            width=220,
            corner_radius=0,
            fg_color=self.palette["surface_alt"],
        )
        sidebar.pack_propagate(False)
        
        # Header
        ctk.CTkLabel(
            sidebar,
            text="📚 Topics",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w", padx=16, pady=(16, 12))
        
        # Topics
        topics = [
            ("🚀 Getting Started", "getting-started"),
            ("💻 Basic Commands", "basic-commands"),
            ("🔄 Workflows", "workflows"),
            ("🔌 Integrations", "integrations"),
            ("🛡️ Security", "security"),
            ("⚙️ Settings", "settings"),
            ("🎤 Voice Control", "voice-control"),
            ("📊 Context & Memory", "context"),
            ("❓ FAQ", "faq"),
            ("🔗 API Reference", "api"),
        ]
        
        for text, topic in topics:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                height=36,
                corner_radius=10,
                font=ctk.CTkFont(size=12),
                fg_color="transparent",
                hover_color=self.palette["surface_subtle"],
                anchor="w",
                command=lambda t=topic: self.controller.on_help_topic(t),
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # Support section
        support_frame = ctk.CTkFrame(
            sidebar,
            corner_radius=12,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        support_frame.pack(fill="x", padx=10, pady=(20, 16))
        
        ctk.CTkLabel(
            support_frame,
            text="💬 Need Help?",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.palette["text"],
        ).pack(padx=12, pady=(10, 6))
        
        ctk.CTkLabel(
            support_frame,
            text="Contact our support team for assistance",
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
            wraplength=170,
        ).pack(padx=12, pady=(0, 8))
        
        ctk.CTkButton(
            support_frame,
            text="📧 Contact Support",
            height=32,
            corner_radius=10,
            font=ctk.CTkFont(size=11),
            fg_color="#10b981",
            hover_color="#059669",
        ).pack(padx=12, pady=(0, 10))
        
        return sidebar
    
    def _show_getting_started(self):
        """Show getting started content."""
        # Clear existing content
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
        
        # Title
        ctk.CTkLabel(
            self.content_scroll,
            text="🚀 Getting Started",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w", pady=(0, 12))
        
        # Introduction
        sections = [
            ("Welcome!", "Windows Use Agent is an AI-powered assistant that helps you automate tasks on Windows using natural language commands."),
            ("Quick Start", "1. Enter a command in the console (e.g., 'Open Notepad')\n2. Select a mode (Basic, Advanced, or Expert)\n3. Click Execute or press Enter\n4. Watch the AI execute your command"),
            ("Modes Explained", "• Basic: Simple, safe commands for everyday tasks\n• Advanced: More complex operations and integrations\n• Expert: Full system access with advanced features"),
            ("Tips", "• Use the examples dropdown for inspiration\n• Try voice commands with the microphone button\n• Create workflows to automate repeated tasks\n• Check the security center for permission settings"),
        ]
        
        for title, content in sections:
            card = ctk.CTkFrame(
                self.content_scroll,
                corner_radius=14,
                fg_color=self.palette["surface_alt"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.palette["text"],
            ).pack(anchor="w", padx=16, pady=(14, 6))
            
            ctk.CTkLabel(
                card,
                text=content,
                font=ctk.CTkFont(size=12),
                text_color=self.palette["text_soft"],
                wraplength=600,
                justify="left",
            ).pack(anchor="w", padx=16, pady=(0, 14))
