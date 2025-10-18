"""Tooltip widget for CustomTkinter."""

from typing import Optional
import customtkinter as ctk


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
