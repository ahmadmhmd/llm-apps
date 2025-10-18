"""Professional activity logs view."""

import customtkinter as ctk
from typing import Dict
from datetime import datetime


class LogsView(ctk.CTkFrame):
    """Modern activity logs with timeline."""
    
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
        """Build the professional logs UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Filters and search
        filters = self._build_filters()
        filters.pack(fill="x", padx=24, pady=(0, 16))
        
        # Logs timeline
        logs_section = self._build_logs_section()
        logs_section.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the logs header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid_columnconfigure(0, weight=1)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="📜 Activity Logs",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="View command execution history and system events",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        # Action buttons
        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=1, sticky="e", padx=(16, 0))
        
        ctk.CTkButton(
            actions,
            text="🗑️ Clear Logs",
            width=110,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.controller.on_clear_logs,
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            actions,
            text="💾 Export",
            width=100,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color=self.palette["surface"],
            hover_color=self.palette["surface_subtle"],
            border_width=1,
            border_color=self.palette["stroke"],
            text_color=self.palette["text"],
            command=self.controller.on_export_logs,
        ).pack(side="left", padx=4)
        
        return header
    
    def _build_filters(self) -> ctk.CTkFrame:
        """Build filter controls."""
        filters = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        filters.grid_columnconfigure(0, weight=1)
        
        content = ctk.CTkFrame(filters, fg_color="transparent")
        content.pack(fill="x", padx=16, pady=12)
        content.grid_columnconfigure(0, weight=1)
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            content,
            placeholder_text="🔍 Search logs...",
            height=38,
            corner_radius=12,
            font=ctk.CTkFont(size=12),
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        
        # Level filter
        self.level_menu = ctk.CTkOptionMenu(
            content,
            values=["All Levels", "Info", "Warning", "Error", "Success"],
            width=130,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
        )
        self.level_menu.set("All Levels")
        self.level_menu.grid(row=0, column=1, padx=4)
        
        # Time filter
        self.time_menu = ctk.CTkOptionMenu(
            content,
            values=["All Time", "Today", "This Week", "This Month"],
            width=130,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
        )
        self.time_menu.set("All Time")
        self.time_menu.grid(row=0, column=2, padx=4)
        
        return filters
    
    def _build_logs_section(self) -> ctk.CTkFrame:
        """Build the logs timeline section."""
        section = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        section.grid_rowconfigure(1, weight=1)
        section.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 12))
        
        ctk.CTkLabel(
            header,
            text="📊 Activity Timeline",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        self.log_count = ctk.CTkLabel(
            header,
            text="0 entries",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        )
        self.log_count.pack(side="right")
        
        # Scrollable logs
        self.logs_scroll = ctk.CTkScrollableFrame(
            section,
            corner_radius=12,
            fg_color="transparent",
        )
        self.logs_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 18))
        
        # Sample logs
        self._add_sample_logs()
        
        return section
    
    def _add_sample_logs(self):
        """Add sample log entries."""
        logs = [
            ("info", "Application started", "System initialized successfully", "2 min ago"),
            ("success", "Command executed", "Opened Notepad application", "5 min ago"),
            ("warning", "Network latency", "Response time exceeded 2 seconds", "8 min ago"),
            ("success", "Workflow completed", "Morning routine workflow finished", "15 min ago"),
            ("error", "Failed to connect", "Gmail API authentication error", "23 min ago"),
        ]
        
        for level, title, message, time in logs:
            self.add_log_entry(level, title, message, time)
    
    def add_log_entry(self, level: str, title: str, message: str, time: str = ""):
        """Add a log entry to the timeline."""
        if not time:
            time = datetime.now().strftime("%I:%M %p")
        
        # Level styling
        level_config = {
            "info": ("ℹ️", "#3b82f6", "#eff6ff"),
            "success": ("✅", "#10b981", "#f0fdf4"),
            "warning": ("⚠️", "#f59e0b", "#fffbeb"),
            "error": ("❌", "#ef4444", "#fef2f2"),
        }
        icon, color, bg = level_config.get(level, ("•", self.palette["text_soft"][0], self.palette["surface_alt"]))
        
        # Log entry card
        entry = ctk.CTkFrame(
            self.logs_scroll,
            corner_radius=14,
            fg_color=bg if self.palette["name"] == "light" else self.palette["surface_alt"],
            border_width=1,
            border_color=color,
        )
        entry.pack(fill="x", pady=6)
        
        content = ctk.CTkFrame(entry, fg_color="transparent")
        content.pack(fill="x", padx=14, pady=12)
        content.grid_columnconfigure(1, weight=1)
        
        # Icon
        ctk.CTkLabel(
            content,
            text=icon,
            font=ctk.CTkFont(size=20),
        ).grid(row=0, column=0, rowspan=2, sticky="n", padx=(0, 12))
        
        # Title
        ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=1, sticky="w")
        
        # Time
        ctk.CTkLabel(
            content,
            text=time,
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
        ).grid(row=0, column=2, sticky="e", padx=(12, 0))
        
        # Message
        ctk.CTkLabel(
            content,
            text=message,
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
            wraplength=500,
            justify="left",
        ).grid(row=1, column=1, columnspan=2, sticky="w", pady=(4, 0))
