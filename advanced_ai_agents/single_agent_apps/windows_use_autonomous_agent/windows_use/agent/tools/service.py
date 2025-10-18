from windows_use.agent.tools.views import (
    Click, Type, Launch, Scroll, Drag, Move, Shortcut, Key, Wait, Scrape, Done, 
    Clipboard, Shell, Screenshot, Calculate, WriteFile, ReadFile, SearchWeb, 
    SendEmail, SystemInfo, OpenURL, FileOperation, TextToSpeech, Reminder, 
    WeatherInfo, TranslateText, MemoryOperation, OCRTool, PDFOperation
)
from windows_use.desktop import Desktop
from humancursor import SystemCursor
from markdownify import markdownify
from langchain.tools import tool
from typing import Literal
import uiautomation as ua
import pyperclip as pc
import pyautogui as pg
import requests
import os
import shutil
import psutil
import webbrowser
import threading
import time
from datetime import datetime, timedelta

cursor=SystemCursor()

@tool('Done Tool',args_schema=Done)
def done_tool(answer:str,desktop:Desktop=None):
    '''To indicate that the task is completed'''
    return answer

@tool('Launch Tool',args_schema=Launch)
def launch_tool(name: str,desktop:Desktop=None) -> str:
    'Launch an application present in start menu (e.g., "notepad", "calculator", "chrome")'
    _,status=desktop.launch_app(name)
    if status!=0:
        return f'Failed to launch {name.title()}.'
    else:
        return f'Launched {name.title()}.'

@tool('Shell Tool',args_schema=Shell)
def shell_tool(command: str,desktop:Desktop=None) -> str:
    'Execute PowerShell commands and return the output with status code'
    response,status=desktop.execute_command(command)
    return f'Status Code: {status}\nResponse: {response}'

@tool('Clipboard Tool',args_schema=Clipboard)
def clipboard_tool(mode: Literal['copy', 'paste'], text: str = None,desktop:Desktop=None)->str:
    'Copy text to clipboard or retrieve current clipboard content. Use "copy" mode with text parameter to copy, "paste" mode to retrieve.'
    if mode == 'copy':
        if text:
            pc.copy(text)  # Copy text to system clipboard
            return f'Copied "{text}" to clipboard'
        else:
            raise ValueError("No text provided to copy")
    elif mode == 'paste':
        clipboard_content = pc.paste()  # Get text from system clipboard
        return f'Clipboard Content: "{clipboard_content}"'
    else:
        raise ValueError('Invalid mode. Use "copy" or "paste".')

@tool('Click Tool',args_schema=Click)
def click_tool(loc:tuple[int,int],button:Literal['left','right','middle']='left',clicks:int=1,desktop:Desktop=None)->str:
    'Click on UI elements at specific coordinates. Supports left/right/middle mouse buttons and single/double/triple clicks. Use coordinates from State-Tool output.'
    x,y=loc
    cursor.move_to(loc)
    control=desktop.get_element_under_cursor()
    pg.click(button=button,clicks=clicks)
    num_clicks={1:'Single',2:'Double',3:'Triple'}
    return f'{num_clicks.get(clicks)} {button} Clicked on {control.Name} Element with ControlType {control.ControlTypeName} at ({x},{y}).'

@tool('Type Tool',args_schema=Type)
def type_tool(loc:tuple[int,int],text:str,clear:str='false',caret_position:Literal['start','idle','end']='idle',desktop:Desktop=None):
    'Type text into input fields, text areas, or focused elements. Set clear=True to replace existing text, False to append. Click on target element coordinates first.'
    x,y=loc
    cursor.click_on(loc)
    control=desktop.get_element_under_cursor()
    if caret_position == 'start':
        pg.press('home')
    elif caret_position == 'end':
        pg.press('end')
    else:
        pass
    if clear=='true':
        pg.hotkey('ctrl','a')
        pg.press('backspace')
    pg.typewrite(text,interval=0.1)
    return f'Typed {text} on {control.Name} Element with ControlType {control.ControlTypeName} at ({x},{y}).'

@tool('Scroll Tool',args_schema=Scroll)
def scroll_tool(loc:tuple[int,int]=None,type:Literal['horizontal','vertical']='vertical',direction:Literal['up','down','left','right']='down',wheel_times:int=1,desktop:Desktop=None)->str:
    'Scroll at specific coordinates or current mouse position. Use wheel_times to control scroll amount (1 wheel = ~3-5 lines). Essential for navigating lists, web pages, and long content.'
    if loc:
        cursor.move_to(loc)
    match type:
        case 'vertical':
            match direction:
                case 'up':
                    ua.WheelUp(wheel_times)
                case 'down':
                    ua.WheelDown(wheel_times)
                case _:
                    return 'Invalid direction. Use "up" or "down".'
        case 'horizontal':
            match direction:
                case 'left':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    ua.WheelUp(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case 'right':
                    pg.keyDown('Shift')
                    pg.sleep(0.05)
                    ua.WheelDown(wheel_times)
                    pg.sleep(0.05)
                    pg.keyUp('Shift')
                case _:
                    return 'Invalid direction. Use "left" or "right".'
        case _:
            return 'Invalid type. Use "horizontal" or "vertical".'
    return f'Scrolled {type} {direction} by {wheel_times} wheel times.'

@tool('Drag Tool',args_schema=Drag)
def drag_tool(from_loc:tuple[int,int],to_loc:tuple[int,int],desktop:Desktop=None)->str:
    'Drag and drop operation from source coordinates to destination coordinates. Useful for moving files, resizing windows, or drag-and-drop interactions.'
    control=desktop.get_element_under_cursor()
    x1,y1=from_loc
    x2,y2=to_loc
    cursor.drag_and_drop(from_loc,to_loc)
    return f'Dragged the {control.Name} element with ControlType {control.ControlTypeName} from ({x1},{y1}) to ({x2},{y2}).'

@tool('Move Tool',args_schema=Move)
def move_tool(to_loc:tuple[int,int],desktop:Desktop=None)->str:
    'Move mouse cursor to specific coordinates without clicking. Useful for hovering over elements or positioning cursor before other actions.'
    x,y=to_loc
    cursor.move_to(to_loc)
    return f'Moved the mouse pointer to ({x},{y}).'

@tool('Shortcut Tool',args_schema=Shortcut)
def shortcut_tool(shortcut:list[str],desktop:Desktop=None):
    'Execute keyboard shortcuts using key combinations. Pass keys as list (e.g., ["ctrl", "c"] for copy, ["alt", "tab"] for app switching, ["win", "r"] for Run dialog).'
    pg.hotkey(*shortcut)
    return 'Pressed ' + '+'.join(shortcut) + '.'

@tool('Key Tool',args_schema=Key)
def key_tool(key:str='',desktop:Desktop=None)->str:
    'Press individual keyboard keys. Supports special keys like "enter", "escape", "tab", "space", "backspace", "delete", arrow keys ("up", "down", "left", "right"), function keys ("f1"-"f12").'
    pg.press(key)
    return f'Pressed the key {key}.'

@tool('Wait Tool',args_schema=Wait)
def wait_tool(duration:int,desktop:Desktop=None)->str:
    'Pause execution for specified duration in seconds. Useful for waiting for applications to load, animations to complete, or adding delays between actions.'
    pg.sleep(duration)
    return f'Waited for {duration} seconds.'

@tool('Scrape Tool',args_schema=Scrape)
def scrape_tool(url:str,desktop:Desktop=None)->str:
    'Fetch and convert webpage content to markdown format. Provide full URL including protocol (http/https). Returns structured text content suitable for analysis.'
    response=requests.get(url,timeout=10)
    html=response.text
    content=markdownify(html=html)
    return f'Scraped the contents of the entire webpage:\n{content}'

@tool('Screenshot Tool',args_schema=Screenshot)
def screenshot_tool(filename:str,folder:Literal['Desktop','Downloads','Documents']='Downloads',desktop:Desktop=None)->str:
    'Take a screenshot of the entire screen and save it to the specified folder. Fast and efficient - completes in under 1 second.'
    # Get the folder path
    folder_map = {
        'Desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
        'Downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
        'Documents': os.path.join(os.path.expanduser('~'), 'Documents')
    }
    folder_path = folder_map.get(folder, folder_map['Downloads'])
    
    # Ensure filename has .png extension
    if not filename.endswith('.png'):
        filename = f'{filename}.png'
    
    # Full path
    filepath = os.path.join(folder_path, filename)
    
    # Take screenshot using pyautogui (fast and reliable)
    screenshot = pg.screenshot()
    screenshot.save(filepath)
    
    return f'Screenshot saved successfully to: {filepath}'

@tool('Calculate Tool',args_schema=Calculate)
def calculate_tool(expression:str,desktop:Desktop=None)->str:
    'Open Windows Calculator and input a mathematical expression, then return the result. Much faster and more reliable than clicking calculator buttons. Handles complex expressions with +, -, *, /, and parentheses.'
    try:
        # Launch calculator if not already open
        _,status = desktop.launch_app('calculator')
        pg.sleep(1)  # Wait for calculator to open
        
        # Clear any existing input (Ctrl+A, Delete)
        pg.hotkey('ctrl', 'a')
        pg.sleep(0.1)
        pg.press('delete')
        pg.sleep(0.2)
        
        # Type the expression directly
        # Calculator accepts keyboard input for math expressions
        pg.typewrite(expression, interval=0.05)
        pg.sleep(0.2)
        
        # Press Enter to calculate
        pg.press('enter')
        pg.sleep(0.3)
        
        # Try to read result by selecting all and copying
        pg.hotkey('ctrl', 'c')
        pg.sleep(0.2)
        
        # Get result from clipboard
        result = pc.paste()
        
        return f'Expression: {expression}\nResult: {result}'
        
    except Exception as e:
        return f'Error calculating: {str(e)}\n\nTip: Make sure Calculator is accessible and expression uses valid operators (+, -, *, /, parentheses)'

@tool('Write File Tool',args_schema=WriteFile)
def write_file_tool(filename:str,content:str,folder:Literal['Desktop','Downloads','Documents']='Desktop',desktop:Desktop=None)->str:
    'Create and write content to a text file. Perfect for notes, documents, todos, reports. Supports txt, md, csv, json, and other text formats.'
    try:
        folder_map = {
            'Desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
            'Downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'Documents': os.path.join(os.path.expanduser('~'), 'Documents')
        }
        folder_path = folder_map.get(folder, folder_map['Desktop'])
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f'✅ File created successfully!\nPath: {filepath}\nSize: {len(content)} characters'
    except Exception as e:
        return f'❌ Error creating file: {str(e)}'

@tool('Read File Tool',args_schema=ReadFile)
def read_file_tool(filepath:str,desktop:Desktop=None)->str:
    'Read and return the contents of a text file. Works with txt, md, csv, json, log, and other text formats.'
    try:
        # If just filename provided, check common folders
        if not os.path.isabs(filepath):
            for folder in ['Desktop', 'Downloads', 'Documents']:
                folder_path = os.path.join(os.path.expanduser('~'), folder)
                test_path = os.path.join(folder_path, filepath)
                if os.path.exists(test_path):
                    filepath = test_path
                    break
        
        if not os.path.exists(filepath):
            return f'❌ File not found: {filepath}'
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f'📄 File: {os.path.basename(filepath)}\n📍 Path: {filepath}\n📏 Size: {len(content)} characters\n\n📝 Content:\n{content}'
    except Exception as e:
        return f'❌ Error reading file: {str(e)}'

@tool('Search Web Tool',args_schema=SearchWeb)
def search_web_tool(query:str,open_browser:bool=True,desktop:Desktop=None)->str:
    'Search Google and optionally open first result. Perfect for quick research, finding information, or opening websites.'
    try:
        search_url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
        
        if open_browser:
            webbrowser.open(search_url)
            return f'🔍 Searched for: "{query}"\n🌐 Opening Google search results in browser...'
        else:
            return f'🔍 Search URL: {search_url}\n💡 Use open_browser=True to open automatically'
    except Exception as e:
        return f'❌ Error searching: {str(e)}'

@tool('Open URL Tool',args_schema=OpenURL)
def open_url_tool(url:str,desktop:Desktop=None)->str:
    'Open any website URL in the default browser. Fast way to access websites, web apps, or online resources.'
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        webbrowser.open(url)
        return f'🌐 Opened URL: {url}\n✅ Browser launched successfully'
    except Exception as e:
        return f'❌ Error opening URL: {str(e)}'

@tool('System Info Tool',args_schema=SystemInfo)
def system_info_tool(info_type:Literal['battery','memory','disk','cpu','network','all']='all',desktop:Desktop=None)->str:
    'Get detailed system information including battery, memory, disk space, CPU usage, and network stats. Essential for system monitoring.'
    try:
        info = []
        
        if info_type in ['battery', 'all']:
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info.append(f'🔋 Battery: {battery.percent}% {"(Charging)" if battery.power_plugged else "(Discharging)"}')
                    if not battery.power_plugged:
                        info.append(f'   Time remaining: {battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m')
            except:
                info.append('🔋 Battery: Not available')
        
        if info_type in ['memory', 'all']:
            memory = psutil.virtual_memory()
            info.append(f'🧠 RAM: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)')
        
        if info_type in ['disk', 'all']:
            disk = psutil.disk_usage('C:\\')
            info.append(f'💾 Disk: {disk.percent}% used ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB free)')
        
        if info_type in ['cpu', 'all']:
            cpu_percent = psutil.cpu_percent(interval=1)
            info.append(f'⚙️ CPU: {cpu_percent}% usage ({psutil.cpu_count()} cores)')
        
        if info_type in ['network', 'all']:
            net = psutil.net_io_counters()
            info.append(f'🌐 Network: ↓{net.bytes_recv // (1024**2)}MB received, ↑{net.bytes_sent // (1024**2)}MB sent')
        
        return '\n'.join(info)
    except Exception as e:
        return f'❌ Error getting system info: {str(e)}'

@tool('File Operation Tool',args_schema=FileOperation)
def file_operation_tool(operation:Literal['create_folder','delete','rename','move','copy'],source:str,destination:str=None,desktop:Desktop=None)->str:
    'Perform file and folder operations: create folders, delete files/folders, rename, move, or copy. Essential for file management.'
    try:
        if operation == 'create_folder':
            os.makedirs(source, exist_ok=True)
            return f'📁 Folder created: {source}'
        
        if not os.path.exists(source):
            return f'❌ Source not found: {source}'
        
        if operation == 'delete':
            if os.path.isfile(source):
                os.remove(source)
                return f'🗑️ File deleted: {source}'
            else:
                shutil.rmtree(source)
                return f'🗑️ Folder deleted: {source}'
        
        if operation in ['rename', 'move', 'copy'] and not destination:
            return f'❌ Destination required for {operation} operation'
        
        if operation == 'rename':
            os.rename(source, destination)
            return f'✏️ Renamed: {source} → {destination}'
        
        if operation == 'move':
            shutil.move(source, destination)
            return f'📦 Moved: {source} → {destination}'
        
        if operation == 'copy':
            if os.path.isfile(source):
                shutil.copy2(source, destination)
            else:
                shutil.copytree(source, destination)
            return f'📋 Copied: {source} → {destination}'
            
    except Exception as e:
        return f'❌ Error in {operation}: {str(e)}'

@tool('Text to Speech Tool',args_schema=TextToSpeech)
def text_to_speech_tool(text:str,desktop:Desktop=None)->str:
    'Convert text to speech and play it aloud using Windows built-in TTS. Great for announcements, notifications, or accessibility.'
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return f'🔊 Spoke: "{text[:100]}{"..." if len(text) > 100 else ""}"'
    except ImportError:
        return '❌ pyttsx3 not installed. Install with: pip install pyttsx3'
    except Exception as e:
        return f'❌ Error in text-to-speech: {str(e)}'

@tool('Reminder Tool',args_schema=Reminder)
def reminder_tool(message:str,minutes:int,desktop:Desktop=None)->str:
    'Set a reminder that will show a notification after specified minutes. Perfect for time-sensitive tasks and reminders.'
    try:
        def show_reminder():
            time.sleep(minutes * 60)
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(
                    "⏰ Reminder",
                    message,
                    duration=10,
                    threaded=True
                )
            except:
                # Fallback to messagebox
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, message, "⏰ Reminder", 0x40)
        
        thread = threading.Thread(target=show_reminder, daemon=True)
        thread.start()
        
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        return f'⏰ Reminder set!\n📝 Message: "{message}"\n⏱️ Will alert at: {reminder_time.strftime("%I:%M %p")}\n⌚ In {minutes} minutes'
    except Exception as e:
        return f'❌ Error setting reminder: {str(e)}'

@tool('Weather Info Tool',args_schema=WeatherInfo)
def weather_info_tool(location:str=None,desktop:Desktop=None)->str:
    """Get weather information for the configured user location or a specified city."""
    try:
        display_name = None
        if not location or location.strip().lower() == 'current':
            city = os.getenv('WINDOWS_USE_CITY')
            region = os.getenv('WINDOWS_USE_REGION')
            country = os.getenv('WINDOWS_USE_COUNTRY')
            lat = os.getenv('WINDOWS_USE_LAT') or os.getenv('WINDOWS_USE_LATITUDE')
            lon = os.getenv('WINDOWS_USE_LON') or os.getenv('WINDOWS_USE_LONGITUDE')
            if lat and lon:
                location = f"{lat},{lon}"
                display_name = ", ".join(part for part in [city, region, country] if part) or f"{lat},{lon}"
            elif city:
                parts = [city, region, country]
                location = ",".join(part for part in parts if part)
                display_name = ", ".join(part for part in parts if part)
            else:
                try:
                    loc_response = requests.get('https://ipapi.co/json/', timeout=5)
                    loc_response.raise_for_status()
                    loc_data = loc_response.json()
                    location = loc_data.get('city') or loc_data.get('region') or 'New York'
                    display_name = loc_data.get('city') or loc_data.get('region') or location
                except Exception:
                    location = 'New York'
                    display_name = 'New York'
        else:
            display_name = location

        url = f'https://wttr.in/{location}?format=j1'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data['current_condition'][0]
        weather_desc = current['weatherDesc'][0]['value']
        temp_c = current['temp_C']
        temp_f = current['temp_F']
        feels_like_c = current['FeelsLikeC']
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']

        name = display_name or location
        lines = [
            f"Weather in {name}:",
            f"Temperature: {temp_c} C ({temp_f} F)",
            f"Feels like: {feels_like_c} C",
            f"Conditions: {weather_desc}",
            f"Humidity: {humidity}%",
            f"Wind: {wind_speed} km/h",
        ]
        timezone = os.getenv('WINDOWS_USE_TIMEZONE')
        if timezone:
            lines.append(f"Timezone: {timezone}")

        return "\n".join(lines)
    except Exception as exc:
        return f"Error getting weather: {exc}\nTry specifying a different city or check your network connection."
@tool('Translate Text Tool',args_schema=TranslateText)
def translate_text_tool(text:str,target_language:str,desktop:Desktop=None)->str:
    'Translate text to any language. Supports 100+ languages including Spanish (es), French (fr), German (de), Arabic (ar), Chinese (zh), Japanese (ja), etc.'
    try:
        from deep_translator import GoogleTranslator
        
        translator = GoogleTranslator(source='auto', target=target_language)
        translated = translator.translate(text)
        
        lang_names = {
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ar': 'Arabic',
            'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'ru': 'Russian',
            'pt': 'Portuguese', 'it': 'Italian', 'hi': 'Hindi', 'tr': 'Turkish'
        }
        lang_name = lang_names.get(target_language, target_language.upper())
        
        return f'🌐 Translation to {lang_name}:\n\n📝 Original: {text}\n✨ Translated: {translated}'
    except ImportError:
        return '❌ deep-translator not installed. Install with: pip install deep-translator'
    except Exception as e:
        return f'❌ Error translating: {str(e)}\n💡 Check language code (es, fr, de, ar, zh, ja, etc.)'

@tool('Memory Operation Tool',args_schema=MemoryOperation)
def memory_operation_tool(operation:str,template_name:str=None,command:str=None,description:str=None,search_query:str=None,count:int=5,desktop:Desktop=None)->str:
    'Manage agent memory: save/load task templates, view command history, search past commands, get statistics. Perfect for repeating workflows!'
    try:
        from windows_use.agent.memory import AgentMemory
        
        memory = AgentMemory()
        
        if operation == 'save_template':
            if not template_name or not command:
                return '❌ Need template_name and command to save template'
            return memory.save_template(template_name, command, description or '')
        
        elif operation == 'load_template':
            if not template_name:
                return '❌ Need template_name to load template'
            cmd = memory.get_template(template_name)
            if cmd:
                return f'✅ Template loaded: {cmd}'
            return f'❌ Template "{template_name}" not found'
        
        elif operation == 'list_templates':
            templates = memory.list_templates()
            if not templates:
                return '📋 No saved templates yet\n💡 Save a template with: save_template operation'
            result = '📋 Saved Templates:\n\n'
            for t in templates:
                result += f'📌 {t["name"]}\n'
                result += f'   📝 {t["description"] or "No description"}\n'
                result += f'   🔧 Command: {t["command"]}\n'
                result += f'   📊 Used: {t["usage_count"]} times\n\n'
            return result
        
        elif operation == 'delete_template':
            if not template_name:
                return '❌ Need template_name to delete'
            return memory.delete_template(template_name)
        
        elif operation == 'recent_history':
            history = memory.get_recent_commands(count)
            if not history:
                return '📋 No command history yet'
            result = f'📜 Last {len(history)} Commands:\n\n'
            for i, entry in enumerate(history, 1):
                status = '✅' if entry['success'] else '❌'
                result += f'{status} {i}. {entry["command"]}\n'
                result += f'   ⏰ {entry["timestamp"][:19]}\n\n'
            return result
        
        elif operation == 'search_history':
            if not search_query:
                return '❌ Need search_query to search history'
            matches = memory.search_history(search_query, count)
            if not matches:
                return f'🔍 No results for "{search_query}"'
            result = f'🔍 Search Results for "{search_query}":\n\n'
            for i, entry in enumerate(matches, 1):
                status = '✅' if entry['success'] else '❌'
                result += f'{status} {i}. {entry["command"]}\n'
                result += f'   ⏰ {entry["timestamp"][:19]}\n\n'
            return result
        
        elif operation == 'statistics':
            stats = memory.get_statistics()
            result = '📊 Agent Memory Statistics:\n\n'
            result += f'📈 Total Commands: {stats["total_commands"]}\n'
            result += f'✅ Successful: {stats["successful"]}\n'
            result += f'❌ Failed: {stats["failed"]}\n'
            result += f'🎯 Success Rate: {stats["success_rate"]}\n'
            result += f'📋 Templates Saved: {stats["templates_saved"]}\n\n'
            if stats['most_used_tools']:
                result += '🔥 Most Used Tools:\n'
                for tool, count in stats['most_used_tools']:
                    result += f'   • {tool}: {count} times\n'
            return result
        
        elif operation == 'clear_history':
            return memory.clear_history()
        
        else:
            return f'❌ Unknown operation: {operation}'
    
    except Exception as e:
        return f'❌ Error: {str(e)}'

@tool('OCR Tool',args_schema=OCRTool)
def ocr_tool(image_path:str,desktop:Desktop=None)->str:
    'Extract text from images using OCR (Optical Character Recognition). Perfect for reading screenshots, scanned documents, photos with text.'
    try:
        try:
            from PIL import Image
            import pytesseract
        except ImportError:
            return '❌ OCR libraries not installed\n💡 Install with: pip install pillow pytesseract\n💡 Also download Tesseract-OCR from: https://github.com/UB-Mannheim/tesseract/wiki'
        
        # Check if file exists
        if not os.path.exists(image_path):
            # Try common folders
            common_folders = [
                os.path.join(os.path.expanduser('~'), 'Desktop'),
                os.path.join(os.path.expanduser('~'), 'Downloads'),
                os.path.join(os.path.expanduser('~'), 'Documents')
            ]
            
            for folder in common_folders:
                full_path = os.path.join(folder, image_path)
                if os.path.exists(full_path):
                    image_path = full_path
                    break
            else:
                return f'❌ Image not found: {image_path}\n💡 Provide full path or place in Desktop/Downloads/Documents'
        
        # Open image and extract text
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        
        if not text.strip():
            return '⚠️ No text detected in image\n💡 Make sure image contains readable text'
        
        return f'📸 Text Extracted from Image:\n\n{text}'
    
    except Exception as e:
        return f'❌ Error reading image: {str(e)}\n💡 Make sure Tesseract-OCR is installed'

@tool('PDF Operation Tool',args_schema=PDFOperation)
def pdf_operation_tool(operation:str,input_files:list[str],output_file:str,pages:str=None,desktop:Desktop=None)->str:
    'Perform PDF operations: merge multiple PDFs, split pages, extract text, compress files. Essential for document management!'
    try:
        try:
            from PyPDF2 import PdfReader, PdfWriter, PdfMerger
        except ImportError:
            return '❌ PyPDF2 not installed\n💡 Install with: pip install PyPDF2'
        
        if operation == 'merge':
            # Merge multiple PDFs
            merger = PdfMerger()
            for pdf_file in input_files:
                if not os.path.exists(pdf_file):
                    return f'❌ File not found: {pdf_file}'
                merger.append(pdf_file)
            
            merger.write(output_file)
            merger.close()
            return f'✅ Merged {len(input_files)} PDFs into: {output_file}'
        
        elif operation == 'split':
            # Split PDF into pages
            if len(input_files) != 1:
                return '❌ Split operation requires exactly 1 input file'
            
            reader = PdfReader(input_files[0])
            total_pages = len(reader.pages)
            
            # Parse page range
            if pages:
                if '-' in pages:
                    start, end = map(int, pages.split('-'))
                    page_list = range(start-1, min(end, total_pages))
                else:
                    page_list = [int(p)-1 for p in pages.split(',')]
            else:
                page_list = range(total_pages)
            
            writer = PdfWriter()
            for page_num in page_list:
                writer.add_page(reader.pages[page_num])
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            return f'✅ Extracted {len(page_list)} pages to: {output_file}'
        
        elif operation == 'extract_text':
            # Extract all text from PDF
            if len(input_files) != 1:
                return '❌ Extract text requires exactly 1 input file'
            
            reader = PdfReader(input_files[0])
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n\n'
            
            # Save to text file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            return f'✅ Extracted text from PDF to: {output_file}\n\n📄 Preview:\n{text[:500]}...'
        
        elif operation == 'compress':
            # Compress PDF by removing unnecessary data
            reader = PdfReader(input_files[0])
            writer = PdfWriter()
            
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            
            original_size = os.path.getsize(input_files[0]) / 1024
            compressed_size = os.path.getsize(output_file) / 1024
            reduction = ((original_size - compressed_size) / original_size) * 100
            
            return f'✅ PDF compressed!\n📁 Original: {original_size:.1f} KB\n📁 Compressed: {compressed_size:.1f} KB\n📉 Reduced by: {reduction:.1f}%'
        
        else:
            return f'❌ Unknown operation: {operation}\n💡 Available: merge, split, extract_text, compress'
    
    except Exception as e:
        return f'❌ Error: {str(e)}'