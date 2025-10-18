# 🪟 Windows Use Agent - Complete Documentation

**The Ultimate Guide: From Zero to Enterprise**

Version 2.0 Enterprise Edition | Last Updated: October 2025

---

## 📋 Table of Contents

### Getting Started
1. [Quick Start (3 Steps)](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)

### Core Features (Basic)
4. [29 Essential Tools](#core-tools)
5. [Command Examples](#command-examples)
6. [Desktop GUI Application](#desktop-gui)
7. [Voice & Text Input](#voice-and-text-input)

### Enterprise Features (Advanced)
8. [Smart Workflow Engine](#smart-workflow-engine)
9. [Context-Aware Intelligence](#context-aware-intelligence)
10. [Security & Permission System](#security-system)
11. [Ecosystem Integration](#ecosystem-integration)

### Reference
12. [Troubleshooting](#troubleshooting)
13. [API Reference](#api-reference)
14. [Configuration Guide](#configuration-guide)

---

# 🚀 Quick Start

## 3 Steps to Get Running

### Step 1: Install (30 seconds)
```bash
install.bat
```
This installs **everything**: core, GUI, voice, workflows, security, integrations.

### Step 2: Configure API Key
1. Copy `.env-example` to `.env`
2. Get API key: https://aistudio.google.com/app/apikey
3. Add to `.env`: `GOOGLE_API_KEY=your_key_here`

### Step 3: Launch
```bash
start.bat
```

**That's it!** The professional desktop app will open. 🎉

---

# 💻 Installation

## System Requirements
- **OS**: Windows 10/11
- **Python**: 3.12+ (recommended)
- **RAM**: 4GB minimum
- **Internet**: Required for LLM API

## Full Installation

### Automated (Recommended)
```bash
install.bat
```

Installs:
- ✅ Core agent framework (langchain, windows-use)
- ✅ Desktop GUI (customtkinter)
- ✅ Voice input (SpeechRecognition, sounddevice)
- ✅ Smart workflows (watchdog, schedule)
- ✅ Context awareness (psutil, pywin32)
- ✅ Security layer (cryptography)
- ✅ Integrations (requests, dotenv)

### Manual Installation
```bash
pip install -e .
```

All dependencies are defined in `pyproject.toml`.

---

# ⚙️ Configuration

## Environment Variables

Create `.env` file in project root:

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional - Email Integration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993

# Optional - Cloud Storage
ONEDRIVE_PATH=C:/Users/YourName/OneDrive
GOOGLE_DRIVE_PATH=C:/Users/YourName/Google Drive

# Optional - Webhooks
WEBHOOK_URL=https://your-webhook-url.com/endpoint
```

## Get API Keys

**Google Gemini API:**
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env`

**Gmail App Password** (for email integration):
1. Enable 2FA on your Google account
2. Visit: https://myaccount.google.com/apppasswords
3. Create app password for "Mail"
4. Use this password in `.env` (not your regular password)

---

# 🛠️ Core Tools

## 29 Essential Tools in 6 Categories

### 1️⃣ Core GUI Automation (13 tools)

| Tool | Purpose | Example Command |
|------|---------|----------------|
| **Click** | Click UI elements | `"Click Save button"` |
| **Type** | Type text anywhere | `"Type 'Hello World' in notepad"` |
| **Launch** | Open applications | `"Launch Chrome"` |
| **Shell** | Run PowerShell commands | `"List files in Documents"` |
| **Clipboard** | Copy/paste operations | `"Copy this to clipboard"` |
| **Shortcut** | Keyboard shortcuts | `"Press Ctrl+C"` |
| **Scroll** | Scroll windows | `"Scroll down 5 times"` |
| **Drag** | Drag and drop | `"Drag file to Downloads"` |
| **Move** | Move cursor | `"Move mouse to (500, 300)"` |
| **Key** | Press specific keys | `"Press Enter key"` |
| **Wait** | Add delays | `"Wait 3 seconds"` |
| **Done** | Mark task complete | `"Task finished"` |
| **Scrape** | Extract web content | `"Scrape text from webpage"` |

### 2️⃣ Productivity Tools (4 tools)

| Tool | Purpose | Speed | Example |
|------|---------|-------|---------|
| **Screenshot** | Capture screen | <1s | `"Take screenshot as report_Q4"` |
| **Calculate** | Fast math | 2-3s | `"Calculate 1500+2300+1800"` |
| **Write File** | Create documents | Instant | `"Write notes to todo.txt"` |
| **Read File** | Read contents | Instant | `"Read my shopping list"` |

### 3️⃣ Web & Research (3 tools)

| Tool | Purpose | Example |
|------|---------|---------|
| **Search Web** | Google search | `"Search for Python tutorials"` |
| **Open URL** | Open websites | `"Open github.com"` |
| **Scrape** | Extract article text | `"Get content from URL"` |

### 4️⃣ System Management (2 tools)

| Tool | Purpose | Example |
|------|---------|---------|
| **System Info** | Check system status | `"Check battery level"` |
| **File Operations** | Manage files/folders | `"Create folder Projects"` |

### 5️⃣ Advanced Features (4 tools)

| Tool | Purpose | Example |
|------|---------|---------|
| **Text-to-Speech** | Speak aloud | `"Read this text aloud"` |
| **Reminders** | Time-based alerts | `"Remind me in 30 minutes"` |
| **Weather** | Get forecast | `"What's the weather today?"` |
| **Translate** | 100+ languages | `"Translate 'Hello' to Spanish"` |

### 6️⃣ Intelligence Layer (3 tools)

| Tool | Purpose | Example |
|------|---------|---------|
| **Memory** | Remember commands | `"Show my recent commands"` |
| **OCR** | Image-to-text | `"Extract text from image"` |
| **PDF** | Merge/split/extract | `"Merge these 3 PDFs"` |

---

# 💡 Command Examples

## Basic Tasks

### Open Applications
```
"Open Notepad"
"Launch Chrome"
"Open Calculator"
"Start Task Manager"
"Open File Explorer"
```

### Screenshots
```
"Take a screenshot"
"Screenshot and save as dashboard_Q4"
"Capture current window"
```

### Calculations
```
"Calculate 100+200+300"
"What's 15% of 1500?"
"Calculate total: 450+680+320"
```

### File Operations
```
"Create notes.txt with my tasks"
"Read todo.txt file"
"Create folder called Projects"
"Copy file to Desktop"
```

### Web Tasks
```
"Search for AI news"
"Open YouTube"
"Search for Python tutorials"
"Open reddit.com"
```

## Intermediate Tasks

### Multi-Step Operations
```
"Open Notepad and write 'Hello World'"
"Search for Python tutorials and open first result"
"Take screenshot and save as report"
"Open Calculator and compute 125*8"
```

### System Info
```
"Check battery level"
"Show system info"
"List running processes"
"Check disk space"
```

### Advanced Automation
```
"Open Excel, type 'Sales Report' in A1, and save as Q4_Report"
"Search for weather forecast and read results aloud"
"Take screenshot, extract text with OCR, and save to file"
```

---

# 🖥️ Desktop GUI

## Professional Enterprise Interface

### UI Layout

```
┌─────────────────┬──────────────────────────────────────────────┐
│                 │  🪟 Windows Use - Enterprise Agent          │
│  🪟 Windows Use │  Basic Commands                              │
│  Enterprise     │  Execute simple Windows tasks      🎤 Voice  │
│                 ├──────────────────────────────────────────────┤
│  System Status  │                                              │
│  ● Agent Ready  │  Command Input                               │
│  ● Advanced     │  [Type your command...        ] [Execute]    │
│                 │                                              │
│  Operation Mode │  Agent Response                              │
│  [Basic ▼]      │  ┌────────────────────────────────────────┐ │
│                 │  │ 👋 Welcome! I'm your Windows agent     │ │
│  Quick Actions  │  │                                        │ │
│  📋 History     │  │ I can help you with:                   │ │
│  🔄 Workflow    │  │  • Basic tasks                         │ │
│  🧠 Context     │  │  • Smart workflows                     │ │
│  🔒 Security    │  │  • Context awareness                   │ │
│  🌐 Integration │  │  • Secure operations                   │ │
│                 │  │  • Integrations                        │ │
│  v2.0 Enterprise│  └────────────────────────────────────────┘ │
│  © 2025         │                                              │
│                 │  💡 Example Commands                         │
│                 │  [Open Notepad] [Search AI] [Screenshot]    │
└─────────────────┴──────────────────────────────────────────────┘
```

### 5 Operation Modes

**1. Basic Mode**
- Simple Windows tasks
- Open apps, screenshots, searches
- Perfect for beginners

**2. Workflow Mode**
- Create automated task chains
- Record and replay actions
- Event-driven triggers

**3. Context-Aware Mode**
- Learn your habits
- Predict next actions
- Smart suggestions

**4. Secure Mode**
- Permission management
- Sandbox testing
- Undo operations

**5. Integrated Mode**
- Email operations
- Cloud storage
- Webhooks & APIs

### Features

#### Left Sidebar
- **System Status** - Real-time agent health
- **Mode Selector** - Switch between 5 modes
- **Quick Actions** - One-click access to features
- **Version Info** - Edition and build number

#### Main Content
- **Dynamic Title** - Changes per mode
- **Large Input Field** - Type or paste commands
- **Execute Button** - Green, prominent CTA
- **Response Area** - Scrollable output with timestamps
- **Example Grid** - 8 contextual examples per mode

#### Top Bar
- **Voice Button** - Record voice commands (if available)
- **Status Indicator** - Ready/Working/Error states

---

# 🎤 Voice and Text Input

## Voice Input

### How to Use
1. **Click** 🎤 Voice button (top right)
2. **Wait** for "Listening..." indicator (button turns red)
3. **Speak** clearly: "Open Notepad"
4. **See** transcription below input
5. **View** result in response area

### Voice Examples
- "Open Calculator"
- "Search for AI news"
- "Take a screenshot"
- "What's the weather?"

### Voice Not Available?
If voice button is disabled:
- sounddevice not installed (rare - usually auto-installs)
- **Use text input instead** - works perfectly!
- Run `install.bat` to install all dependencies

## Text Input

### How to Use
1. **Type** command in input field
2. **Press Enter** OR click "Execute" button
3. **View** result in response area

### Quick Examples
- Click any example button
- Command auto-fills and executes
- Learn by trying!

---

# 🔄 Smart Workflow Engine

**Phase 5: Autonomous Automation**

## What It Does

- **Auto-detect Intent** - Understands goals from natural language
- **Conditional Execution** - "If battery < 20% then skip video processing"
- **Workflow Recording** - "Watch me do this and automate it"
- **Event-driven Triggers** - Run on file changes, time, or system events
- **Self-optimization** - Learns which approaches work best

## Commands

### Auto-detect Intent
```
"Prepare my report"
→ Detects: research → analyze → format → share

"Backup my files"
→ Detects: check space → compress → copy → verify
```

### Create Workflow
```python
from windows_use.agent.workflow_engine import SmartWorkflowEngine

engine = SmartWorkflowEngine()

# Create workflow
workflow = engine.create_workflow(
    name="morning_routine",
    steps=[
        {"action": "check_weather", "params": {}},
        {"action": "open_email", "params": {}},
        {"action": "read_calendar", "params": {}}
    ],
    description="My morning startup routine"
)
```

### Record Workflow
```
"Start recording workflow"
[Perform your actions...]
"Stop recording as 'backup_workflow'"
```

### Add Triggers

**Time-based:**
```
"Run backup_workflow every Friday at 4PM"
"Execute morning_routine daily at 8AM"
```

**Event-based:**
```
"Run screenshot_workflow when file changes in Documents"
"Execute cleanup_workflow when Downloads > 100 files"
```

**System-based:**
```
"If battery < 20%, close heavy apps"
"When memory > 90%, clear cache"
```

### Execute Workflow
```
"Run my morning_routine"
"Execute backup_workflow"
"Start workflow: generate_report"
```

### List Workflows
```
"Show all workflows"
"List my workflows"
```

## Real-World Examples

### Business Reporting
```python
workflow = engine.create_workflow(
    name="weekly_report",
    steps=[
        {"action": "open_excel", "params": {"file": "sales_data.xlsx"}},
        {"action": "calculate_metrics", "params": {}},
        {"action": "create_charts", "params": {}},
        {"action": "generate_pdf", "params": {}},
        {"action": "email_team", "params": {"to": "team@company.com"}}
    ]
)

# Set trigger
engine.add_trigger(
    workflow_name="weekly_report",
    trigger_type="time",
    schedule="every Friday at 5PM"
)
```

### File Management
```python
workflow = engine.create_workflow(
    name="organize_downloads",
    steps=[
        {"action": "scan_folder", "params": {"path": "Downloads"}},
        {"action": "move_pdfs", "params": {"to": "Documents"}},
        {"action": "move_images", "params": {"to": "Pictures"}},
        {"action": "delete_temp", "params": {}}
    ]
)

# Conditional trigger
engine.add_trigger(
    workflow_name="organize_downloads",
    trigger_type="condition",
    condition="file_count > 100"
)
```

### Morning Routine
```
"Create morning routine: check weather, open email, read calendar, start music"

"Set trigger: run morning_routine every weekday at 8AM"
```

---

# 🧠 Context-Aware Intelligence

**Phase 6: Learning Your Habits**

## What It Does

- **Cross-app Tracking** - Monitors your workflow patterns
- **Temporal Awareness** - "You usually use Excel at 2PM on Mondays"
- **Predictive Suggestions** - "You might need Slack next"
- **Smart Resource Management** - Closes unused apps to save memory
- **Habit Learning** - Builds profile of your work patterns

## Features

### App Usage Tracking
```
"What apps do I use most?"
"Show my app usage stats"
"When do I use Excel?"
```

**Response:**
```
📊 Your App Usage Patterns:

Most Used Apps:
1. VS Code (45% of time)
2. Chrome (30%)
3. Slack (15%)
4. Excel (10%)

Time Patterns:
• Excel: Mon-Fri, 2-4 PM (reporting hours)
• Slack: Throughout day (communication)
• VS Code: Mon-Fri, 9 AM-6 PM (coding hours)
```

### Pattern Recognition
```
"Show my morning patterns"
"What do I do after lunch?"
"Predict my workflow"
```

**Response:**
```
🔮 Your Morning Pattern (8-10 AM):

1. Check email (Outlook) - 8:00 AM
2. Review calendar (Google Calendar) - 8:15 AM
3. Team standup (Zoom) - 9:00 AM
4. Start coding (VS Code) - 9:30 AM

Confidence: 87% (observed 18/21 days)
```

### Smart Suggestions
```
"Suggest what I need next"
"What should I work on?"
"Predict my next task"
```

**Response:**
```
💡 Based on your patterns:

It's 2:15 PM Monday - you typically:
1. Open Excel for weekly report
2. Pull data from accounting system
3. Generate charts
4. Email to management

Would you like me to start your report workflow?
```

### Resource Optimization
```
"Optimize my system"
"Close unused apps"
"Free up memory"
```

**Response:**
```
🔧 Resource Optimization:

Closed 5 apps not used in 2+ hours:
• Photoshop (saving 1.2GB RAM)
• OBS Studio (saving 800MB RAM)
• Old Chrome tabs (saving 600MB RAM)

System Performance:
• RAM: 87% → 62% (freed 2.6GB)
• CPU: 45% → 28% (closed background tasks)
```

## Usage Examples

### Track Work Patterns
```python
from windows_use.agent.context_manager import ContextManager

manager = ContextManager()

# Get insights
insights = manager.get_insights()
print(f"Most used app: {insights['top_app']}")
print(f"Peak hours: {insights['peak_hours']}")
print(f"Work patterns: {insights['patterns']}")
```

### Predict Next Action
```python
# Based on current time and history
prediction = manager.predict_next_action()
print(f"You might need: {prediction['app']}")
print(f"Confidence: {prediction['confidence']}%")
```

### Get Time-based Suggestions
```python
# Get suggestions for current time
suggestions = manager.get_suggestions()
for suggestion in suggestions:
    print(f"• {suggestion['action']} - {suggestion['reason']}")
```

---

# 🔒 Security System

**Phase 7: Enterprise-Grade Protection**

## What It Does

- **Granular Permissions** - File/system/network/registry access control
- **Sandbox Mode** - Test commands safely
- **Undo Stack** - Reverse last 50 actions
- **Encrypted Storage** - Secure credential management
- **Backup Points** - Create/restore system snapshots
- **Audit Trail** - Track all operations

## Features

### Permission System

**Check Permissions:**
```
"Show my permissions"
"What can the agent do?"
"Check security status"
```

**Set Permissions:**
```python
from windows_use.agent.security import SecurityManager

security = SecurityManager()

# Grant permissions
security.set_permission("file_write", True)
security.set_permission("system_modify", False)
security.set_permission("network_access", True)
```

**Permission Levels:**
- `file_read` - Read files
- `file_write` - Write/modify files
- `file_delete` - Delete files
- `system_modify` - Change system settings
- `network_access` - Internet operations
- `registry_modify` - Windows registry changes

### Sandbox Mode

**Enable Sandbox:**
```
"Enable sandbox mode"
"Test in sandbox"
```

**In sandbox:**
- All operations simulated
- No real system changes
- Preview results safely
- Perfect for testing

**Disable Sandbox:**
```
"Disable sandbox mode"
"Exit sandbox"
```

### Undo Operations

**Undo Last Action:**
```
"Undo last action"
"Undo that"
"Reverse previous command"
```

**Undo Multiple:**
```
"Undo last 5 actions"
"Undo everything from today"
```

**View History:**
```
"Show undo history"
"What can I undo?"
```

### Protected Paths

**Set Protected:**
```python
# Prevent accidental deletion
security.add_protected_path("C:/Important/Projects")
security.add_protected_path("C:/Users/YourName/Documents")
```

**Try to Delete:**
```
"Delete everything in Projects folder"
→ ❌ Blocked: Projects is a protected path
```

### Encrypted Secrets

**Store Secret:**
```python
# Encrypt and store sensitive data
security.store_secret("api_key", "sk-1234567890abcdef")
security.store_secret("db_password", "SuperSecure123!")
```

**Retrieve Secret:**
```python
api_key = security.get_secret("api_key")
# Returns decrypted value
```

### Backup Points

**Create Backup:**
```
"Create backup point"
"Save current state as 'before_cleanup'"
```

**List Backups:**
```
"Show all backups"
"List backup points"
```

**Restore Backup:**
```
"Restore from backup: before_cleanup"
"Undo to last backup"
```

## Security Best Practices

### 1. Start with Minimal Permissions
```python
security = SecurityManager()
# Only grant what's needed
security.set_permission("file_read", True)
security.set_permission("file_write", False)
```

### 2. Use Sandbox for Testing
```
"Enable sandbox mode"
[Test your commands]
"If looks good, disable sandbox and run for real"
```

### 3. Create Backups Before Big Changes
```
"Create backup point: before_system_cleanup"
[Make changes]
"If something breaks: restore from backup"
```

### 4. Review Audit Trail
```
"Show today's operations"
"What did the agent do?"
```

---

# 🌐 Ecosystem Integration

**Phase 8: Connect Everything**

## What It Does

- **Email Operations** - Send/receive emails with attachments
- **Cloud Storage** - Upload/download from OneDrive/Google Drive
- **Webhooks** - Trigger external services
- **Custom APIs** - Integrate with your tools

## Email Integration

### Setup

Add to `.env`:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

### Send Email
```
"Send email to john@company.com with subject 'Report' and body 'See attached'"
"Email screenshot to team@company.com"
```

### Send with Attachment
```
"Email report.pdf to boss@company.com"
"Send Q4_results.xlsx to team with subject 'Results'"
```

### Bulk Email
```python
from windows_use.agent.integrations import IntegrationManager

manager = IntegrationManager()

recipients = ["person1@company.com", "person2@company.com"]
manager.email.bulk_send(
    recipients=recipients,
    subject="Team Update",
    body="Here's the weekly update...",
    attachments=["report.pdf"]
)
```

### Check Emails
```
"Check my emails"
"Read unread messages"
"Show emails from yesterday"
```

## Cloud Storage

### Setup

Add to `.env`:
```env
ONEDRIVE_PATH=C:/Users/YourName/OneDrive
GOOGLE_DRIVE_PATH=C:/Users/YourName/Google Drive
```

### Upload File
```
"Upload report.pdf to cloud"
"Save screenshot to OneDrive"
"Back up Documents folder to cloud"
```

### Download File
```
"Download report.pdf from cloud"
"Get latest backup from OneDrive"
```

### List Files
```
"List files in cloud"
"Show OneDrive contents"
```

### Sync Folder
```python
# Continuous sync
manager.cloud.sync_folder(
    local_path="C:/Projects",
    cloud_path="OneDrive/Projects",
    interval=300  # seconds
)
```

## Webhooks

### Setup

Add to `.env`:
```env
WEBHOOK_URL=https://your-webhook-url.com/endpoint
```

### Trigger Webhook
```
"Send webhook when task completes"
"Trigger webhook with status: success"
```

### Custom Webhook
```python
manager.webhook.trigger(
    url="https://api.slack.com/webhook/abc123",
    data={
        "text": "Task completed successfully!",
        "channel": "#automation",
        "username": "Windows Agent"
    }
)
```

### Webhook on Event
```python
# Trigger webhook when file changes
manager.webhook.on_file_change(
    path="C:/Reports",
    webhook_url="https://your-url.com/notify",
    data={"event": "file_changed"}
)
```

## Real-World Integration Examples

### Automated Reporting
```python
# Generate report and email
workflow = engine.create_workflow(
    name="auto_report",
    steps=[
        {"action": "generate_report", "params": {"format": "pdf"}},
        {"action": "upload_cloud", "params": {"service": "onedrive"}},
        {"action": "email_team", "params": {
            "recipients": ["team@company.com"],
            "subject": "Weekly Report",
            "attach_cloud_link": True
        }},
        {"action": "trigger_webhook", "params": {
            "url": "https://slack.com/webhook/123",
            "message": "Report generated and shared"
        }}
    ]
)
```

### File Backup System
```python
# Back up important files to cloud daily
workflow = engine.create_workflow(
    name="daily_backup",
    steps=[
        {"action": "compress_folder", "params": {"path": "Documents"}},
        {"action": "upload_cloud", "params": {"service": "google_drive"}},
        {"action": "send_confirmation", "params": {
            "to": "you@email.com",
            "subject": "Backup Complete"
        }}
    ]
)

engine.add_trigger(
    workflow_name="daily_backup",
    trigger_type="time",
    schedule="daily at 6PM"
)
```

---

# 🔧 Troubleshooting

## Installation Issues

### ❌ "Module not found" errors

**Solution:**
```bash
# Run full installer
install.bat

# Or install manually
pip install -e .
```

### ❌ Voice input not working

**Solution:**

Voice input uses `sounddevice` which is cross-platform compatible and works on all Python versions.

If voice button is disabled:
```bash
# Reinstall dependencies
install.bat
```

If still not working:
- **Use text input** (recommended) - works perfectly
- Check microphone permissions in Windows Settings
- Verify microphone is working in other apps

### ❌ "GOOGLE_API_KEY not found"

**Solution:**
1. Copy `.env-example` to `.env`
2. Get key: https://aistudio.google.com/app/apikey
3. Add: `GOOGLE_API_KEY=your_key_here`

## Voice Input Issues

### ❌ Microphone button disabled or not working

**Solution:**
```bash
# Ensure all dependencies installed
install.bat
```

**Check:**
- Voice uses `sounddevice` (works on all Python versions)
- Microphone permissions enabled in Windows Settings
- Use text input as alternative (always works)

### ❌ "Listening..." but no response

**Check:**
1. Microphone permissions (Windows Settings → Privacy)
2. Correct microphone selected
3. Background noise levels
4. Try text input as alternative

## Performance Issues

### ❌ Agent is slow

**Solutions:**

1. **Screenshot tool slow:**
   - Already optimized (<1 second)
   - Update to latest code

2. **Calculator tool slow:**
   - Already optimized (2-3 seconds)
   - Uses keyboard input now

3. **Too many apps open:**
   - Use context-aware cleanup: `"Close unused apps"`
   - Enable resource optimization

### ❌ Out of memory

**Solution:**
```
"Optimize my system"
"Free up memory"
"Close apps not used in 2 hours"
```

## Advanced Feature Issues

### ❌ Advanced features not available

**Check if installed:**
```
"Check system status"
```

**If not showing:**
```bash
# Reinstall with all features
install.bat
```

**Verify installation:**
```python
try:
    from windows_use.agent.workflow_engine import SmartWorkflowEngine
    print("✅ Workflows available")
except ImportError:
    print("❌ Workflows not installed")
```

### ❌ Workflows not executing

**Check:**
1. Workflow exists: `"List workflows"`
2. Triggers configured: `"Show triggers"`
3. Permissions granted: `"Check permissions"`

### ❌ Context manager not learning

**Solution:**
- Runs in background automatically
- Needs 3-5 days to build patterns
- Check: `"Show my patterns"`

## Common Errors

### ❌ "Permission denied"

**Solution:**
```
"Grant file_write permission"
"Enable system_modify permission"
```

### ❌ "Sandbox mode active"

**Solution:**
```
"Disable sandbox mode"
```

Operations were simulated, not real.

### ❌ "Protected path"

**Solution:**
Path is protected for safety. To modify:
```python
security.remove_protected_path("C:/Important/Folder")
```

---

# 📚 API Reference

## Core Agent

### Initialize Agent
```python
from windows_use.agent import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
agent = Agent(
    instructions=["Custom instructions here"],
    llm=llm,
    use_vision=True
)
```

### Execute Command
```python
result = agent.invoke(query="Open Notepad")
print(result.content)
```

## Smart Workflow Engine

### Initialize
```python
from windows_use.agent.workflow_engine import SmartWorkflowEngine

engine = SmartWorkflowEngine()
```

### Create Workflow
```python
workflow = engine.create_workflow(
    name="workflow_name",
    steps=[
        {"action": "action1", "params": {"key": "value"}},
        {"action": "action2", "params": {}}
    ],
    description="What this workflow does"
)
```

### Execute Workflow
```python
result = engine.execute_workflow("workflow_name")
```

### Add Trigger
```python
# Time-based
engine.add_trigger(
    workflow_name="my_workflow",
    trigger_type="time",
    schedule="every day at 9AM"
)

# File-based
engine.add_trigger(
    workflow_name="my_workflow",
    trigger_type="file_change",
    path="C:/Documents"
)

# Condition-based
engine.add_trigger(
    workflow_name="my_workflow",
    trigger_type="condition",
    condition="battery < 20"
)
```

### List Workflows
```python
workflows = engine.list_workflows()
for workflow in workflows:
    print(f"{workflow['name']}: {workflow['description']}")
```

## Context Manager

### Initialize
```python
from windows_use.agent.context_manager import ContextManager

manager = ContextManager()
```

### Get App Usage
```python
stats = manager.get_app_usage()
print(f"Most used: {stats['top_app']}")
print(f"Usage time: {stats['hours']}")
```

### Get Patterns
```python
patterns = manager.get_patterns()
for pattern in patterns:
    print(f"{pattern['time']}: {pattern['action']}")
```

### Predict Next Action
```python
prediction = manager.predict_next_action()
print(f"Suggested: {prediction['app']}")
print(f"Confidence: {prediction['confidence']}%")
```

### Get Suggestions
```python
suggestions = manager.get_suggestions()
for suggestion in suggestions:
    print(f"• {suggestion['action']}")
```

## Security Manager

### Initialize
```python
from windows_use.agent.security import SecurityManager

security = SecurityManager()
```

### Permissions
```python
# Set permission
security.set_permission("file_write", True)

# Check permission
has_perm = security.check_permission("file_write")

# Get all permissions
perms = security.get_all_permissions()
```

### Sandbox Mode
```python
# Enable
security.enable_sandbox()

# Disable
security.disable_sandbox()

# Check status
is_sandbox = security.is_sandbox_active()
```

### Undo Operations
```python
# Undo last action
security.undo()

# Undo multiple
security.undo(count=5)

# View history
history = security.get_undo_history()
```

### Protected Paths
```python
# Add protection
security.add_protected_path("C:/Important")

# Remove protection
security.remove_protected_path("C:/Important")

# List protected
paths = security.get_protected_paths()
```

### Secrets
```python
# Store secret (encrypted)
security.store_secret("api_key", "secret_value")

# Retrieve secret (decrypted)
value = security.get_secret("api_key")

# Delete secret
security.delete_secret("api_key")
```

### Backup Points
```python
# Create backup
backup_id = security.create_backup("before_cleanup")

# List backups
backups = security.list_backups()

# Restore backup
security.restore_backup(backup_id)
```

## Integration Manager

### Initialize
```python
from windows_use.agent.integrations import IntegrationManager

manager = IntegrationManager()
```

### Email
```python
# Send email
manager.email.send(
    to="recipient@email.com",
    subject="Subject",
    body="Message body",
    attachments=["file.pdf"]
)

# Send to multiple
manager.email.bulk_send(
    recipients=["user1@email.com", "user2@email.com"],
    subject="Subject",
    body="Message"
)

# Check emails
emails = manager.email.check_inbox(unread_only=True)
```

### Cloud Storage
```python
# Upload file
manager.cloud.upload("local_file.pdf", "cloud_folder")

# Download file
manager.cloud.download("cloud_file.pdf", "local_folder")

# List files
files = manager.cloud.list_files("cloud_folder")

# Sync folder
manager.cloud.sync_folder(
    local_path="C:/Projects",
    cloud_path="OneDrive/Projects"
)
```

### Webhooks
```python
# Trigger webhook
manager.webhook.trigger(
    url="https://your-webhook.com/endpoint",
    data={"key": "value"}
)

# Register webhook
manager.webhook.register(
    name="my_webhook",
    url="https://your-webhook.com/endpoint"
)

# Trigger by name
manager.webhook.trigger_by_name(
    "my_webhook",
    data={"status": "success"}
)
```

---

# ⚙️ Configuration Guide

## Desktop GUI Customization

Edit `main_desktop_gui.py`:

### Change Theme
```python
# Line 14
ctk.set_appearance_mode("dark")  # "dark", "light", "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

### Change Window Size
```python
# Line 23
self.geometry("1400x900")  # width x height
```

### Change Sidebar Width
```python
# Line 107
self.sidebar = ctk.CTkFrame(self.main_container, width=280)
```

## Workflow Engine Configuration

```python
engine = SmartWorkflowEngine(
    max_workflows=100,  # Maximum stored workflows
    auto_optimize=True,  # Enable self-optimization
    retry_on_fail=True,  # Retry failed steps
    max_retries=3        # Maximum retry attempts
)
```

## Context Manager Configuration

```python
manager = ContextManager(
    tracking_enabled=True,     # Enable usage tracking
    learning_enabled=True,      # Enable habit learning
    prediction_enabled=True,    # Enable predictions
    min_confidence=0.7,        # Minimum prediction confidence
    history_days=30            # Days of history to keep
)
```

## Security Manager Configuration

```python
security = SecurityManager(
    default_permissions={
        "file_read": True,
        "file_write": False,
        "file_delete": False,
        "system_modify": False,
        "network_access": True,
        "registry_modify": False
    },
    undo_limit=50,            # Maximum undo operations
    backup_retention=7,        # Days to keep backups
    encryption_enabled=True    # Encrypt sensitive data
)
```

## Integration Manager Configuration

```python
manager = IntegrationManager(
    email_config={
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "imap_server": "imap.gmail.com",
        "imap_port": 993
    },
    cloud_config={
        "provider": "onedrive",  # or "google_drive"
        "sync_interval": 300     # seconds
    },
    webhook_config={
        "timeout": 30,           # seconds
        "retry_on_fail": True
    }
)
```

---

# 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Desktop GUI (CTk)                    │
│  • Voice/Text Input  • Mode Selector  • Response View  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Core Agent (LangChain)                │
│  • LLM Integration  • Tool Selection  • Vision Support  │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────┘
   │      │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│29   ││Smart││Cont-││Secu-││Inte-││OCR  ││PDF  ││More │
│Core ││Work-││ext  ││rity ││gra- ││Image││Ops  ││Tools│
│Tools││flows││Mgr  ││Mgr  ││tions││2Text││     ││     │
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
```

---

# 🚀 What's Next?

## Start Using Now

1. **Install**: `install.bat`
2. **Configure**: Add API key to `.env`
3. **Launch**: `start.bat`
4. **Try basic commands** first
5. **Explore advanced features** as you get comfortable

## Learning Path

**Week 1: Basics**
- Open apps
- Take screenshots
- Search web
- Basic file operations

**Week 2: Workflows**
- Create first workflow
- Add time trigger
- Record actions
- Automate routine tasks

**Week 3: Context**
- Let it learn your patterns
- Use smart suggestions
- Optimize system resources

**Week 4: Enterprise**
- Set up permissions
- Configure integrations
- Create backup points
- Full automation

## Get Help

- **Quick Start**: This guide's beginning
- **Examples**: See "Command Examples" section
- **Troubleshooting**: See "Troubleshooting" section
- **Visual Roadmap**: `EVOLUTION_ROADMAP.md`

---

# 📄 License & Credits

## License
MIT License - See LICENSE file for details

## Built With
- **LangChain** - Agent framework
- **Google Gemini** - LLM provider
- **CustomTkinter** - Modern GUI
- **Python 3.12+** - Core language

## Version
**2.0 Enterprise Edition** - October 2025

---

**Built with ❤️ for Windows automation**

**Ready to transform how you work? Let's go! 🚀**
