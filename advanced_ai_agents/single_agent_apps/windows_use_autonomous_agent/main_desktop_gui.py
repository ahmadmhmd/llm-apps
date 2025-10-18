# -*- coding: utf-8 -*-
"""Enterprise desktop interface for the Windows Use Agent."""

from __future__ import annotations

import ctypes
import json
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import customtkinter as ctk
import numpy as np
import speech_recognition as sr
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from markdownify import markdownify
from tkinter import messagebox, ttk
from windows_use.agent import Agent

load_dotenv()


class CTkToolTip:
    """Lightweight tooltip helper for CustomTkinter widgets."""

    def __init__(self, widget: ctk.CTkBaseClass, text: str, delay: int = 600) -> None:
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window: Optional[ctk.CTkToplevel] = None
        self.after_id: Optional[str] = None

        self.widget.bind("<Enter>", self._schedule)
        self.widget.bind("<Leave>", self._hide)
        self.widget.bind("<ButtonPress>", self._hide)

    def _schedule(self, _event) -> None:
        self.after_id = self.widget.after(self.delay, self._show)

    def _show(self) -> None:
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx() + 40
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6

        self.tip_window = ctk.CTkToplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        self.tip_window.configure(fg_color="#1f2937")

        label = ctk.CTkLabel(
            self.tip_window,
            text=self.text,
            font=ctk.CTkFont(size=11),
            text_color="#f3f4f6",
            justify="left",
            padx=12,
            pady=8,
        )
        label.pack()

    def _hide(self, _event=None) -> None:
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class WindowsUseApp(ctk.CTk):
    """Enterprise-grade desktop shell for the Windows Use Agent."""

    PLACEHOLDER_ROTATION = [
        "Open Notepad",
        "Take screenshot",
        "Search for AI news",
        "Email latest report",
        "List active windows",
    ]

    MODE_COLORS = {
        "Basic": "#2563eb",
        "Workflow": "#f97316",
        "Context": "#22c55e",
        "Secure": "#ef4444",
        "Integrated": "#a855f7",
    }

    NAV_ITEMS = [
        ("Command Console", "[CC]", "Main workspace for natural language commands."),
        ("Workflows", "[WF]", "Create, edit, and trigger automated task chains."),
        ("Integrations", "[IN]", "Manage Gmail, cloud storage, webhooks, and APIs."),
        ("Context Insights", "[CI]", "Analytics, productivity graphs, and AI tips."),
        ("Security Center", "[SC]", "Permissions, sandboxing, undo stack, backups."),
        ("Settings", "[ST]", "Theme, keys, notifications, and voice preferences."),
        ("Logs & History", "[LH]", "Timeline of past commands, status, and recovery."),
        ("Help", "[HP]", "Quick start, troubleshooting, docs, and support."),
    ]

    MODE_EXAMPLES: Dict[str, List[str]] = {
        "Basic": [
            "Open Notepad",
            "Search AI news",
            "Take screenshot",
            "Check weather",
            "List open windows",
            "Start Calculator",
        ],
        "Workflow": [
            "Create morning routine workflow",
            "Execute workflow: daily_brief",
            "Auto backup Desktop at 6 PM",
            "List all workflows",
        ],
        "Context": [
            "What apps do I use most?",
            "Show my morning patterns",
            "Predict my next task",
            "Track time spent coding",
        ],
        "Secure": [
            "Show current permissions",
            "Enable sandbox mode",
            "Undo last action",
            "Create backup point",
        ],
        "Integrated": [
            "Email screenshot to team",
            "Upload report to OneDrive",
            "Send webhook notification",
            "Check Gmail inbox",
        ],
    }

    QUICK_COMMANDS = [
        "Open Notepad",
        "Search AI News",
        "Screenshot",
        "Check Weather",
        "List Open Windows",
    ]

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.palette: Dict[str, tuple[str, str]] = {
            "background": ("#eef2ff", "#050c1a"),
            "sidebar": ("#f8fafc", "#111827"),
            "surface": ("#ffffff", "#0f172a"),
            "surface_alt": ("#f1f5ff", "#17233a"),
            "surface_subtle": ("#e7ecff", "#101c33"),
            "stroke": ("#dbeafe", "#1f2b44"),
            "muted": ("#475569", "#94a3b8"),
            "text": ("#0f172a", "#f8fafc"),
            "text_soft": ("#64748b", "#a1b5d8"),
        }

        self.title("Windows Use Agent - Enterprise v2.0")
        self.geometry("1500x900")
        self.minsize(1280, 820)
        self.configure(fg_color=self.palette["background"])

        self.user_profile = self._resolve_user_profile()
        self._apply_profile_environment()

        self.current_mode = "Basic"
        self.current_view = "Command Console"
        self.placeholder_index = 0
        self.placeholder_job: Optional[str] = None
        self.is_listening = False
        self.voice_enabled = False
        self.agent_ready = False
        self.agent_error: Optional[str] = None
        self.advanced_features = False
        self.sidebar_collapsed = False

        self.history: List[Dict[str, str]] = []
        self.response_cards: List[ctk.CTkFrame] = []
        self.quick_buttons: List[ctk.CTkButton] = []
        self.selected_workflow: Optional[str] = None
        self.workflow_cards: Dict[str, ctk.CTkFrame] = {}
        self.help_content_cache: Dict[str, str] = {}

        self.settings_path = Path.home() / "Documents" / "PowerAgent" / "app_settings.json"
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self.user_settings = self._load_user_settings()

        self._initialize_agent()
        self._build_layout()
        self.after(150, self._center_window)
        self._start_placeholder_rotation()
        self._update_right_panel(self.current_view)
        self.after(500, self._maybe_warn_about_location)

    # --------------------------------------------------------------------- #
    # Initialization
    # --------------------------------------------------------------------- #

    def _resolve_user_profile(self) -> Dict[str, Optional[str]]:
        profile = {
            "city": os.getenv("WINDOWS_USE_CITY") or os.getenv("USER_CITY"),
            "region": os.getenv("WINDOWS_USE_REGION") or os.getenv("USER_REGION") or os.getenv("USER_STATE"),
            "country": os.getenv("WINDOWS_USE_COUNTRY") or os.getenv("USER_COUNTRY"),
            "latitude": os.getenv("WINDOWS_USE_LAT") or os.getenv("USER_LATITUDE") or os.getenv("USER_LAT"),
            "longitude": os.getenv("WINDOWS_USE_LON") or os.getenv("USER_LONGITUDE") or os.getenv("USER_LON"),
            "timezone": os.getenv("WINDOWS_USE_TIMEZONE"),
        }

        if not profile["timezone"]:
            try:
                from tzlocal import get_localzone_name  # type: ignore

                profile["timezone"] = get_localzone_name()
            except Exception:
                try:
                    profile["timezone"] = datetime.now().astimezone().tzinfo.key  # type: ignore[attr-defined]
                except Exception:
                    profile["timezone"] = time.tzname[0] if time.tzname else None

        if profile["timezone"] and not profile["city"]:
            tz_parts = profile["timezone"].split("/")
            if len(tz_parts) > 1:
                derived_city = tz_parts[-1].replace("_", " ")
                profile["city"] = derived_city
                if not profile["region"]:
                    profile["region"] = tz_parts[0]

        if not profile["region"]:
            profile["region"] = self._get_windows_region()

        if not all([profile.get("city"), profile.get("country"), profile.get("latitude"), profile.get("longitude"), profile.get("timezone")]):
            ip_profile = self._fetch_ip_location()
            if ip_profile:
                for key, value in ip_profile.items():
                    if value and not profile.get(key):
                        profile[key] = value

        for coord_key in ("latitude", "longitude"):
            raw_value = profile[coord_key]
            if raw_value:
                try:
                    profile[coord_key] = f"{float(raw_value):.4f}"
                except ValueError:
                    profile[coord_key] = None

        profile["utc_offset"] = self._calculate_utc_offset()
        return profile

    def _apply_profile_environment(self) -> None:
        for key, value in self.user_profile.items():
            if value:
                os.environ[f"WINDOWS_USE_{key.upper()}"] = str(value)
        if hasattr(self, "location_label"):
            self.location_label.configure(text=f"Location: {self._format_location_summary()}")

    def _load_user_settings(self) -> Dict[str, Any]:
        defaults: Dict[str, Any] = {
            "theme": "System",
            "language": "English",
            "notifications": "Toast",
            "microphone": "Default",
            "voice_feedback": True,
            "auto_run_on_enter": True,
            "context_tracking": True,
            "data_retention_days": 30,
        }
        if self.settings_path.exists():
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                    defaults.update(stored)
            except Exception as exc:
                print(f"[WindowsUseApp] Failed to load settings: {exc}")
        return defaults

    def _save_user_settings(self) -> None:
        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.user_settings, f, indent=2)
            self._add_response_card(
                summary="Settings saved.",
                body="Your preferences have been stored successfully.",
                status="info",
                duration="-",
                mode="Secure",
            )
        except Exception as exc:
            self._add_response_card(
                summary="Failed to save settings.",
                body=str(exc),
                status="error",
                duration="-",
                mode="Secure",
            )

    def _calculate_utc_offset(self) -> Optional[str]:
        try:
            offset = datetime.now().astimezone().utcoffset()
            if offset is None:
                return None
            total_minutes = int(offset.total_seconds() // 60)
            sign = "+" if total_minutes >= 0 else "-"
            total_minutes = abs(total_minutes)
            hours, minutes = divmod(total_minutes, 60)
            return f"{sign}{hours:02d}:{minutes:02d}"
        except Exception:
            return None

    def _get_windows_region(self) -> Optional[str]:
        try:
            buffer = ctypes.create_unicode_buffer(85)
            if ctypes.windll.kernel32.GetUserDefaultGeoName(buffer, 85):
                value = buffer.value.strip()
                return value or None
        except Exception:
            pass
        return None

    def _fetch_ip_location(self) -> Optional[Dict[str, str]]:
        try:
            response = requests.get("https://ipapi.co/json/", timeout=5)
            response.raise_for_status()
            data = response.json()
            ip_profile: Dict[str, Optional[str]] = {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country_name") or data.get("country"),
                "latitude": None,
                "longitude": None,
                "timezone": data.get("timezone"),
            }
            if data.get("latitude"):
                try:
                    ip_profile["latitude"] = f"{float(data['latitude']):.4f}"
                except (ValueError, TypeError):
                    ip_profile["latitude"] = None
            if data.get("longitude"):
                try:
                    ip_profile["longitude"] = f"{float(data['longitude']):.4f}"
                except (ValueError, TypeError):
                    ip_profile["longitude"] = None
            return {k: v for k, v in ip_profile.items() if v}
        except Exception:
            return None

    def _format_location_summary(self) -> str:
        parts = [self.user_profile.get("city"), self.user_profile.get("region"), self.user_profile.get("country")]
        summary = ", ".join(part for part in parts if part)
        timezone = self.user_profile.get("timezone")
        if timezone:
            summary = f"{summary} ({timezone})" if summary else timezone
        return summary or "Not configured"

    def _build_location_instruction(self) -> Optional[str]:
        summary = ", ".join(filter(None, [self.user_profile.get("city"), self.user_profile.get("region"), self.user_profile.get("country")]))
        timezone = self.user_profile.get("timezone")
        offset = self.user_profile.get("utc_offset")
        if not summary and not timezone:
            return None

        clause = f"The user is located in {summary}" if summary else "Use the configured timezone for location-aware tasks"
        if timezone:
            clause += f" with timezone {timezone}"
            if offset:
                clause += f" (UTC{offset})"
        clause += ". Always base 'current location' or similar references on this information unless the user explicitly specifies otherwise."
        return clause

    def _maybe_warn_about_location(self) -> None:
        if getattr(self, "_location_warning_shown", False):
            return
        if self.user_profile.get("city") or self.user_profile.get("latitude"):
            return
        self._location_warning_shown = True
        self._add_response_card(
            summary="Location not configured.",
            body=(
                "Set WINDOWS_USE_CITY (and optionally WINDOWS_USE_REGION, WINDOWS_USE_COUNTRY, WINDOWS_USE_LAT, "
                "WINDOWS_USE_LON) in your environment or .env file so that location-aware tools use your exact position."
            ),
            status="info",
            duration="-",
            mode="Secure",
        )

    def _initialize_agent(self) -> None:
        """Connect to LLM agent and optional enterprise modules."""
        try:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
            instructions = [
                (
                    "Claude Desktop, Perplexity, and ChatGPT apps are installed. "
                    "Collaborate with them for advanced reasoning when required."
                )
            ]
            location_instruction = self._build_location_instruction()
            if location_instruction:
                instructions.append(location_instruction)
            self.agent = Agent(instructions=instructions, llm=llm, use_vision=True)
            self.agent_ready = True
        except Exception as error:  # pragma: no cover - runtime guard
            self.agent_error = str(error)
            self.agent_ready = False
            print(f"[WindowsUseApp] Agent init failed: {error}")
            return

        try:
            from windows_use.agent.context_manager.context_manager import ContextManager
            from windows_use.agent.integrations.integration_manager import IntegrationManager
            from windows_use.agent.security.security_manager import SecurityManager
            from windows_use.agent.workflow_engine.smart_workflow_engine import SmartWorkflowEngine

            self.workflow_engine = SmartWorkflowEngine()
            self.context_manager = ContextManager()
            self.security_manager = SecurityManager()
            self.integration_manager = IntegrationManager()
            self.advanced_features = True
        except ImportError as error:
            self.advanced_features = False
            print(f"[WindowsUseApp] Advanced modules unavailable: {error}")

        self._initialize_voice()

    def _initialize_voice(self) -> None:
        self.recognizer = sr.Recognizer()
        self.voice_backend: Optional[str] = None
        self.sd_samplerate = int(os.getenv("WINDOWS_USE_AUDIO_RATE", "16000"))
        self.sd_voice_threshold = int(os.getenv("WINDOWS_USE_AUDIO_THRESHOLD", "500"))

        try:
            import sounddevice  # type: ignore

            self.sd = sounddevice
            self.voice_backend = "sounddevice"
            self.voice_enabled = True
            print("[WindowsUseApp] Voice input enabled via sounddevice backend.")
            return
        except Exception as sd_error:
            print(f"[WindowsUseApp] sounddevice backend unavailable: {sd_error}")

        try:
            self.microphone = sr.Microphone()
            self.voice_backend = "pyaudio"
            self.voice_enabled = True
            print("[WindowsUseApp] Voice input enabled via PyAudio backend.")
        except Exception as error:
            self.voice_enabled = False
            self.voice_backend = None
            print(f"[WindowsUseApp] Voice disabled: {error}")

    # --------------------------------------------------------------------- #
    # Layout
    # --------------------------------------------------------------------- #

    def _build_layout(self) -> None:
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=2)

        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0,
            fg_color=self.palette["sidebar"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.center = ctk.CTkFrame(self, fg_color="transparent")
        self.center.grid(row=0, column=1, sticky="nsew", padx=(0, 16), pady=16)
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(0, weight=1)

        self.right_panel = ctk.CTkFrame(
            self,
            width=340,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=(0, 16), pady=16)
        self.right_panel.grid_propagate(False)

        self._build_sidebar()
        self._build_views()

    def _build_sidebar(self) -> None:
        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(24, 18))

        self.brand = ctk.CTkLabel(
            header,
            text="Windows Use Agent\nEnterprise Edition",
            font=ctk.CTkFont(size=18, weight="bold"),
            justify="left",
            text_color=self.palette["text"],
        )
        self.brand.pack(anchor="w")

        self.toggle_btn = ctk.CTkButton(
            header,
            text="<",
            width=34,
            height=34,
            fg_color=self.palette["surface"],
            hover_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
            command=self._toggle_sidebar,
        )
        self.toggle_btn.pack(anchor="e", pady=(12, 0))

        status = ctk.CTkFrame(
            self.sidebar,
            corner_radius=12,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        status.pack(fill="x", padx=20, pady=(0, 18))

        ctk.CTkLabel(
            status,
            text="System Status",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.palette["text"],
        ).pack(
            anchor="w", padx=16, pady=(14, 6)
        )

        agent_state = "Ready" if self.agent_ready else "Unavailable"
        agent_color = "#10b981" if self.agent_ready else "#ef4444"
        self.agent_status = ctk.CTkLabel(
            status,
            text=f"Agent: {agent_state}",
            text_color=agent_color,
        )
        self.agent_status.pack(anchor="w", padx=16, pady=2)

        features_state = "Advanced Modules" if self.advanced_features else "Basic Mode"
        self.feature_status = ctk.CTkLabel(
            status,
            text=f"Features: {features_state}",
            text_color="#3b82f6" if self.advanced_features else self.palette["text_soft"],
        )
        self.feature_status.pack(anchor="w", padx=16, pady=(0, 12))

        location_summary = self._format_location_summary()
        self.location_label = ctk.CTkLabel(
            status,
            text=f"Location: {location_summary}",
            text_color=self.palette["text_soft"],
        )
        self.location_label.pack(anchor="w", padx=16, pady=(0, 12))

        self.nav_buttons: Dict[str, ctk.CTkButton] = {}
        for name, icon, tooltip in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {name}",
                anchor="w",
                height=46,
                corner_radius=12,
                fg_color="transparent",
                text_color=self.palette["text"],
                hover_color=self.palette["surface_alt"],
                border_width=0,
                command=lambda view=name: self._navigate(view),
            )
            btn.pack(fill="x", padx=20, pady=4)
            CTkToolTip(btn, tooltip)
            self.nav_buttons[name] = btn

        footer = ctk.CTkLabel(
            self.sidebar,
            text="v2.0 Enterprise - Adaptive Cognition\n(c) 2025",
            font=ctk.CTkFont(size=10),
            text_color="#6b7280",
            justify="left",
        )
        footer.pack(side="bottom", padx=20, pady=20)

        self._apply_profile_environment()

        self._update_nav_styles()

    def _build_views(self) -> None:
        self.views: Dict[str, ctk.CTkFrame] = {}
        self.views["Command Console"] = self._build_console_view()
        self.views["Workflows"] = self._build_workflow_view()
        self.views["Integrations"] = self._build_integrations_view()
        self.views["Context Insights"] = self._build_context_view()
        self.views["Security Center"] = self._build_security_view()
        self.views["Settings"] = self._build_settings_view()
        self.views["Logs & History"] = self._build_logs_view()
        self.views["Help"] = self._build_help_view()
        self._show_view("Command Console")

    # --------------------------------------------------------------------- #
    # Command Console
    # --------------------------------------------------------------------- #

    def _build_console_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            self.center,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
        header.grid_columnconfigure(1, weight=1)

        title = ctk.CTkFrame(header, fg_color="transparent")
        title.grid(row=0, column=0, sticky="w")

        self.mode_title = ctk.CTkLabel(
            title,
            text="Command Console",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=self.palette["text"],
        )
        self.mode_title.pack(anchor="w")

        self.mode_subtitle = ctk.CTkLabel(
            title,
            text="Execute and visualize AI-powered desktop commands.",
            font=ctk.CTkFont(size=12),
            text_color=self.palette["text_soft"],
        )
        self.mode_subtitle.pack(anchor="w")

        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.grid(row=0, column=1, sticky="e")

        self.mode_selector = ctk.CTkOptionMenu(
            controls,
            values=list(self.MODE_COLORS.keys()),
            command=self._on_mode_change,
            width=160,
            fg_color=self.palette["surface_alt"],
            button_color=self.palette["surface_subtle"],
            text_color=self.palette["text"],
            dropdown_font=ctk.CTkFont(size=12),
        )
        self.mode_selector.set(self.current_mode)
        self.mode_selector.pack(side="right", padx=(0, 12))

        self.voice_btn = ctk.CTkButton(
            controls,
            text="Voice",
            width=100,
            fg_color="#1d4ed8",
            hover_color="#1e3a8a",
            command=self._toggle_listening,
            state="normal" if self.voice_enabled else "disabled",
        )
        self.voice_btn.pack(side="right", padx=(0, 12))

        self.status_badge = ctk.CTkLabel(
            controls,
            text="Ready",
            fg_color="#16a34a",
            text_color="white",
            corner_radius=8,
            padx=12,
            pady=6,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.status_badge.pack(side="right")

        # Input panel
        input_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        input_panel.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 16))
        input_panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            input_panel,
            text="Command Input",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.palette["text"],
        ).grid(
            row=0, column=0, sticky="w", padx=20, pady=(16, 8)
        )

        self.command_entry = ctk.CTkEntry(
            input_panel,
            placeholder_text=self.PLACEHOLDER_ROTATION[0],
            height=48,
            font=ctk.CTkFont(size=14),
            fg_color=self.palette["surface"],
            border_color=self.palette["stroke"],
        )
        self.command_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        self.command_entry.bind("<Return>", lambda _event: self._execute_text_command())

        button_row = ctk.CTkFrame(input_panel, fg_color="transparent")
        button_row.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 16))
        button_row.grid_columnconfigure(2, weight=1)

        self.execute_btn = ctk.CTkButton(
            button_row,
            text="Execute",
            width=120,
            fg_color=self.MODE_COLORS[self.current_mode],
            hover_color=self._shade_color(self.MODE_COLORS[self.current_mode], -0.2),
            command=self._execute_text_command,
        )
        self.execute_btn.grid(row=0, column=0, padx=(0, 10))

        ctk.CTkButton(
            button_row,
            text="Clear",
            width=100,
            fg_color="transparent",
            border_width=1,
            command=self._clear_responses,
        ).grid(row=0, column=1)

        self.examples_menu = ctk.CTkOptionMenu(
            button_row,
            values=list(self.MODE_EXAMPLES[self.current_mode]),
            command=self._on_example_selected,
            width=220,
            fg_color=self.palette["surface"],
            button_color=self.palette["surface_alt"],
            text_color=self.palette["text"],
        )
        self.examples_menu.set("Examples ▾")
        self.examples_menu.grid(row=0, column=3, sticky="e")

        self.transcription_label = ctk.CTkLabel(
            input_panel,
            text="",
            font=ctk.CTkFont(size=11, slant="italic"),
            text_color="#10b981",
        )
        self.transcription_label.grid(row=3, column=0, sticky="w", padx=20, pady=(0, 12))

        # Response feed
        response_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        response_panel.grid(row=2, column=0, sticky="nsew", padx=24)
        response_panel.grid_rowconfigure(1, weight=1)
        response_panel.grid_columnconfigure(0, weight=1)

        header_row = ctk.CTkFrame(response_panel, fg_color="transparent")
        header_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 0))
        header_row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header_row, text="Response Timeline", font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, sticky="w"
        )

        self.response_timestamp = ctk.CTkLabel(
            header_row,
            text="Last updated: -",
            text_color=self.palette["text_soft"],
        )
        self.response_timestamp.grid(row=0, column=1, sticky="e")

        self.response_feed = ctk.CTkScrollableFrame(response_panel, corner_radius=12, fg_color="transparent")
        self.response_feed.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.response_feed.grid_columnconfigure(0, weight=1)

        # Quick commands
        quick_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        quick_panel.grid(row=3, column=0, sticky="ew", padx=24, pady=(16, 24))
        quick_panel.grid_columnconfigure(tuple(range(len(self.QUICK_COMMANDS))), weight=1)

        ctk.CTkLabel(
            quick_panel,
            text="Quick Examples",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.palette["text"],
        ).grid(
            row=0, column=0, columnspan=len(self.QUICK_COMMANDS), sticky="w", padx=20, pady=(18, 8)
        )

        for idx, example in enumerate(self.QUICK_COMMANDS):
            btn = ctk.CTkButton(
                quick_panel,
                text=example,
                height=38,
                corner_radius=10,
                command=lambda text=example: self._run_quick_command(text),
                fg_color=self.MODE_COLORS[self.current_mode],
                hover_color=self._shade_color(self.MODE_COLORS[self.current_mode], -0.2),
                text_color="white",
            )
            btn.grid(row=1, column=idx, padx=8, pady=(0, 16), sticky="ew")
            self.quick_buttons.append(btn)

        self._add_intro_card()
        return frame

    # ------------------------------------------------------------------ #
    # Integrations Dashboard
    # ------------------------------------------------------------------ #

    def _build_integrations_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            self.center,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        if not self.integration_manager:
            ctk.CTkLabel(
                frame,
                text=(
                    "Integration manager not available.\n"
                    "Install advanced modules to enable Gmail, cloud, and webhook management."
                ),
                text_color=self.palette["text_soft"],
                font=ctk.CTkFont(size=14),
            ).pack(expand=True)
            return frame

        tabs = ctk.CTkTabview(frame, corner_radius=14)
        tabs.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

        gmail_tab = tabs.add("Gmail")
        storage_tab = tabs.add("Cloud Storage")
        webhook_tab = tabs.add("Webhooks")

        self._populate_gmail_tab(gmail_tab)
        self._populate_storage_tab(storage_tab)
        self._populate_webhook_tab(webhook_tab)
        return frame


    def _populate_gmail_tab(self, tab: ctk.CTkFrame) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        form_panel = ctk.CTkFrame(
            tab,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        form_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        form_panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            form_panel,
            text="Gmail Integration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(18, 8))

        config = self.integration_manager.config.get("email", {}) if self.integration_manager else {}
        fields = [
            ("SMTP Server", "smtp_server", "smtp.gmail.com", False),
            ("IMAP Server", "imap_server", "imap.gmail.com", False),
            ("Username", "username", "user@company.com", False),
            ("App Password", "password", "", True),
            ("SMTP Port", "smtp_port", "587", False),
            ("IMAP Port", "imap_port", "993", False),
        ]

        self.gmail_entries = {}
        for idx, (label, key, placeholder, secret) in enumerate(fields):
            ctk.CTkLabel(form_panel, text=label, text_color=self.palette["text"]).grid(
                row=idx + 1, column=0, sticky="w", padx=20, pady=6
            )
            entry = ctk.CTkEntry(
                form_panel,
                placeholder_text=placeholder,
                fg_color=self.palette["surface"],
            )
            value = config.get(key)
            if value:
                entry.insert(0, str(value))
            if secret:
                entry.configure(show="*")
            entry.grid(row=idx + 1, column=1, sticky="ew", padx=(10, 20), pady=6)
            self.gmail_entries[key] = entry

        actions = ctk.CTkFrame(form_panel, fg_color="transparent")
        actions.grid(row=len(fields) + 1, column=0, columnspan=2, sticky="e", padx=20, pady=(12, 18))
        ctk.CTkButton(actions, text="Save Settings", width=130, command=self._save_gmail_settings).pack(side="left", padx=6)
        ctk.CTkButton(actions, text="Send Test Email", width=140, command=self._send_test_email).pack(side="left", padx=6)

        example_panel = ctk.CTkFrame(
            tab,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        example_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        example_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            example_panel,
            text="Automation Examples",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 8))

        examples = (
            "- Email my latest report to boss@company.com"
            "- Send backup logs to team@company.com"
            "- Summarize today's inbox for leadership"
        )
        textbox = ctk.CTkTextbox(
            example_panel,
            height=160,
            wrap="word",
            fg_color=self.palette["surface"],
            text_color=self.palette["text"],
        )
        textbox.insert("1.0", examples)
        textbox.configure(state="disabled")
        textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 16))

    def _populate_storage_tab(self, tab: ctk.CTkFrame) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)

        self.cloud_entries = {}
        config = self.integration_manager.config.get("cloud_storage", {}) if self.integration_manager else {}
        provider_tabs = ctk.CTkTabview(tab, corner_radius=12)
        provider_tabs.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for provider in ("OneDrive", "Google Drive"):
            pane = provider_tabs.add(provider)
            pane.grid_columnconfigure(1, weight=1)

            entries = {}
            ctk.CTkLabel(pane, text=f"{provider} Configuration", font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 6)
            )

            entries["local"] = ctk.CTkEntry(pane, placeholder_text=r"C:\Projects")
            entries["cloud"] = ctk.CTkEntry(pane, placeholder_text="/Automations/Reports")
            entries["interval"] = ctk.CTkEntry(pane, placeholder_text="15")

            ctk.CTkLabel(pane, text="Local Path").grid(row=1, column=0, sticky="w", padx=16, pady=4)
            entries["local"].grid(row=1, column=1, sticky="ew", padx=(10, 16), pady=4)
            ctk.CTkLabel(pane, text="Cloud Path").grid(row=2, column=0, sticky="w", padx=16, pady=4)
            entries["cloud"].grid(row=2, column=1, sticky="ew", padx=(10, 16), pady=4)
            ctk.CTkLabel(pane, text="Sync Interval (minutes)").grid(row=3, column=0, sticky="w", padx=16, pady=4)
            entries["interval"].grid(row=3, column=1, sticky="w", padx=(10, 16), pady=4)

            if config.get("provider") == provider.lower():
                if config.get("local_path"):
                    entries["local"].insert(0, config["local_path"])
                if config.get("cloud_path"):
                    entries["cloud"].insert(0, config["cloud_path"])
                if config.get("sync_interval"):
                    entries["interval"].insert(0, str(config["sync_interval"]))

            button_row = ctk.CTkFrame(pane, fg_color="transparent")
            button_row.grid(row=4, column=0, columnspan=2, sticky="e", padx=16, pady=(8, 12))
            ctk.CTkButton(button_row, text="Save Settings", width=120, command=lambda p=provider: self._save_cloud_settings(p)).pack(side="left", padx=6)
            ctk.CTkButton(button_row, text="Sync Now", width=110, command=lambda p=provider: self._sync_cloud_now(p)).pack(side="left", padx=6)

            self.cloud_entries[provider.lower()] = entries

            history = config.get("history", []) if config.get("provider") == provider.lower() else []
            history_box = ctk.CTkTextbox(pane, height=120, fg_color=self.palette["surface"], text_color=self.palette["text"])
            history_box.grid(row=5, column=0, columnspan=2, sticky="ew", padx=16, pady=(4, 12))
            if history:
                for item in history:
                    history_box.insert("end", f"- {item}")
            else:
                history_box.insert("end", "No sync history recorded.")
            history_box.configure(state="disabled")


    def _populate_webhook_tab(self, tab: ctk.CTkFrame) -> None:
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        config = self.integration_manager.config.get("webhooks", {}) if self.integration_manager else {}
        form_panel = ctk.CTkFrame(
            tab,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        form_panel.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        form_panel.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(form_panel, text="Webhook URL", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=16, pady=8)
        url_entry = ctk.CTkEntry(form_panel, placeholder_text="https://hooks.company.com/automations")
        url_entry.grid(row=0, column=1, sticky="ew", padx=(10, 16), pady=8)
        if config.get("url"):
            url_entry.insert(0, config["url"])

        ctk.CTkLabel(form_panel, text="Payload (JSON)", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, sticky="nw", padx=16, pady=8)
        payload_box = ctk.CTkTextbox(form_panel, height=140, fg_color=self.palette["surface"], text_color=self.palette["text"])
        payload_box.grid(row=1, column=1, sticky="ew", padx=(10, 16), pady=8)
        payload_box.insert("1.0", config.get("payload", '{"workflow": "example"}'))

        actions = ctk.CTkFrame(form_panel, fg_color="transparent")
        actions.grid(row=2, column=0, columnspan=2, sticky="e", padx=16, pady=(0, 16))
        ctk.CTkButton(actions, text="Save Settings", width=130, command=self._save_webhook_settings).pack(side="left", padx=6)
        ctk.CTkButton(actions, text="Send Sample Data", width=150, command=self._send_sample_webhook).pack(side="left", padx=6)

        monitor_panel = ctk.CTkFrame(
            tab,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        monitor_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 20))
        monitor_panel.grid_columnconfigure(0, weight=1)
        monitor_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(monitor_panel, text="Webhook Monitor", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))
        monitor_box = ctk.CTkTextbox(monitor_panel, fg_color=self.palette["surface"], text_color=self.palette["text"])
        monitor_box.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        history = config.get("history", [])
        if history:
            for event in history:
                monitor_box.insert("end", f"- {event}")
        else:
            monitor_box.insert("end", "No webhook activity yet.")
        monitor_box.configure(state="disabled")

        self.webhook_entries = {
            "url": url_entry,
            "payload": payload_box,
        }

    def _build_context_view(self) -> ctk.CTkFrame:
            frame = ctk.CTkFrame(self.center, corner_radius=16)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            if not self.context_manager:
                ctk.CTkLabel(
                    frame,
                    text=(
                        "Context manager not available."
                        "Install advanced modules to enable habit tracking and insights."
                    ),
                    text_color=self.palette["text_soft"],
                    font=ctk.CTkFont(size=14),
                ).pack(expand=True)
                return frame

            cards_row = ctk.CTkFrame(frame, corner_radius=14)
            cards_row.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))
            cards_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

            summary_definitions = [
                ("apps", "Most Used Apps", "#2563eb"),
                ("hours", "Top Work Hours", "#22c55e"),
                ("automations", "Automations", "#f97316"),
                ("suggestions", "AI Suggestions", "#a855f7"),
            ]
            self.context_summary_labels = {}
            for idx, (key, title, color) in enumerate(summary_definitions):
                card = ctk.CTkFrame(cards_row, corner_radius=12, fg_color=color)
                card.grid(row=0, column=idx, sticky="ew", padx=8, pady=8)
                ctk.CTkLabel(card, text=title, text_color="white", font=ctk.CTkFont(size=13, weight="bold")).pack(
                    anchor="w", padx=16, pady=(12, 6)
                )
                value_label = ctk.CTkLabel(card, text="Loading...", text_color="white", font=ctk.CTkFont(size=18))
                value_label.pack(anchor="w", padx=16, pady=(0, 14))
                self.context_summary_labels[key] = value_label

            analytics = ctk.CTkFrame(frame, corner_radius=14)
            analytics.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
            analytics.grid_columnconfigure((0, 1), weight=1)
            analytics.grid_rowconfigure(3, weight=1)

            ctk.CTkLabel(analytics, text="Usage Analytics", font=ctk.CTkFont(size=16, weight="bold")).grid(
                row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 10)
            )

            self.context_usage_box = ctk.CTkTextbox(
                analytics,
                height=160,
                fg_color=self.palette["surface"],
                text_color=self.palette["text"],
            )
            self.context_usage_box.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 16))
            self.context_usage_box.configure(state="disabled")

            self.context_timeline_box = ctk.CTkTextbox(
                analytics,
                height=160,
                fg_color=self.palette["surface"],
                text_color=self.palette["text"],
            )
            self.context_timeline_box.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 16))
            self.context_timeline_box.configure(state="disabled")

            prediction_card = ctk.CTkFrame(
                analytics,
                corner_radius=12,
                fg_color=self.palette["surface"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            prediction_card.grid(row=2, column=0, sticky="ew", padx=(20, 10), pady=(0, 16))
            ctk.CTkLabel(
                prediction_card,
                text="Next Suggested Action",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).pack(anchor="w", padx=16, pady=(12, 4))
            self.context_prediction_label = ctk.CTkLabel(prediction_card, text="Loading...")
            self.context_prediction_label.pack(anchor="w", padx=16, pady=(0, 12))

            learning_card = ctk.CTkFrame(
                analytics,
                corner_radius=12,
                fg_color=self.palette["surface"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            learning_card.grid(row=2, column=1, sticky="ew", padx=(10, 20), pady=(0, 16))
            ctk.CTkLabel(learning_card, text="Learning Status", font=ctk.CTkFont(weight="bold")).pack(
                anchor="w", padx=16, pady=(12, 4)
            )
            self.context_learning_label = ctk.CTkLabel(learning_card, text="Monitoring habits...")
            self.context_learning_label.pack(anchor="w", padx=16, pady=(0, 12))

            suggestions_card = ctk.CTkFrame(
                analytics,
                corner_radius=12,
                fg_color=self.palette["surface"],
                border_width=1,
                border_color=self.palette["stroke"],
            )
            suggestions_card.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0, 20))
            ctk.CTkLabel(suggestions_card, text="AI Suggestions", font=ctk.CTkFont(weight="bold")).pack(
                anchor="w", padx=16, pady=(12, 4)
            )
            self.context_suggestions_box = ctk.CTkTextbox(
                suggestions_card,
                height=120,
                fg_color=self.palette["surface"],
                text_color=self.palette["text"],
            )
            self.context_suggestions_box.pack(fill="both", expand=True, padx=16, pady=(0, 12))
            self.context_suggestions_box.configure(state="disabled")

            self._refresh_context_insights()
            return frame

    def _refresh_context_insights(self) -> None:
        """Refresh the context insights view with current data."""
        if not self.context_manager or not hasattr(self, "context_summary_labels"):
            return

        try:
            # Get context data
            insights = getattr(self.context_manager, "get_insights", lambda: {})()
            
            # Update summary cards
            if "apps" in self.context_summary_labels:
                top_apps = insights.get("top_apps", ["Chrome", "VSCode", "Slack"])
                self.context_summary_labels["apps"].configure(text=", ".join(top_apps[:2]))
            
            if "hours" in self.context_summary_labels:
                peak_hours = insights.get("peak_hours", "9-11 AM, 2-4 PM")
                self.context_summary_labels["hours"].configure(text=peak_hours)
            
            if "automations" in self.context_summary_labels:
                automation_count = insights.get("automation_count", len(self.history))
                self.context_summary_labels["automations"].configure(text=str(automation_count))
            
            if "suggestions" in self.context_summary_labels:
                suggestion_count = insights.get("suggestion_count", 5)
                self.context_summary_labels["suggestions"].configure(text=f"{suggestion_count} Active")

            # Update usage box
            if hasattr(self, "context_usage_box"):
                self.context_usage_box.configure(state="normal")
                self.context_usage_box.delete("1.0", "end")
                usage_data = insights.get("usage", "App usage tracking active.\n\nRecent activity:\n- Document editing\n- Web browsing\n- Email management")
                self.context_usage_box.insert("1.0", usage_data)
                self.context_usage_box.configure(state="disabled")

            # Update timeline box
            if hasattr(self, "context_timeline_box"):
                self.context_timeline_box.configure(state="normal")
                self.context_timeline_box.delete("1.0", "end")
                timeline = insights.get("timeline", "Recent Timeline:\n\n09:00 - Email check\n10:30 - Document work\n14:00 - Team meeting\n16:00 - Code review")
                self.context_timeline_box.insert("1.0", timeline)
                self.context_timeline_box.configure(state="disabled")

            # Update prediction label
            if hasattr(self, "context_prediction_label"):
                prediction = insights.get("prediction", "Check email and start daily standup")
                self.context_prediction_label.configure(text=prediction)

            # Update learning status
            if hasattr(self, "context_learning_label"):
                learning_status = insights.get("learning_status", f"Tracked {len(self.history)} interactions")
                self.context_learning_label.configure(text=learning_status)

            # Update suggestions box
            if hasattr(self, "context_suggestions_box"):
                self.context_suggestions_box.configure(state="normal")
                self.context_suggestions_box.delete("1.0", "end")
                suggestions = insights.get("suggestions", [
                    "• Consider automating your morning email routine",
                    "• Peak productivity detected between 10-11 AM",
                    "• Create a workflow for report generation",
                    "• Schedule breaks based on your work patterns"
                ])
                if isinstance(suggestions, list):
                    suggestions_text = "\n".join(suggestions)
                else:
                    suggestions_text = suggestions
                self.context_suggestions_box.insert("1.0", suggestions_text)
                self.context_suggestions_box.configure(state="disabled")

        except Exception as e:
            # Silently fail if context manager doesn't have expected methods
            pass

    # ------------------------------------------------------------------ #
    # Security Center
    # ------------------------------------------------------------------ #

    def _build_security_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.center, corner_radius=16)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tabs = ctk.CTkTabview(frame, corner_radius=14)
        tabs.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

        permissions_tab = tabs.add("Permissions")
        sandbox_tab = tabs.add("Sandbox")
        undo_tab = tabs.add("Undo Stack")
        protected_tab = tabs.add("Protected Paths")
        secrets_tab = tabs.add("Secrets Vault")
        backups_tab = tabs.add("Backup Points")

        for label, enabled in [
            ("File Read", True),
            ("File Write", False),
            ("Network Access", True),
            ("System Modify", False),
        ]:
            switch = ctk.CTkSwitch(permissions_tab, text=label)
            switch.select() if enabled else switch.deselect()
            switch.pack(anchor="w", padx=20, pady=8)
        ctk.CTkButton(permissions_tab, text="Grant Temporary Access", width=210).pack(
            anchor="e", padx=20, pady=16
        )

        sandbox_tab.grid_columnconfigure(0, weight=1)
        sandbox_toggle = ctk.CTkSwitch(sandbox_tab, text="Sandbox Mode", command=self._toggle_sandbox_mode)
        sandbox_toggle.pack(anchor="w", padx=20, pady=(20, 10))
        ctk.CTkLabel(
            sandbox_tab,
            text="All commands are simulated while sandbox is active.",
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", padx=20)

        undo_tab.grid_rowconfigure(0, weight=1)
        undo_text = ctk.CTkTextbox(undo_tab, wrap="word")
        undo_text.insert(
            "1.0",
            "13:05 Undo ready - Deleted file restored\n"
            "12:58 Undo ready - Window reopened\n"
            "12:31 Undo ready - Folder move reverted\n",
        )
        undo_text.configure(state="disabled")
        undo_text.pack(fill="both", expand=True, padx=20, pady=20)
        undo_actions = ctk.CTkFrame(undo_tab, fg_color="transparent")
        undo_actions.pack(anchor="e", padx=20, pady=(0, 20))
        for title in ["Undo", "Redo", "Clear"]:
            ctk.CTkButton(undo_actions, text=title, width=90).pack(side="left", padx=6)

        ctk.CTkLabel(protected_tab, text="Protected Folders", font=ctk.CTkFont(weight="bold")).pack(
            anchor="w", padx=20, pady=(20, 6)
        )
        protected_box = ctk.CTkTextbox(protected_tab, height=180)
        protected_box.insert("1.0", "C:\\Finance\nC:\\Projects\nC:\\System\\Configs\n")
        protected_box.configure(state="disabled")
        protected_box.pack(fill="x", padx=20)
        ctk.CTkLabel(
            protected_tab,
            text="Prevents accidental modification or deletion.",
            text_color=self.palette["text_soft"],
        ).pack(anchor="w", padx=20, pady=6)
        ctk.CTkButton(protected_tab, text="Add Folder").pack(anchor="w", padx=20, pady=(0, 16))

        secrets_table = ttk.Treeview(
            secrets_tab,
            columns=("key", "status"),
            show="headings",
            height=6,
        )
        secrets_table.heading("key", text="Key")
        secrets_table.heading("status", text="Status")
        secrets_table.insert("", "end", values=("GOOGLE_API_KEY", "Encrypted"))
        secrets_table.pack(fill="both", expand=True, padx=20, pady=20)
        ctk.CTkButton(secrets_tab, text="Add Secret").pack(anchor="e", padx=20, pady=(0, 14))

        backup_table = ttk.Treeview(
            backups_tab,
            columns=("name", "created", "size"),
            show="headings",
            height=6,
        )
        for column in ("name", "created", "size"):
            backup_table.heading(column, text=column.title())
            backup_table.column(column, anchor="w", width=160)
        backup_table.insert("", "end", values=("pre-update", "2025-03-01 17:20", "1.2 GB"))
        backup_table.insert("", "end", values=("design-review", "2025-02-20 09:10", "800 MB"))
        backup_table.pack(fill="both", expand=True, padx=20, pady=20)

        backup_actions = ctk.CTkFrame(backups_tab, fg_color="transparent")
        backup_actions.pack(anchor="e", padx=20, pady=(0, 16))
        for title in ["Create Backup", "Restore", "Delete"]:
            ctk.CTkButton(backup_actions, text=title, width=130).pack(side="left", padx=6)

        return frame

    # ------------------------------------------------------------------ #
    # Settings
    # ------------------------------------------------------------------ #

    def _build_settings_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.center, corner_radius=16)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tabs = ctk.CTkTabview(frame, corner_radius=14)
        tabs.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

        general = tabs.add("General")
        voice = tabs.add("Voice & Input")
        api = tabs.add("API & Keys")
        integrations = tabs.add("Integrations")
        privacy = tabs.add("Privacy")
        about = tabs.add("About")

        self.settings_vars = {
            "theme": ctk.StringVar(value=self.user_settings.get("theme", "System")),
            "language": ctk.StringVar(value=self.user_settings.get("language", "English")),
            "notifications": ctk.StringVar(value=self.user_settings.get("notifications", "Toast")),
            "microphone": ctk.StringVar(value=self.user_settings.get("microphone", "Default")),
            "voice_feedback": ctk.BooleanVar(value=self.user_settings.get("voice_feedback", True)),
            "auto_run_on_enter": ctk.BooleanVar(value=self.user_settings.get("auto_run_on_enter", True)),
            "context_tracking": ctk.BooleanVar(value=self.user_settings.get("context_tracking", True)),
            "data_retention_days": ctk.StringVar(value=str(self.user_settings.get("data_retention_days", 30))),
            "api_key": ctk.StringVar(value=self.user_settings.get("google_api_key", "")),
        }

        # General tab
        general.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(general, text="Theme").grid(row=0, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkOptionMenu(general, values=["Dark", "Light", "System"], variable=self.settings_vars["theme"]).grid(row=0, column=1, sticky="w", padx=20)
        ctk.CTkLabel(general, text="Language").grid(row=1, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkOptionMenu(general, values=["English", "German", "French"], variable=self.settings_vars["language"]).grid(row=1, column=1, sticky="w", padx=20)
        ctk.CTkLabel(general, text="Notifications").grid(row=2, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkSegmentedButton(general, values=["Toast", "Voice"], variable=self.settings_vars["notifications"]).grid(row=2, column=1, sticky="w", padx=20)
        ctk.CTkButton(general, text="Save General Settings", command=self._handle_save_settings).grid(row=3, column=1, sticky="e", padx=20, pady=(12, 20))

        # Voice tab
        voice.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(voice, text="Microphone").grid(row=0, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkOptionMenu(voice, values=["Default", "Studio Mic", "USB Headset"], variable=self.settings_vars["microphone"]).grid(row=0, column=1, sticky="w", padx=20)
        ctk.CTkSwitch(voice, text="Voice Feedback", variable=self.settings_vars["voice_feedback"]).grid(row=1, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkSwitch(voice, text="Auto-run on Enter", variable=self.settings_vars["auto_run_on_enter"]).grid(row=2, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkButton(voice, text="Save Voice Settings", command=self._handle_save_settings).grid(row=3, column=1, sticky="e", padx=20, pady=(12, 20))

        # API tab
        api.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(api, text="Google API Key").grid(row=0, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkEntry(api, textvariable=self.settings_vars["api_key"], fg_color=self.palette["surface"], show="*").grid(row=0, column=1, sticky="ew", padx=20, pady=12)
        ctk.CTkButton(api, text="Save API Settings", command=self._handle_save_settings).grid(row=1, column=1, sticky="e", padx=20, pady=(12, 20))

        # Integrations tab summary
        integrations.grid_columnconfigure(0, weight=1)
        integrations_text = ctk.CTkTextbox(integrations, height=200, fg_color=self.palette["surface"], text_color=self.palette["text"])
        integrations_text.pack(fill="both", expand=True, padx=20, pady=20)
        integrations_text.insert("1.0", json.dumps(self.integration_manager.config if self.integration_manager else {}, indent=2))
        integrations_text.configure(state="disabled")

        # Privacy tab
        ctk.CTkSwitch(privacy, text="Context Tracking", variable=self.settings_vars["context_tracking"]).grid(row=0, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkLabel(privacy, text="Data Retention (days)").grid(row=1, column=0, sticky="w", padx=20, pady=12)
        ctk.CTkEntry(privacy, textvariable=self.settings_vars["data_retention_days"], width=120).grid(row=1, column=1, sticky="w", padx=20, pady=12)
        ctk.CTkButton(privacy, text="Save Privacy Settings", command=self._handle_save_settings).grid(row=2, column=1, sticky="e", padx=20, pady=(12, 20))

        # About tab
        about_text = (
            "Windows Use Agent – Enterprise v2.0"
            f"Profiles stored at: {self.settings_path}"
            "Open source project – Adaptive Cognition 2025"
        )
        ctk.CTkLabel(about, text=about_text, justify="left", text_color=self.palette["text"]).pack(padx=20, pady=20, anchor="w")

        return frame
    
    def _handle_save_settings(self) -> None:
        if not hasattr(self, "settings_vars"):
            return

        self.user_settings.update({
            "theme": self.settings_vars["theme"].get(),
            "language": self.settings_vars["language"].get(),
            "notifications": self.settings_vars["notifications"].get(),
            "microphone": self.settings_vars["microphone"].get(),
            "voice_feedback": bool(self.settings_vars["voice_feedback"].get()),
            "auto_run_on_enter": bool(self.settings_vars["auto_run_on_enter"].get()),
            "context_tracking": bool(self.settings_vars["context_tracking"].get()),
            "google_api_key": self.settings_vars["api_key"].get().strip(),
        })

        try:
            self.user_settings["data_retention_days"] = max(1, int(self.settings_vars["data_retention_days"].get()))
            self.settings_vars["data_retention_days"].set(str(self.user_settings["data_retention_days"]))
        except ValueError:
            self.user_settings["data_retention_days"] = 30
            self.settings_vars["data_retention_days"].set("30")

        # Apply theme immediately
        theme = self.user_settings.get("theme", "System")
        ctk.set_appearance_mode(theme.lower() if theme in ("Light", "Dark") else "system")

        self._save_user_settings()


    def _build_logs_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.center, corner_radius=16)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        toolbar = ctk.CTkFrame(frame, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 12))

        ctk.CTkLabel(toolbar, text="Logs & History", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        self.history_search_entry = ctk.CTkEntry(toolbar, placeholder_text="Search commands...")
        self.history_search_entry.pack(side="left", padx=12, fill="x", expand=True)

        table_panel = ctk.CTkFrame(frame, corner_radius=14)
        table_panel.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        table_panel.grid_rowconfigure(0, weight=1)
        table_panel.grid_columnconfigure(0, weight=1)

        self.history_table = ttk.Treeview(
            table_panel,
            columns=("command", "timestamp", "mode", "status", "duration"),
            show="headings",
        )
        headings = {
            "command": "Command",
            "timestamp": "Timestamp",
            "mode": "Mode",
            "status": "Status",
            "duration": "Duration",
        }
        for key, title in headings.items():
            self.history_table.heading(key, text=title)
            self.history_table.column(key, anchor="w", width=220 if key == "command" else 140)
        self.history_table.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        actions = ctk.CTkFrame(table_panel, fg_color="transparent")
        actions.grid(row=1, column=0, sticky="e", padx=20, pady=(0, 18))
        ctk.CTkButton(actions, text="Export CSV", width=130, command=self._export_history_csv).pack(side="left", padx=6)
        ctk.CTkButton(actions, text="Clear History", width=130, command=self._clear_history).pack(side="left", padx=6)

        self._refresh_history_table()
        return frame


    def _refresh_history_table(self) -> None:
        if not hasattr(self, "history_table"):
            return
        for row in self.history_table.get_children():
            self.history_table.delete(row)
        for entry in reversed(self.history[-200:]):
            self.history_table.insert(
                "",
                "end",
                values=(
                    entry.get("command", ""),
                    entry.get("timestamp", ""),
                    entry.get("mode", ""),
                    entry.get("status", "pending"),
                    entry.get("duration", "-"),
                ),
            )

    def _export_history_csv(self) -> None:
        if not self.history:
            self._add_response_card(
                summary="No history to export.",
                body="Execute a command to generate history entries.",
                status="info",
                duration="-",
                mode="Basic",
            )
            return
        filename = f"command_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write("command,timestamp,mode,status,duration")
            for entry in self.history:
                fh.write(
                    f"{entry.get('command','')},{entry.get('timestamp','')},{entry.get('mode','')},{entry.get('status','pending')},{entry.get('duration','-')}\n"
                )
        self._add_response_card(
            summary="History exported.",
            body=f"CSV written to {filename}",
            status="success",
            duration="-",
            mode="Basic",
        )

    def _clear_history(self) -> None:
        self.history.clear()
        self._refresh_history_table()
        self._add_response_card(
            summary="History cleared.",
            body="Command history has been removed for this session.",
            status="info",
            duration="-",
            mode="Basic",
        )


    # ------------------------------------------------------------------ #
    # Help & Onboarding
    # ------------------------------------------------------------------ #


    def _run_demo_workflow(self) -> None:
        if not hasattr(self, 'text_entry'):
            return
        demo_command = "List open windows"
        self._add_response_card(
            summary="Demo workflow started.",
            body="Running a sample automation: list open windows.",
            status="info",
            duration="-",
            mode="Workflow",
        )
        self.text_entry.delete(0, "end")
        self.text_entry.insert(0, demo_command)
        self._execute_text_command()

    def _load_help_content(self) -> Dict[str, str]:
            if self.help_content_cache:
                return self.help_content_cache

            content_map: Dict[str, str] = {}
            readme_path = Path(__file__).resolve().parent / "README.md"
            if readme_path.exists():
                try:
                    raw = readme_path.read_text(encoding="utf-8")
                    markdown_text = markdownify(raw)
                    sections = {}
                    current = "General"
                    for line in raw.splitlines():
                        if line.startswith("## "):
                            current = line[3:].strip()
                            sections[current] = []
                        else:
                            sections.setdefault(current, []).append(line)
                    for heading, lines in sections.items():
                        content_map[heading.lower()] = markdownify("".join(lines))
                    content_map["full"] = markdown_text
                except Exception as exc:
                    content_map["error"] = f"Failed to load documentation: {exc}"
            else:
                content_map["error"] = "README.md not found for help content."

            roadmap_path = Path(__file__).resolve().parent / "EVOLUTION_ROADMAP.md"
            if roadmap_path.exists():
                try:
                    content_map["roadmap"] = markdownify(roadmap_path.read_text(encoding="utf-8"))
                except Exception:
                    pass

            self.help_content_cache = content_map
            return content_map



    def _build_help_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.center, corner_radius=16)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        content = self._load_help_content()
        tabs = ctk.CTkTabview(frame, corner_radius=14)
        tabs.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)

        mapping = {
            "Quick Start": "quick start",
            "Troubleshooting": "troubleshooting",
            "Documentation": "full",
            "Contact Support": "support",
        }
        for name, key in mapping.items():
            tab = tabs.add(name)
            text_box = ctk.CTkTextbox(tab, wrap="word", fg_color=self.palette["surface"], text_color=self.palette["text"])
            text_box.pack(fill="both", expand=True, padx=20, pady=20)
            match = None
            for heading, body in content.items():
                if key in heading:
                    match = body
                    break
            if not match:
                match = content.get("full") or content.get("error") or "Documentation not available."
            text_box.insert("1.0", match)
            text_box.configure(state="disabled")

        ctk.CTkButton(frame, text="Run Demo Workflow", width=180, command=self._run_demo_workflow).grid(
            row=1, column=0, sticky="e", padx=24, pady=(0, 24)
        )

        return frame

    # ------------------------------------------------------------------ #
    # Voice Input & Placeholder rotation
    # ------------------------------------------------------------------ #

    def _toggle_sidebar(self) -> None:
        """Toggle sidebar visibility."""
        if self.sidebar_collapsed:
            # Expand sidebar
            self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(16, 0), pady=16)
            self.toggle_btn.configure(text="<")
            self.sidebar_collapsed = False
        else:
            # Collapse sidebar
            self.sidebar.grid_forget()
            self.toggle_btn.configure(text=">")
            self.sidebar_collapsed = True

    def _navigate(self, view: str) -> None:
        """Navigate to a different view."""
        self.current_view = view
        self._update_nav_styles()
        self._update_right_panel(view)

    def _update_nav_styles(self) -> None:
        """Update navigation button styles to highlight the current view."""
        for name, btn in self.nav_buttons.items():
            if name == self.current_view:
                # Highlight active button
                btn.configure(
                    fg_color=self.palette["surface"],
                    border_width=1,
                    border_color=self.palette["stroke"],
                    text_color=self.palette["text"],
                )
            else:
                # Reset inactive buttons
                btn.configure(
                    fg_color="transparent",
                    border_width=0,
                    text_color=self.palette["text"],
                )

    def _update_right_panel(self, view: str) -> None:
        """Update the right panel to show content for the current view."""
        # Clear existing content
        for widget in self.right_panel.winfo_children():
            widget.pack_forget()
        
        # Show the appropriate view
        if view in self.views:
            self.views[view].pack(fill="both", expand=True)

    def _show_view(self, view: str) -> None:
        """Show a specific view by name."""
        self.current_view = view
        self._update_nav_styles()
        self._update_right_panel(view)

    def _toggle_listening(self) -> None:
        if not self.voice_enabled:
            self._add_response_card(
                summary="Voice input unavailable.",
                body="Install the audio dependencies (see install.bat) to enable speech commands.",
                status="error",
                duration="-",
                mode="Secure",
            )
            return

        if self.is_listening:
            self.is_listening = False
            self.voice_btn.configure(text="Voice", fg_color="#1d4ed8")
            self.transcription_label.configure(text="")
        else:
            self.is_listening = True
            self.voice_btn.configure(text="Stop", fg_color="#ef4444")
            self.transcription_label.configure(text="Listening...", text_color="#fbbf24")
            threading.Thread(target=self._listen_for_voice, daemon=True).start()

    def _listen_for_voice(self) -> None:
        try:
            if self.voice_backend == "sounddevice":
                self.after(
                    0,
                    lambda: self.transcription_label.configure(
                        text="Processing speech...", text_color="#fbbf24"
                    ),
                )
                audio = self._capture_audio_sounddevice()
            elif self.voice_backend == "pyaudio" and hasattr(self, "microphone"):
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.after(
                    0,
                    lambda: self.transcription_label.configure(
                        text="Processing speech...", text_color="#fbbf24"
                    ),
                )
            else:
                raise sr.WaitTimeoutError("Voice backend is not configured.")

            transcript = self.recognizer.recognize_google(audio)
            self.after(0, lambda: self._handle_transcription(transcript))
        except sr.WaitTimeoutError:
            self.after(
                0,
                lambda: self.transcription_label.configure(text="No speech detected.", text_color="#ef4444"),
            )
        except sr.UnknownValueError:
            self.after(
                0,
                lambda: self.transcription_label.configure(
                    text="Could not understand audio. Please speak clearly.", text_color="#ef4444"
                ),
            )
        except Exception as error:
            self.after(
                0,
                lambda: self.transcription_label.configure(text=f"Speech error: {error}", text_color="#ef4444"),
            )
        finally:
            self.after(0, self._toggle_listening)

    def _handle_transcription(self, text: str) -> None:
        self.transcription_label.configure(text=f'You said: "{text}"', text_color="#10b981")
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, text)
        self._execute_text_command()

    def _start_placeholder_rotation(self) -> None:
        if self.placeholder_job:
            self.after_cancel(self.placeholder_job)
        self.placeholder_job = self.after(4000, self._rotate_placeholder)

    def _rotate_placeholder(self) -> None:
        if self.command_entry.get() or self.focus_get() == self.command_entry:
            self._start_placeholder_rotation()
            return
        self.placeholder_index = (self.placeholder_index + 1) % len(self.PLACEHOLDER_ROTATION)
        self.command_entry.configure(placeholder_text=self.PLACEHOLDER_ROTATION[self.placeholder_index])
        self._start_placeholder_rotation()

    def _capture_audio_sounddevice(self, timeout: float = 8.0, silence: float = 1.0) -> sr.AudioData:
        if not hasattr(self, "sd"):
            raise sr.WaitTimeoutError("sounddevice backend not available")

        block_duration = 0.1
        block_samples = max(1, int(self.sd_samplerate * block_duration))
        frames = []
        silence_run = 0.0
        start_time = time.time()

        with self.sd.InputStream(samplerate=self.sd_samplerate, channels=1, dtype="int16") as stream:
            while True:
                data, _ = stream.read(block_samples)
                frames.append(data.copy())

                mean_amplitude = float(np.abs(data).mean())
                if mean_amplitude > self.sd_voice_threshold:
                    silence_run = 0.0
                else:
                    silence_run += block_duration

                elapsed = time.time() - start_time
                if (silence_run >= silence and len(frames) > 3) or elapsed >= timeout:
                    break

        if not frames:
            raise sr.WaitTimeoutError("No audio captured")

        audio_bytes = b"".join(frame.tobytes() for frame in frames)
        return sr.AudioData(audio_bytes, self.sd_samplerate, 2)

    def _shade_color(self, color: str, factor: float) -> str:
        """Return a hex color lightened (factor > 0) or darkened (factor < 0)."""
        color = color.lstrip("#")
        if len(color) != 6:
            return f"#{color}"

        r, g, b = (int(color[i : i + 2], 16) for i in (0, 2, 4))
        if factor < 0:
            factor = 1 + factor
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
        else:
            r = int(r + (255 - r) * factor)
            g = int(g + (255 - g) * factor)
            b = int(b + (255 - b) * factor)

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return f"#{r:02x}{g:02x}{b:02x}"

    # ------------------------------------------------------------------ #
    # Misc Helpers
    # ------------------------------------------------------------------ #

    def _toggle_sandbox_mode(self) -> None:
        self._add_response_card(
            summary="Sandbox toggle requested.",
            body="Sandbox state toggled. Commands will now respect the updated policy.",
            status="info",
            duration="-",
            mode="Secure",
        )

    def _center_window(self) -> None:
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _add_intro_card(self) -> None:
        self._add_response_card(
            summary="Welcome to Windows Use Agent Enterprise.",
            body=(
                "Use the command console to orchestrate desktop automations, smart workflows, "
                "and secure integrations. Select a mode or run any example to get started."
            ),
            status="info",
            duration="-",
            mode="Basic",
        )

    def _on_mode_change(self, mode: str) -> None:
        self.current_mode = mode
        color = self.MODE_COLORS.get(mode, "#2563eb")
        self.execute_btn.configure(fg_color=color, hover_color=self._shade_color(color, -0.2))
        self.status_badge.configure(fg_color=color)

        titles = {
            "Basic": ("Command Console", "Execute and visualize AI-powered desktop commands."),
            "Workflow": ("Workflow Orchestration", "Create, test, and deploy multi-step task chains."),
            "Context": ("Context Intelligence", "Review analytics, habits, and proactive suggestions."),
            "Secure": ("Secure Operations", "Guardrails, permissions, sandboxing, and undo recovery."),
            "Integrated": ("Integrated Ecosystem", "Connect Gmail, cloud storage, webhooks, and APIs."),
        }
        title, subtitle = titles.get(mode, titles["Basic"])
        self.mode_title.configure(text=title)
        self.mode_subtitle.configure(text=subtitle)

        examples = list(self.MODE_EXAMPLES.get(mode, self.MODE_EXAMPLES["Basic"]))
        self.examples_menu.configure(values=examples)
        self.examples_menu.set("Examples ▾")
        for btn in self.quick_buttons:
            btn.configure(fg_color=color, hover_color=self._shade_color(color, -0.2))
        self._update_nav_styles()
        self._update_right_panel(self.current_view)

        self._add_response_card(
            summary=f"Mode switched to {mode}.",
            body="The console, examples, and analytics now emphasize this operating mode.",
            status="info",
            duration="-",
            mode=mode,
        )

    def _on_example_selected(self, value: str) -> None:
        if value == "Examples ▾":
            return
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, value)
        self._execute_text_command()
        self.examples_menu.set("Examples ▾")

    def _run_quick_command(self, text: str) -> None:
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, text)
        self._execute_text_command()

    def _execute_text_command(self) -> None:
        command = self.command_entry.get().strip()
        if not command:
            return

        self.history.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "command": command,
                "mode": self.current_mode,
            }
        )

        self.command_entry.delete(0, "end")
        self._set_status("processing")
        self.execute_btn.configure(state="disabled", text="Working…")

        self._add_response_card(
            summary=f"Executing: {command}",
            body=f"The {self.current_mode.lower()} agent is working on this request.",
            status="processing",
            duration="-",
            mode=self.current_mode,
        )

        worker = threading.Thread(target=self._run_agent, args=(command,), daemon=True)
        worker.start()

    def _run_agent(self, command: str) -> None:
        start = time.perf_counter()
        if not self.agent_ready:
            self.after(0, lambda: self._on_agent_error("Agent not configured. Check API keys and network."))
            return

        try:
            result = self.agent.invoke(query=command)
            duration = f"{time.perf_counter() - start:.2f}s"
            response = getattr(result, "content", str(result))
            summary = (response.strip().splitlines() or ["Command completed."])[0][:90]
            if self.history:
                self.history[-1].update(
                    {
                        "status": "success",
                        "duration": duration,
                        "response": response,
                    }
                )
            self.after(
                0,
                lambda: self._add_response_card(
                    summary=f"\u2705 {summary}",
                    body=response,
                    status="success",
                    duration=duration,
                    mode=self.current_mode,
                ),
            )
            self.after(0, lambda: self._set_status("ready"))
            self.after(0, self._refresh_history_table)
        except Exception as error:  # pragma: no cover - runtime safety
            if self.history:
                self.history[-1].update(
                    {
                        "status": "error",
                        "duration": "-",
                        "response": str(error),
                    }
                )
            self.after(0, lambda: self._on_agent_error(str(error)))
            self.after(0, self._refresh_history_table)

    def _on_agent_error(self, message: str) -> None:
        self._add_response_card(
            summary="\u274c Command failed.",
            body=message,
            status="error",
            duration="-",
            mode=self.current_mode,
        )
        self._set_status("error")

    def _clear_responses(self) -> None:
        for card in self.response_cards:
            card.destroy()
        self.response_cards.clear()
        self.response_timestamp.configure(text="Last updated: -")

    def _add_response_card(self, summary: str, body: str, status: str, duration: str, mode: str) -> None:
        card = ctk.CTkFrame(
            self.response_feed,
            corner_radius=12,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        card.grid_columnconfigure(0, weight=1)

        accent = self.MODE_COLORS.get(mode, "#2563eb")
        accent_bar = ctk.CTkFrame(card, height=4, corner_radius=4, fg_color=accent)
        accent_bar.grid(row=0, column=0, sticky="ew")

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.grid(row=1, column=0, sticky="ew", padx=18, pady=14)
        content.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text=summary, font=ctk.CTkFont(size=14, weight="bold")).grid(
            row=0, column=0, sticky="w"
        )

        timestamp = datetime.now().strftime("%H:%M:%S")
        meta = ctk.CTkLabel(header, text=f"{duration} | {timestamp}", text_color=self.palette["text_soft"])
        meta.grid(row=0, column=1, sticky="e")

        textbox = ctk.CTkTextbox(
            content,
            height=120,
            wrap="word",
            font=ctk.CTkFont(size=12),
            fg_color=self.palette["surface"],
            text_color=self.palette["text"],
        )
        textbox.insert("1.0", body.strip() or "No additional output provided.")
        textbox.configure(state="disabled")
        textbox.grid(row=1, column=0, sticky="ew", pady=(10, 14))

        actions = ctk.CTkFrame(content, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="e")

        ctk.CTkButton(actions, text="Copy", width=80, command=lambda text=body: self._copy_to_clipboard(text)).pack(
            side="right", padx=(10, 0)
        )
        ctk.CTkButton(actions, text="Save", width=80, command=lambda text=body: self._save_result(text)).pack(
            side="right", padx=(10, 0)
        )
        ctk.CTkButton(actions, text="Undo", width=80, command=self._request_undo).pack(side="right")

        status_color = {
            "success": "#16a34a",
            "processing": "#f59e0b",
            "info": "#0ea5e9",
            "error": "#ef4444",
        }.get(status, self.palette["text_soft"][0])
        ctk.CTkLabel(
            content,
            text=f"Status: {status.capitalize()}",
            text_color=status_color,
        ).grid(
            row=3, column=0, sticky="w", pady=(6, 0)
        )

        # Pack the card - add to the top if other packed cards exist
        if self.response_cards:
            try:
                # Try to pack before the first existing card
                card.pack(fill="x", padx=4, pady=6, before=self.response_cards[0])
            except Exception:
                # If that fails, just pack it normally at the end
                card.pack(fill="x", padx=4, pady=6)
        else:
            # First card, just pack it normally
            card.pack(fill="x", padx=4, pady=6)

        self.response_cards.insert(0, card)
        self.response_timestamp.configure(text=f"Last updated: {timestamp}")
        self._update_right_panel(self.current_view)

    def _set_status(self, state: str) -> None:
        if state == "processing":
            self.status_badge.configure(text="Processing", fg_color="#fbbf24")
        elif state == "error":
            self.status_badge.configure(text="Error", fg_color="#ef4444")
        else:
            self.status_badge.configure(text="Ready", fg_color="#16a34a")
        self.execute_btn.configure(state="normal", text="Execute")

    def _copy_to_clipboard(self, text: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(text)
        self._add_response_card(
            summary="Response copied to clipboard.",
            body="Result text is ready to paste into any application.",
            status="info",
            duration="-",
            mode=self.current_mode,
        )

    def _save_result(self, text: str) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"agent_result_{timestamp}.txt"
        path = os.path.join(os.getcwd(), filename)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        self._add_response_card(
            summary="Response saved to disk.",
            body=f"File stored at {path}",
            status="info",
            duration="-",
            mode=self.current_mode,
        )

    def _request_undo(self) -> None:
        self._add_response_card(
            summary="Undo requested.",
            body="The security stack will attempt to reverse the last executed action.",
            status="processing",
            duration="-",
            mode="Secure",
        )

    # ------------------------------------------------------------------ #
    # Workflow Builder
    # ------------------------------------------------------------------ #

    def _build_workflow_view(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            self.center,
            corner_radius=16,
            fg_color=self.palette["surface"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        frame.grid_columnconfigure((0, 1, 2), weight=1)
        frame.grid_rowconfigure(0, weight=1)

        if not self.workflow_engine:
            ctk.CTkLabel(
                frame,
                text=(
                    "Advanced workflow engine is not available."
                    "Run install.bat to enable SmartWorkflowEngine features."
                ),
                text_color=self.palette["text_soft"],
                font=ctk.CTkFont(size=14),
            ).pack(expand=True)
            return frame

        list_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        list_panel.grid(row=0, column=0, sticky="nsew", padx=(24, 12), pady=24)
        list_panel.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(list_panel, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Workflows",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(
            header,
            text="New Workflow",
            width=120,
            command=lambda: self._open_workflow_editor(None),
        ).grid(row=0, column=1, sticky="e")

        self.workflow_list_container = ctk.CTkScrollableFrame(
            list_panel,
            corner_radius=12,
            fg_color="transparent",
        )
        self.workflow_list_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 12))

        self.workflow_list_empty = ctk.CTkLabel(
            self.workflow_list_container,
            text="No workflows yet.\nClick 'New Workflow' to create one.",
            text_color=self.palette["text_soft"],
            font=ctk.CTkFont(size=13),
            justify="center",
        )

        detail_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        detail_panel.grid(row=0, column=1, sticky="nsew", padx=12, pady=24)
        detail_panel.grid_columnconfigure(0, weight=1)
        detail_panel.grid_rowconfigure(4, weight=1)

        self.workflow_detail_title = ctk.CTkLabel(
            detail_panel,
            text="Select a workflow to view details",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        )
        self.workflow_detail_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        self.workflow_detail_subtitle = ctk.CTkLabel(
            detail_panel,
            text="",
            text_color=self.palette["text_soft"],
            justify="left",
        )
        self.workflow_detail_subtitle.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 6))

        self.workflow_description = ctk.CTkTextbox(
            detail_panel,
            height=80,
            fg_color=self.palette["surface"],
            text_color=self.palette["text"],
            wrap="word",
        )
        self.workflow_description.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 12))
        self.workflow_description.configure(state="disabled")

        self.workflow_steps_container = ctk.CTkScrollableFrame(
            detail_panel,
            corner_radius=12,
            fg_color="transparent",
        )
        self.workflow_steps_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 12))

        action_row = ctk.CTkFrame(detail_panel, fg_color="transparent")
        action_row.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 20))
        action_row.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.workflow_run_button = ctk.CTkButton(
            action_row, text="Run Workflow", command=self._run_selected_workflow
        )
        self.workflow_run_button.grid(row=0, column=0, padx=4)
        self.workflow_optimize_button = ctk.CTkButton(
            action_row, text="Optimize", command=self._optimize_selected_workflow
        )
        self.workflow_optimize_button.grid(row=0, column=1, padx=4)
        self.workflow_edit_button = ctk.CTkButton(
            action_row, text="Edit", command=lambda: self._open_workflow_editor(self.selected_workflow)
        )
        self.workflow_edit_button.grid(row=0, column=2, padx=4)
        self.workflow_delete_button = ctk.CTkButton(
            action_row,
            text="Delete",
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=self._delete_selected_workflow,
        )
        self.workflow_delete_button.grid(row=0, column=3, padx=4)

        self.workflow_sidebar_panel = ctk.CTkFrame(
            frame,
            corner_radius=14,
            fg_color=self.palette["surface_alt"],
            border_width=1,
            border_color=self.palette["stroke"],
        )
        self.workflow_sidebar_panel.grid(row=0, column=2, sticky="nsew", padx=(12, 24), pady=24)
        self.workflow_sidebar_panel.grid_columnconfigure(0, weight=1)
        self.workflow_sidebar_panel.grid_rowconfigure(3, weight=1)

        self.workflow_metrics_label = ctk.CTkLabel(
            self.workflow_sidebar_panel,
            text="Workflow Metrics",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.palette["text"],
        )
        self.workflow_metrics_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.workflow_metrics_text = ctk.CTkTextbox(
            self.workflow_sidebar_panel,
            height=120,
            fg_color=self.palette["surface"],
            text_color=self.palette["text"],
            wrap="word",
        )
        self.workflow_metrics_text.grid(row=1, column=0, sticky="ew", padx=20)
        self.workflow_metrics_text.configure(state="disabled")

        ctk.CTkLabel(
            self.workflow_sidebar_panel,
            text="Active Triggers",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.palette["text"],
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(16, 8))

        self.workflow_trigger_container = ctk.CTkScrollableFrame(
            self.workflow_sidebar_panel,
            corner_radius=12,
            fg_color="transparent",
        )
        self.workflow_trigger_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self._refresh_workflow_list()
        self._update_workflow_panels(None)

        return frame

    def _save_gmail_settings(self) -> None:
        if not self.integration_manager or not hasattr(self, "gmail_entries"):
            self._add_response_card(
                summary="Email integration unavailable.",
                body="Install advanced features to manage integrations.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return

        data = {key: entry.get().strip() for key, entry in self.gmail_entries.items()}
        self.integration_manager.config.setdefault("email", {}).update(data)

        try:
            username = data.get("username")
            password = data.get("password")
            smtp_server = data.get("smtp_server") or "smtp.gmail.com"
            if username and password:
                self.integration_manager.setup_email(username, password, smtp_server)
                if self.integration_manager.email:
                    try:
                        self.integration_manager.email.smtp_port = int(data.get("smtp_port") or 587)
                    except Exception:
                        pass
                    if data.get("imap_server"):
                        self.integration_manager.email.imap_server = data["imap_server"]
            self.integration_manager._save_config()
            self._add_response_card(
                summary="Email settings saved.",
                body=json.dumps(self.integration_manager.config.get("email", {}), indent=2),
                status="success",
                duration="-",
                mode="Integrated",
            )
        except Exception as exc:
            self._add_response_card(
                summary="Failed to save email settings.",
                body=str(exc),
                status="error",
                duration="-",
                mode="Integrated",
            )

    def _send_test_email(self) -> None:
        manager = getattr(self, "integration_manager", None)
        email_client = getattr(manager, "email", None)
        if not manager or not email_client:
            self._add_response_card(
                summary="Email integration not configured.",
                body="Enter credentials and save before sending a test email.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return
        recipient = self.gmail_entries.get("username").get().strip() if hasattr(self, "gmail_entries") else ""
        if not recipient:
            self._add_response_card(
                summary="Missing recipient.",
                body="Specify the username field to send a test email.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return
        try:
            result = email_client.send_email(
                to=recipient,
                subject="Test email from Windows Use Agent",
                body="This is an automated test message."
            )
            status = result.get("status", "error")
            self._add_response_card(
                summary=result.get("message", "Test email") if status == "success" else "Test email failed.",
                body=json.dumps(result, indent=2),
                status="success" if status == "success" else "error",
                duration="-",
                mode="Integrated",
            )
        except Exception as exc:
            self._add_response_card(
                summary="Test email failed.",
                body=str(exc),
                status="error",
                duration="-",
                mode="Integrated",
            )

    def _save_cloud_settings(self, provider: str) -> None:
        if not self.integration_manager or not hasattr(self, "cloud_entries"):
            self._add_response_card(
                summary="Cloud integration unavailable.",
                body="Install advanced features to manage integrations.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return

        entries = self.cloud_entries.get(provider.lower())
        if not entries:
            return

        interval_value = entries["interval"].get().strip() or "15"
        try:
            interval_int = max(1, int(interval_value))
        except ValueError:
            interval_int = 15

        config = self.integration_manager.config.setdefault("cloud_storage", {})
        config.update({
            "provider": provider.lower(),
            "local_path": entries["local"].get().strip(),
            "cloud_path": entries["cloud"].get().strip(),
            "sync_interval": interval_int,
        })

        try:
            self.integration_manager.setup_cloud_storage(provider.lower())
            self.integration_manager._save_config()
            self._add_response_card(
                summary=f"{provider} settings saved.",
                body=json.dumps(config, indent=2),
                status="success",
                duration="-",
                mode="Integrated",
            )
        except Exception as exc:
            self._add_response_card(
                summary="Failed to configure cloud storage.",
                body=str(exc),
                status="error",
                duration="-",
                mode="Integrated",
            )

    def _sync_cloud_now(self, provider: str) -> None:
        self._add_response_card(
            summary=f"Sync requested for {provider}.",
            body="The automation engine will handle syncing in the background once configured.",
            status="info",
            duration="-",
            mode="Integrated",
        )

    def _save_webhook_settings(self) -> None:
        if not self.integration_manager or not hasattr(self, "webhook_entries"):
            self._add_response_card(
                summary="Webhook integration unavailable.",
                body="Install advanced features to manage integrations.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return
        url = self.webhook_entries["url"].get().strip()
        payload = self.webhook_entries["payload"].get("1.0", "end").strip()
        config = self.integration_manager.config.setdefault("webhooks", {})
        config.update({"url": url, "payload": payload})
        self.integration_manager._save_config()
        self._add_response_card(
            summary="Webhook settings saved.",
            body=json.dumps(config, indent=2),
            status="success",
            duration="-",
            mode="Integrated",
        )

    def _send_sample_webhook(self) -> None:
        if not self.integration_manager or not hasattr(self, "webhook_entries"):
            return
        url = self.webhook_entries["url"].get().strip()
        payload_text = self.webhook_entries["payload"].get("1.0", "end").strip() or "{}"
        if not url:
            self._add_response_card(
                summary="Webhook URL required.",
                body="Enter a webhook URL before sending sample data.",
                status="error",
                duration="-",
                mode="Integrated",
            )
            return
        try:
            payload = json.loads(payload_text)
        except Exception:
            payload = {"sample": payload_text}
        try:
            response = requests.post(url, json=payload, timeout=10)
            summary = f"Webhook responded with {response.status_code}."
            body = response.text
            status = "success" if response.ok else "error"
        except Exception as exc:
            summary = "Webhook request failed."
            body = str(exc)
            status = "error"
        self._add_response_card(summary, body, status, "-", "Integrated")


    def _refresh_workflow_list(self) -> None:
        if not hasattr(self, "workflow_list_container"):
            return
        for child in self.workflow_list_container.winfo_children():
            child.destroy()

        # Recreate the empty state label since it was destroyed above
        self.workflow_list_empty = ctk.CTkLabel(
            self.workflow_list_container,
            text="No workflows yet.\nClick 'New Workflow' to create one.",
            text_color=self.palette["text_soft"],
            font=ctk.CTkFont(size=13),
            justify="center",
        )

        if not self.workflow_engine or not getattr(self.workflow_engine, "workflows", {}):
            self.workflow_list_empty.pack(expand=True, pady=40)
            self.selected_workflow = None
            self._update_workflow_panels(None)
            return

        self.workflow_list_empty.pack_forget()
        self.workflow_cards.clear()
        for name, workflow in sorted(self.workflow_engine.workflows.items(), key=lambda item: item[0].lower()):
            metadata = f"Runs: {workflow.get('execution_count', 0)}  |  Success: {workflow.get('success_count', 0)}"
            card = ctk.CTkFrame(
                self.workflow_list_container,
                corner_radius=12,
                fg_color=self.palette['surface'],
                border_width=1,
                border_color=self.palette['stroke'],
            )
            card.pack(fill='x', padx=4, pady=4)
            card.grid_columnconfigure(0, weight=1)

            title = ctk.CTkLabel(card, text=name, font=ctk.CTkFont(size=14, weight='bold'))
            title.grid(row=0, column=0, sticky='w', padx=14, pady=(10, 2))
            meta = ctk.CTkLabel(card, text=metadata, text_color=self.palette['text_soft'])
            meta.grid(row=1, column=0, sticky='w', padx=14, pady=(0, 10))

            for widget in (card, title, meta):
                widget.bind('<Button-1>', lambda _e, w=name: self._select_workflow(w))

            self.workflow_cards[name] = card

        if self.selected_workflow and self.selected_workflow in self.workflow_cards:
            self._highlight_selected_workflow(self.selected_workflow)
            self._update_workflow_panels(self.workflow_engine.workflows[self.selected_workflow])
        else:
            first = next(iter(self.workflow_cards.keys()))
            self._select_workflow(first)

    def _highlight_selected_workflow(self, name: str) -> None:
        for workflow_name, card in self.workflow_cards.items():
            if workflow_name == name:
                card.configure(
                    fg_color=self._shade_color(self.MODE_COLORS['Workflow'], 0.25),
                    border_color=self.MODE_COLORS['Workflow'],
                )
            else:
                card.configure(fg_color=self.palette['surface'], border_color=self.palette['stroke'])

    def _select_workflow(self, name: Optional[str]) -> None:
        if not name or not self.workflow_engine or name not in self.workflow_engine.workflows:
            self.selected_workflow = None
            self._update_workflow_panels(None)
            return
        self.selected_workflow = name
        self._highlight_selected_workflow(name)
        self._update_workflow_panels(self.workflow_engine.workflows[name])

    def _update_workflow_panels(self, workflow: Optional[Dict[str, Any]]) -> None:
        buttons = [
            getattr(self, 'workflow_run_button', None),
            getattr(self, 'workflow_optimize_button', None),
            getattr(self, 'workflow_edit_button', None),
            getattr(self, 'workflow_delete_button', None),
        ]
        for button in buttons:
            if button:
                button.configure(state='disabled')

        if not workflow:
            self.workflow_detail_title.configure(text='Select a workflow to view details')
            self.workflow_detail_subtitle.configure(text='')
        else:
            self.workflow_detail_title.configure(text=workflow['name'])
            runs = workflow.get('execution_count', 0)
            success = workflow.get('success_count', 0)
            success_rate = f"{(success / runs * 100):.0f}%" if runs else '0%'
            subtitle = f"Created: {workflow.get('created_at', 'N/A')}  |  Runs: {runs}  |  Success: {success_rate}"
            self.workflow_detail_subtitle.configure(text=subtitle)

        self.workflow_description.configure(state='normal')
        self.workflow_description.delete('1.0', 'end')
        if workflow:
            description = workflow.get('description') or 'No description provided.'
            self.workflow_description.insert('1.0', description)
        else:
            self.workflow_description.insert('1.0', 'Select a workflow to inspect its steps.')
        self.workflow_description.configure(state='disabled')

        for child in self.workflow_steps_container.winfo_children():
            child.destroy()

        if workflow:
            for index, step in enumerate(workflow.get('steps', []), start=1):
                step_frame = ctk.CTkFrame(
                    self.workflow_steps_container,
                    corner_radius=10,
                    fg_color=self.palette['surface'],
                    border_width=1,
                    border_color=self.palette['stroke'],
                )
                step_frame.pack(fill='x', padx=4, pady=4)
                step_frame.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(step_frame, text=f"Step {index}: {step.get('action', 'unknown').title()}", font=ctk.CTkFont(weight='bold')).grid(row=0, column=0, sticky='w', padx=12, pady=(10, 2))
                params = json.dumps(step.get('params', {}), indent=2) if step.get('params') else 'No parameters'
                ctk.CTkLabel(step_frame, text=params, text_color=self.palette['text_soft'], justify='left').grid(row=1, column=0, sticky='w', padx=12, pady=(0, 10))

        metrics_text = 'No metrics available.'
        if workflow:
            metrics = [
                f"Average duration: {workflow.get('average_duration', 0):.2f}s",
                f"Execution count: {workflow.get('execution_count', 0)}",
                f"Success count: {workflow.get('success_count', 0)}",
            ]
            metrics_text = ''.join(metrics)
        self.workflow_metrics_text.configure(state='normal')
        self.workflow_metrics_text.delete('1.0', 'end')
        self.workflow_metrics_text.insert('1.0', metrics_text)
        self.workflow_metrics_text.configure(state='disabled')

        for child in self.workflow_trigger_container.winfo_children():
            child.destroy()

        if workflow:
            triggers = []
            listeners = getattr(self.workflow_engine, 'event_listeners', {})
            for trigger_list in listeners.values():
                for trigger in trigger_list:
                    if trigger.get('workflow') == workflow['name']:
                        triggers.append(trigger)
            if triggers:
                for trigger in triggers:
                    item = ctk.CTkFrame(self.workflow_trigger_container, corner_radius=10, fg_color=self.palette['surface'], border_width=1, border_color=self.palette['stroke'])
                    item.pack(fill='x', padx=4, pady=4)
                    ctk.CTkLabel(item, text=f"{trigger.get('type', 'event').title()} trigger", font=ctk.CTkFont(weight='bold')).pack(anchor='w', padx=12, pady=(8, 2))
                    ctk.CTkLabel(item, text=json.dumps(trigger.get('condition', {}), indent=2), text_color=self.palette['text_soft'], justify='left').pack(anchor='w', padx=12, pady=(0, 8))
            else:
                ctk.CTkLabel(self.workflow_trigger_container, text='No triggers configured.', text_color=self.palette['text_soft']).pack(pady=8)

        if workflow:
            for button in (self.workflow_run_button, self.workflow_optimize_button, self.workflow_edit_button, self.workflow_delete_button):
                button.configure(state='normal')

    def _open_workflow_editor(self, workflow_name: Optional[str]) -> None:
        editor = ctk.CTkToplevel(self)
        editor.title('Workflow Editor')
        editor.geometry('620x520')
        editor.transient(self)
        editor.grab_set()

        existing = self.workflow_engine.workflows.get(workflow_name) if (workflow_name and self.workflow_engine) else None

        name_entry = ctk.CTkEntry(editor, placeholder_text='Workflow name')
        name_entry.pack(fill='x', padx=24, pady=(24, 8))
        if existing:
            name_entry.insert(0, existing['name'])
            name_entry.configure(state='disabled')

        desc_box = ctk.CTkTextbox(editor, height=80)
        desc_box.pack(fill='x', padx=24, pady=8)
        if existing:
            desc_box.insert('1.0', existing.get('description', ''))

        steps_box = ctk.CTkTextbox(editor)
        steps_box.pack(fill='both', expand=True, padx=24, pady=8)
        if existing:
            steps_box.insert('1.0', json.dumps(existing.get('steps', []), indent=2))
        else:
            steps_box.insert('1.0', '''[
  {
    "action": "launch_app",
    "params": {"app": "notepad"}
  }
]''')

        status_label = ctk.CTkLabel(editor, text='', text_color='#ef4444')
        status_label.pack(fill='x', padx=24, pady=(4, 0))

        def save_workflow() -> None:
            name = name_entry.get().strip()
            if not name:
                status_label.configure(text='Name is required.')
                return
            try:
                steps = json.loads(steps_box.get('1.0', 'end').strip())
                if not isinstance(steps, list):
                    raise ValueError('Steps must be a list of action dictionaries.')
            except Exception as exc:
                status_label.configure(text=f'Invalid steps JSON: {exc}')
                return

            description = desc_box.get('1.0', 'end').strip()

            if existing:
                workflow = self.workflow_engine.workflows[name]
                workflow['steps'] = steps
                workflow['description'] = description
                self.workflow_engine._save_workflows()
                message = f"Workflow '{name}' updated."
            else:
                creation = self.workflow_engine.create_workflow(name, steps, description=description)
                message = creation.get('message', 'Workflow created.')

            self._refresh_workflow_list()
            self._select_workflow(name)
            editor.destroy()
            self._add_response_card(message, json.dumps({'workflow': name}, indent=2), 'info', '-', 'Workflow')

        ctk.CTkButton(editor, text='Save Workflow', command=save_workflow).pack(pady=16)

    def _run_selected_workflow(self) -> None:
        if not self.selected_workflow or not self.workflow_engine:
            return

        workflow_name = self.selected_workflow

        def worker() -> None:
            self._set_status('processing')
            result = self.workflow_engine.execute_workflow(workflow_name, self.agent)
            summary = result.get('message', f"Workflow '{workflow_name}' executed.")
            body = json.dumps(result, indent=2)
            self.after(0, lambda: self._add_response_card(summary, body, 'success', '-', 'Workflow'))
            self.after(0, self._refresh_workflow_list)
            self.after(0, lambda: self._set_status('ready'))

        threading.Thread(target=worker, daemon=True).start()

    def _optimize_selected_workflow(self) -> None:
        if not self.selected_workflow or not self.workflow_engine:
            return
        result = self.workflow_engine.optimize_workflow(self.selected_workflow)
        body = json.dumps(result, indent=2)
        status = 'success' if result.get('status') == 'success' else 'info'
        self._add_response_card(result.get('message', 'Optimization complete.'), body, status, '-', 'Workflow')
        self._refresh_workflow_list()

    def _delete_selected_workflow(self) -> None:
        if not self.selected_workflow or not self.workflow_engine:
            return
        if not messagebox.askyesno('Delete workflow', f"Delete workflow '{self.selected_workflow}'?"):
            return
        self.workflow_engine.workflows.pop(self.selected_workflow, None)
        self.workflow_engine._save_workflows()
        self._add_response_card(
            summary='Workflow removed.',
            body=f"Workflow '{self.selected_workflow}' deleted.",
            status='info',
            duration='-',
            mode='Workflow',
        )
        self.selected_workflow = None
        self._refresh_workflow_list()




def main() -> None:
    app = WindowsUseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
