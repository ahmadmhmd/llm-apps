"""Application constants and configuration."""

from typing import Dict, List

# Placeholder texts for command input
PLACEHOLDER_ROTATION = [
    "Open Notepad",
    "Take screenshot",
    "Search for AI news",
    "Email latest report",
    "List active windows",
]

# Color scheme for different modes
MODE_COLORS = {
    "Basic": "#2563eb",
    "Workflow": "#f97316",
    "Context": "#22c55e",
    "Secure": "#ef4444",
    "Integrated": "#a855f7",
}

# Navigation items (name, icon, tooltip)
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

# Example commands for each mode
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

# Quick command buttons
QUICK_COMMANDS = [
    "Open Notepad",
    "Search AI News",
    "Screenshot",
    "Check Weather",
    "List Open Windows",
]

# Application color palette (light, dark)
COLOR_PALETTE = {
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
