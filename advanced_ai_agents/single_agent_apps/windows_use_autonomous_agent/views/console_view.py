"""Professional command console view."""

import customtkinter as ctk
from typing import Dict, Callable, List
from datetime import datetime
from config import MODE_COLORS, MODE_EXAMPLES, QUICK_COMMANDS
from utils import shade_color


class ConsoleView(ctk.CTkFrame):
    """Modern command console with glassmorphism design."""
    
    def __init__(
        self,
        parent,
        palette: Dict[str, tuple],
        controller,
        current_mode: str
    ):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        
        self.palette = palette
        self.controller = controller
        self.current_mode = current_mode
        self.response_cards: List[ctk.CTkFrame] = []
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the professional console UI."""
        # Header section with mode selector
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 16))
        
        # Command input section (glassmorphism card)
        input_card = self._build_input_section()
        input_card.pack(fill="x", padx=24, pady=(0, 16))
        
        # Quick actions (modern pill buttons)
        quick_actions = self._build_quick_actions()
        quick_actions.pack(fill="x", padx=24, pady=(0, 16))
        
        # Response feed (scrollable with modern cards)
        response_section = self._build_response_section()
        response_section.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the console header with mode selector."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid_columnconfigure(0, weight=1)
        
        # Title section
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")
        
        self.mode_title = ctk.CTkLabel(
            title_frame,
            text="🚀 Command Console",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        )
        self.mode_title.pack(anchor="w")
        
        self.mode_subtitle = ctk.CTkLabel(
            title_frame,
            text="Execute natural language commands with AI",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        )
        self.mode_subtitle.pack(anchor="w", pady=(4, 0))
        
        # Mode selector (modern segmented button)
        mode_frame = ctk.CTkFrame(header, fg_color="transparent")
        mode_frame.grid(row=0, column=1, sticky="e", padx=(16, 0))
        
        ctk.CTkLabel(
            mode_frame,
            text="Mode:",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        ).pack(side="left", padx=(0, 8))
        
        modes = list(MODE_COLORS.keys())
        self.mode_selector = ctk.CTkSegmentedButton(
            mode_frame,
            values=modes,
            command=self.controller.on_mode_change,
            font=ctk.CTkFont(size=12),
            corner_radius=10,
        )
        self.mode_selector.set(self.current_mode)
        self.mode_selector.pack(side="left")
        
        return header
    
    def _build_input_section(self) -> ctk.CTkFrame:
        """Build the command input section with glassmorphism."""
        card = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        
        # Examples dropdown
        examples_frame = ctk.CTkFrame(card, fg_color="transparent")
        examples_frame.pack(fill="x", padx=20, pady=(16, 12))
        
        ctk.CTkLabel(
            examples_frame,
            text="💡 Examples:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        examples = MODE_EXAMPLES.get(self.current_mode, [])
        self.examples_menu = ctk.CTkOptionMenu(
            examples_frame,
            values=examples if examples else ["No examples"],
            command=self.controller.on_example_selected,
            width=200,
            corner_radius=10,
            font=ctk.CTkFont(size=11),
        )
        self.examples_menu.set("Choose an example ▾")
        self.examples_menu.pack(side="left", padx=12)
        
        # Voice button
        self.voice_btn = ctk.CTkButton(
            examples_frame,
            text="🎤 Voice",
            width=90,
            height=32,
            corner_radius=10,
            fg_color="#1d4ed8",
            hover_color="#1e40af",
            command=self.controller.on_voice_toggle,
            font=ctk.CTkFont(size=11),
        )
        self.voice_btn.pack(side="right")
        
        # Command input area
        input_frame = ctk.CTkFrame(card, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 16))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.command_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Type your command here... (e.g., 'Open Notepad')",
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=14),
            border_width=2,
            border_color=self.palette["stroke"],
        )
        self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self.command_entry.bind("<Return>", lambda e: self.controller.on_execute())
        
        # Execute button (prominent)
        self.execute_btn = ctk.CTkButton(
            input_frame,
            text="⚡ Execute",
            width=120,
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=MODE_COLORS[self.current_mode],
            hover_color=shade_color(MODE_COLORS[self.current_mode], -0.2),
            command=self.controller.on_execute,
        )
        self.execute_btn.grid(row=0, column=1)
        
        # Transcription label (for voice input)
        self.transcription_label = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#fbbf24",
        )
        self.transcription_label.pack(anchor="w", padx=20, pady=(0, 16))
        
        return card
    
    def _build_quick_actions(self) -> ctk.CTkFrame:
        """Build quick action buttons."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(
            frame,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.palette["text_soft"],
        ).pack(side="left", padx=(0, 12))
        
        self.quick_buttons: List[ctk.CTkButton] = []
        for idx, cmd in enumerate(QUICK_COMMANDS):
            btn = ctk.CTkButton(
                frame,
                text=cmd,
                height=36,
                corner_radius=18,  # Pill shape
                font=ctk.CTkFont(size=11),
                fg_color=MODE_COLORS[self.current_mode],
                hover_color=shade_color(MODE_COLORS[self.current_mode], -0.2),
                command=lambda c=cmd: self.controller.on_quick_command(c),
            )
            btn.pack(side="left", padx=4)
            self.quick_buttons.append(btn)
        
        return frame
    
    def _build_response_section(self) -> ctk.CTkFrame:
        """Build the response feed section."""
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
        header.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            header,
            text="📊 Response Feed",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, sticky="w")
        
        self.response_timestamp = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
        )
        self.response_timestamp.grid(row=0, column=1, sticky="e")
        
        # Scrollable feed
        self.response_feed = ctk.CTkScrollableFrame(
            section,
            corner_radius=12,
            fg_color="transparent",
        )
        self.response_feed.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 18))
        self.response_feed.grid_columnconfigure(0, weight=1)
        
        return section
    
    def add_response_card(
        self,
        summary: str,
        body: str,
        status: str = "success",
        duration: str = "-",
        mode: str = "Basic"
    ):
        """Add a modern response card to the feed."""
        timestamp = datetime.now().strftime("%I:%M %p")
        
        # Status colors
        status_colors = {
            "success": "#10b981",
            "processing": "#f59e0b",
            "info": "#0ea5e9",
            "error": "#ef4444",
        }
        status_color = status_colors.get(status, self.palette["text_soft"][0])
        
        # Card with modern design
        card = ctk.CTkFrame(
            self.response_feed,
            corner_radius=16,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        
        # Header with icon and status
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=16, pady=(14, 8))
        
        # Status icon
        status_icons = {
            "success": "✅",
            "processing": "⏳",
            "info": "ℹ️",
            "error": "❌",
        }
        icon = status_icons.get(status, "•")
        
        ctk.CTkLabel(
            card_header,
            text=f"{icon} {summary}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.palette["text"],
        ).pack(side="left")
        
        ctk.CTkLabel(
            card_header,
            text=timestamp,
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
        ).pack(side="right")
        
        # Body text
        body_text = ctk.CTkTextbox(
            card,
            height=80,
            corner_radius=8,
            fg_color=self.palette["surface"],
            text_color=self.palette["text"],
            font=ctk.CTkFont(size=12),
            wrap="word",
        )
        body_text.pack(fill="x", padx=16, pady=(0, 12))
        body_text.insert("1.0", body)
        body_text.configure(state="disabled")
        
        # Footer with metadata
        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=(0, 14))
        
        ctk.CTkLabel(
            footer,
            text=f"Mode: {mode}",
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
        ).pack(side="left")
        
        ctk.CTkLabel(
            footer,
            text=f"● {status.capitalize()}",
            font=ctk.CTkFont(size=10),
            text_color=status_color,
        ).pack(side="left", padx=12)
        
        ctk.CTkLabel(
            footer,
            text=f"⏱️ {duration}",
            font=ctk.CTkFont(size=10),
            text_color=self.palette["text_soft"],
        ).pack(side="left")
        
        # Action buttons
        action_frame = ctk.CTkFrame(footer, fg_color="transparent")
        action_frame.pack(side="right")
        
        for text, icon in [("Copy", "📋"), ("Save", "💾")]:
            btn = ctk.CTkButton(
                action_frame,
                text=f"{icon} {text}",
                width=70,
                height=28,
                corner_radius=8,
                font=ctk.CTkFont(size=10),
                fg_color=self.palette["surface"],
                hover_color=self.palette["surface_subtle"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            btn.pack(side="left", padx=4)
        
        # Add card to feed
        if self.response_cards:
            try:
                card.pack(fill="x", padx=4, pady=6, before=self.response_cards[0])
            except:
                card.pack(fill="x", padx=4, pady=6)
        else:
            card.pack(fill="x", padx=4, pady=6)
        
        self.response_cards.insert(0, card)
        self.response_timestamp.configure(text=f"Last updated: {timestamp}")
    
    def get_command(self) -> str:
        """Get the current command text."""
        return self.command_entry.get()
    
    def clear_command(self):
        """Clear the command input."""
        self.command_entry.delete(0, "end")
    
    def update_mode(self, mode: str):
        """Update the current mode."""
        self.current_mode = mode
        self.mode_selector.set(mode)
        
        # Update colors
        color = MODE_COLORS[mode]
        self.execute_btn.configure(fg_color=color, hover_color=shade_color(color, -0.2))
        
        for btn in self.quick_buttons:
            btn.configure(fg_color=color, hover_color=shade_color(color, -0.2))
        
        # Update examples
        examples = MODE_EXAMPLES.get(mode, [])
        self.examples_menu.configure(values=examples if examples else ["No examples"])
        self.examples_menu.set("Choose an example ▾")
