"""Professional context insights view."""

import customtkinter as ctk
from typing import Dict


class ContextView(ctk.CTkFrame):
    """Modern context analytics with charts."""
    
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
        """Build the professional context UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Metrics grid
        metrics = self._build_metrics()
        metrics.pack(fill="x", padx=24, pady=(0, 20))
        
        # Insights cards
        insights = self._build_insights()
        insights.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the context header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid_columnconfigure(0, weight=1)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="🧠 Context Insights",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="AI memory and behavior analytics",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        # Refresh button
        ctk.CTkButton(
            header,
            text="🔄 Refresh",
            width=110,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color=self.palette["surface"],
            hover_color=self.palette["surface_subtle"],
            border_width=1,
            border_color=self.palette["stroke"],
            text_color=self.palette["text"],
            command=self.controller.on_refresh_context,
        ).grid(row=0, column=1, sticky="e", padx=(16, 0))
        
        return header
    
    def _build_metrics(self) -> ctk.CTkFrame:
        """Build metrics cards."""
        metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        metrics = [
            ("💾 Context Size", "2.3 MB", "#3b82f6", "of 10 MB used"),
            ("📝 Stored Items", "156", "#10b981", "in memory"),
            ("⚡ Processing", "Fast", "#f59e0b", "avg 120ms"),
        ]
        
        for idx, (label, value, color, sublabel) in enumerate(metrics):
            card = ctk.CTkFrame(
                metrics_frame,
                corner_radius=16,
                fg_color=self.palette["surface"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.grid(row=0, column=idx, sticky="ew", padx=6)
            
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=self.palette["text_soft"],
            ).pack(padx=16, pady=(14, 4))
            
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=color,
            ).pack(padx=16)
            
            ctk.CTkLabel(
                card,
                text=sublabel,
                font=ctk.CTkFont(size=10),
                text_color=self.palette["text_soft"],
            ).pack(padx=16, pady=(0, 14))
        
        return metrics_frame
    
    def _build_insights(self) -> ctk.CTkFrame:
        """Build insights section."""
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
        ctk.CTkLabel(
            section,
            text="📊 Detailed Insights",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 12))
        
        # Scrollable insights
        self.insights_scroll = ctk.CTkScrollableFrame(
            section,
            corner_radius=12,
            fg_color="transparent",
        )
        self.insights_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 18))
        
        # Sample insights
        self._add_insight_cards()
        
        return section
    
    def _add_insight_cards(self):
        """Add sample insight cards."""
        insights = [
            ("🎯 Most Used Commands", "File operations (42%), Browser actions (28%)", "#3b82f6"),
            ("⏰ Peak Activity", "Between 2 PM - 5 PM on weekdays", "#10b981"),
            ("🔥 Hot Topics", "Project management, code development, email", "#f59e0b"),
            ("💡 Suggestions", "Consider creating workflows for repeated tasks", "#8b5cf6"),
        ]
        
        for title, content, color in insights:
            card = ctk.CTkFrame(
                self.insights_scroll,
                corner_radius=14,
                fg_color=self.palette["surface_alt"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=color,
            ).pack(anchor="w", padx=14, pady=(12, 4))
            
            ctk.CTkLabel(
                card,
                text=content,
                font=ctk.CTkFont(size=11),
                text_color=self.palette["text"],
                wraplength=500,
                justify="left",
            ).pack(anchor="w", padx=14, pady=(0, 12))
