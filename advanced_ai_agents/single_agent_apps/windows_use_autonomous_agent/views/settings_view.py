"""Professional application settings view."""

import customtkinter as ctk
from typing import Dict


class SettingsView(ctk.CTkFrame):
    """Modern settings with organized tabs."""
    
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
        """Build the professional settings UI."""
        # Header
        header = self._build_header()
        header.pack(fill="x", padx=24, pady=(24, 20))
        
        # Tabbed settings
        tabs = self._build_tabs()
        tabs.pack(fill="both", expand=True, padx=24, pady=(0, 24))
    
    def _build_header(self) -> ctk.CTkFrame:
        """Build the settings header."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(
            header,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            header,
            text="Configure application preferences",
            font=ctk.CTkFont(size=13),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(4, 0))
        
        return header
    
    def _build_tabs(self) -> ctk.CTkTabview:
        """Build the settings tabs."""
        tabview = ctk.CTkTabview(
            self,
            corner_radius=20,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        
        # Create tabs
        general_tab = tabview.add("🎨 General")
        ai_tab = tabview.add("🤖 AI Model")
        voice_tab = tabview.add("🎤 Voice")
        advanced_tab = tabview.add("⚡ Advanced")
        
        # Build tab content
        self._build_general_tab(general_tab)
        self._build_ai_tab(ai_tab)
        self._build_voice_tab(voice_tab)
        self._build_advanced_tab(advanced_tab)
        
        return tabview
    
    def _build_general_tab(self, parent):
        """Build general settings tab."""
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Theme setting
        self._add_setting_row(
            scroll,
            "🌓 Theme",
            "Choose your preferred color scheme",
            ctk.CTkSegmentedButton(
                scroll,
                values=["Light", "Dark", "System"],
                command=self.controller.on_theme_change,
            )
        )
        
        # Language setting
        self._add_setting_row(
            scroll,
            "🌍 Language",
            "Select application language",
            ctk.CTkOptionMenu(
                scroll,
                values=["English", "Spanish", "French", "German"],
                width=200,
            )
        )
        
        # Notifications
        self._add_setting_row(
            scroll,
            "🔔 Notifications",
            "Show desktop notifications",
            ctk.CTkSwitch(scroll, text="")
        )
        
        # Auto-start
        self._add_setting_row(
            scroll,
            "🚀 Launch at Startup",
            "Start app when Windows boots",
            ctk.CTkSwitch(scroll, text="")
        )
    
    def _build_ai_tab(self, parent):
        """Build AI model settings tab."""
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Model selection
        self._add_setting_row(
            scroll,
            "🤖 AI Model",
            "Choose the AI model for command processing",
            ctk.CTkOptionMenu(
                scroll,
                values=["GPT-4", "GPT-3.5", "Gemini Pro", "Claude"],
                width=200,
            )
        )
        
        # API Key
        self._add_setting_row(
            scroll,
            "🔑 API Key",
            "Your OpenAI/Gemini API key",
            ctk.CTkEntry(scroll, width=300, show="*")
        )
        
        # Temperature
        self._add_setting_row(
            scroll,
            "🌡️ Temperature",
            "Control AI creativity (0.0 - 1.0)",
            ctk.CTkSlider(scroll, from_=0, to=1, number_of_steps=10)
        )
        
        # Max tokens
        self._add_setting_row(
            scroll,
            "📝 Max Tokens",
            "Maximum response length",
            ctk.CTkEntry(scroll, width=150, placeholder_text="2048")
        )
    
    def _build_voice_tab(self, parent):
        """Build voice settings tab."""
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Voice input
        self._add_setting_row(
            scroll,
            "🎤 Voice Input",
            "Enable voice commands",
            ctk.CTkSwitch(scroll, text="")
        )
        
        # Microphone
        self._add_setting_row(
            scroll,
            "🎙️ Microphone",
            "Select audio input device",
            ctk.CTkOptionMenu(
                scroll,
                values=["Default", "Microphone 1", "Microphone 2"],
                width=200,
            )
        )
        
        # Voice feedback
        self._add_setting_row(
            scroll,
            "🔊 Voice Feedback",
            "Speak responses aloud",
            ctk.CTkSwitch(scroll, text="")
        )
        
        # Wake word
        self._add_setting_row(
            scroll,
            "👂 Wake Word",
            "Custom activation phrase",
            ctk.CTkEntry(scroll, width=200, placeholder_text="Hey Assistant")
        )
    
    def _build_advanced_tab(self, parent):
        """Build advanced settings tab."""
        scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Debug mode
        self._add_setting_row(
            scroll,
            "🐛 Debug Mode",
            "Enable detailed logging",
            ctk.CTkSwitch(scroll, text="")
        )
        
        # Cache
        self._add_setting_row(
            scroll,
            "💾 Cache Size",
            "Maximum cache storage",
            ctk.CTkOptionMenu(
                scroll,
                values=["50 MB", "100 MB", "500 MB", "1 GB"],
                width=150,
            )
        )
        
        # Analytics
        self._add_setting_row(
            scroll,
            "📊 Anonymous Analytics",
            "Help improve the app",
            ctk.CTkSwitch(scroll, text="")
        )
        
        # Export/Import
        export_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        export_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            export_frame,
            text="📤 Export Settings",
            width=150,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=12),
            fg_color=self.palette["surface_alt"],
            hover_color=self.palette["surface_subtle"],
            border_width=1,
            border_color=self.palette["stroke"],
            text_color=self.palette["text"],
        ).pack(side="left", padx=6)
        
        ctk.CTkButton(
            export_frame,
            text="📥 Import Settings",
            width=150,
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=12),
            fg_color=self.palette["surface_alt"],
            hover_color=self.palette["surface_subtle"],
            border_width=1,
            border_color=self.palette["stroke"],
            text_color=self.palette["text"],
        ).pack(side="left", padx=6)
        
        # Reset button
        ctk.CTkButton(
            scroll,
            text="🔄 Reset to Defaults",
            height=40,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.controller.on_reset_settings,
        ).pack(pady=20)
    
    def _add_setting_row(self, parent, title: str, description: str, widget):
        """Add a setting row with title, description, and widget."""
        row = ctk.CTkFrame(
            parent,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        row.pack(fill="x", pady=8)
        
        content = ctk.CTkFrame(row, fg_color="transparent")
        content.pack(fill="x", padx=16, pady=14)
        
        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.palette["text"],
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", pady=(2, 0))
        
        widget.pack(side="right", padx=(12, 0))
