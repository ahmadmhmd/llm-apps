"""Professional workflows management view."""

import customtkinter as ctk
from typing import Dict, List, Callable
from datetime import datetime


class WorkflowsView(ctk.CTkFrame):
    """Modern workflow management with card-based layout."""
    
    def __init__(
        self,
        parent,
        palette: Dict[str, tuple],
        controller
    ):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.palette = palette
        self.controller = controller
        self.workflow_cards: List[ctk.CTkFrame] = []
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the professional workflows UI."""
        # Header with actions
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Stats cards
        stats = self._build_stats_cards()
        stats.pack(fill="x", padx=24, pady=(0, 20))
        
        # Workflows grid
        workflows_section = self._build_workflows_section()
        workflows_section.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the workflows header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid_columnconfigure(0, weight=1)
        
        # Title section
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            title_frame,
            text="🔄 Workflow Automation",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Create and manage automated command sequences",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        # Action buttons
        actions = ctk.CTkFrame(header, fg_color="transparent")
        actions.grid(row=0, column=1, sticky="e", padx=(16, 0))
        
        ctk.CTkButton(
            actions,
            text="➕ New Workflow",
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=self.controller.on_new_workflow,
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            actions,
            text="📥 Import",
            width=100,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color=self.palette["surface"],
            hover_color=self.palette["surface_subtle"],
            border_width=1,
            border_color=self.palette["stroke"],
            text_color=self.palette["text"],
            command=self.controller.on_import_workflow,
        ).pack(side="left", padx=4)
        
        return header
    
    def _build_stats_cards(self) -> ctk.CTkFrame:
        """Build statistics cards."""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        stats = [
            ("📊 Total Workflows", "12", "#3b82f6"),
            ("✅ Active", "8", "#10b981"),
            ("⏸️ Paused", "3", "#f59e0b"),
            ("🚀 Runs Today", "47", "#8b5cf6"),
        ]
        
        for idx, (label, value, color) in enumerate(stats):
            card = ctk.CTkFrame(
                stats_frame,
                corner_radius=16,
                fg_color=self.palette["surface"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            card.grid(row=0, column=idx, sticky="ew", padx=6)
            
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=11),
                text_color=self.palette["text_soft"],
            ).pack(padx=16, pady=(12, 4))
            
            ctk.CTkLabel(
                card,
                text=value,
                font=ctk.CTkFont(size=28, weight="bold"),
                text_color=color,
            ).pack(padx=16, pady=(0, 12))
        
        return stats_frame
    
    def _build_workflows_section(self) -> ctk.CTkFrame:
        """Build the workflows list section."""
        section = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        section.grid_rowconfigure(1, weight=1)
        section.grid_columnconfigure(0, weight=1)
        
        # Header with search
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 12))
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header,
            text="📁 My Workflows",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, sticky="w")
        
        # Search bar
        self.search_entry = ctk.CTkEntry(
            header,
            placeholder_text="🔍 Search workflows...",
            height=36,
            width=250,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.search_entry.grid(row=0, column=1, sticky="e", padx=(12, 0))
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.grid(row=0, column=2, sticky="e", padx=(12, 0))
        
        for text in ["All", "Active", "Paused"]:
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                width=70,
                height=32,
                corner_radius=10,
                font=ctk.CTkFont(size=11),
                fg_color=self.palette["surface_alt"] if text == "All" else "transparent",
                hover_color=self.palette["surface_alt"],
                border_width=1,
                border_color=self.palette["stroke"],
                text_color=self.palette["text"],
                command=lambda t=text: self.controller.on_filter_workflows(t),
            )
            btn.pack(side="left", padx=2)
        
        # Scrollable workflow list
        self.workflow_list = ctk.CTkScrollableFrame(
            section,
            corner_radius=12,
            fg_color="transparent",
        )
        self.workflow_list.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 18))
        self.workflow_list.grid_columnconfigure(0, weight=1)
        
        # Empty state
        self.workflow_list_empty = ctk.CTkFrame(
            self.workflow_list,
            fg_color="transparent",
        )
        
        ctk.CTkLabel(
            self.workflow_list_empty,
            text="📋",
            font=ctk.CTkFont(size=48),
        ).pack(pady=(40, 12))
        
        ctk.CTkLabel(
            self.workflow_list_empty,
            text="No workflows yet",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).pack()
        
        ctk.CTkLabel(
            self.workflow_list_empty,
            text="Create your first workflow to get started",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        ).pack(pady=(4, 40))
        
        self.workflow_list_empty.pack(fill="both", expand=True)
        
        return section
    
    def add_workflow_card(
        self,
        name: str,
        description: str,
        status: str = "active",
        steps: int = 0,
        last_run: str = "Never",
        success_rate: str = "N/A"
    ):
        """Add a workflow card to the list."""
        # Hide empty state
        if self.workflow_list_empty.winfo_ismapped():
            self.workflow_list_empty.pack_forget()
        
        # Status colors and icons
        status_config = {
            "active": ("#10b981", "🟢", "Active"),
            "paused": ("#f59e0b", "⏸️", "Paused"),
            "error": ("#ef4444", "🔴", "Error"),
        }
        color, icon, label = status_config.get(status, ("#6b7280", "⚪", "Unknown"))
        
        # Workflow card
        card = ctk.CTkFrame(
            self.workflow_list,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        card.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))
        header.grid_columnconfigure(1, weight=1)
        
        # Workflow icon and name
        name_frame = ctk.CTkFrame(header, fg_color="transparent")
        name_frame.grid(row=0, column=0, sticky="w")
        
        ctk.CTkLabel(
            name_frame,
            text="🔄",
            font=ctk.CTkFont(size=20),
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkLabel(
            name_frame,
            text=name,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        # Status badge
        status_badge = ctk.CTkFrame(
            header,
            corner_radius=10,
            fg_color=color + "20",  # 20% opacity
            border_width=1,
            border_color=color,
        )
        status_badge.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(
            status_badge,
            text=f"{icon} {label}",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=color,
        ).pack(padx=10, pady=4)
        
        # Description
        ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
            wraplength=600,
            justify="left",
        ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))
        
        # Metadata row
        metadata = ctk.CTkFrame(card, fg_color="transparent")
        metadata.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        
        info_items = [
            (f"📊 {steps} steps", self.palette["text_soft"]),
            (f"⏱️ {last_run}", self.palette["text_soft"]),
            (f"✅ {success_rate} success", "#10b981" if success_rate != "N/A" else self.palette["text_soft"]),
        ]
        
        for text, text_color in info_items:
            ctk.CTkLabel(
                metadata,
                text=text,
                font=ctk.CTkFont(size=11),
                text_color=text_color,
            ).pack(side="left", padx=(0, 16))
        
        # Action buttons
        actions = ctk.CTkFrame(metadata, fg_color="transparent")
        actions.pack(side="right")
        
        action_buttons = [
            ("▶️ Run", "#10b981", self.controller.on_run_workflow),
            ("✏️ Edit", "#3b82f6", self.controller.on_edit_workflow),
            ("📤 Export", "#8b5cf6", self.controller.on_export_workflow),
            ("🗑️ Delete", "#ef4444", self.controller.on_delete_workflow),
        ]
        
        for text, btn_color, command in action_buttons:
            btn = ctk.CTkButton(
                actions,
                text=text,
                width=80,
                height=32,
                corner_radius=10,
                font=ctk.CTkFont(size=10),
                fg_color=btn_color,
                hover_color=btn_color + "CC",  # Darker on hover
                command=lambda n=name, c=command: c(n),
            )
            btn.pack(side="left", padx=2)
        
        card.pack(fill="x", padx=4, pady=6)
        self.workflow_cards.append(card)
    
    def clear_workflows(self):
        """Clear all workflow cards."""
        for card in self.workflow_cards:
            card.destroy()
        self.workflow_cards.clear()
        
        # Show empty state
        if not self.workflow_list_empty.winfo_ismapped():
            self.workflow_list_empty.pack(fill="both", expand=True)
    
    def refresh(self):
        """Refresh the workflows list."""
        self.clear_workflows()
        self.controller.load_workflows()
