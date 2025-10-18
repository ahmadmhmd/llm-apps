from pydantic import BaseModel,Field
from typing import Literal

class SharedBaseModel(BaseModel):
    class Config:
        extra='allow'

class Done(SharedBaseModel):
    answer:str = Field(...,description="the detailed final answer to the user query in proper markdown format",examples=["The task is completed successfully."])

class Clipboard(SharedBaseModel):
    mode:Literal['copy','paste'] = Field(...,description="the mode of the clipboard",examples=['Copy'])
    text:str = Field(...,description="the text to copy to clipboard",examples=["hello world"])

class Click(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinates of the element to click on.",examples=[(0,0)])
    button:Literal['left','right','middle']=Field(description='The button to click on the element.',default='left',examples=['left'])
    clicks:Literal[0,1,2]=Field(description="The number of times to click on the element. (0 for hover, 1 for single click, 2 for double click)",default=2,examples=[0])

class Shell(SharedBaseModel):
    command:str=Field(...,description="The PowerShell command to execute.",examples=['Get-Process'])

class Type(SharedBaseModel):
    loc:tuple[int,int]=Field(...,description="The coordinates of the element to type on.",examples=[(0,0)])
    text:str=Field(...,description="The text to type on the element.",examples=['hello world'])
    clear:Literal['true','false']=Field(description="To clear the text field before typing.",default='false',examples=['true'])
    caret_position:Literal['start','idle','end']=Field(description="The position of the caret.",default='idle',examples=['start','idle','end'])

class Launch(SharedBaseModel):
    name:str=Field(...,description="The name of the application to launch.",examples=['Google Chrome'])

class Scroll(SharedBaseModel):
    loc:tuple[int,int]|None=Field(description="The coordinates of the element to scroll on. If None, the screen will be scrolled.",default=None,examples=[(0,0)])
    type:Literal['horizontal','vertical']=Field(description="The type of scroll.",default='vertical',examples=['vertical'])
    direction:Literal['up','down','left','right']=Field(description="The direction of the scroll.",default=['down'],examples=['down'])
    wheel_times:int=Field(description="The number of times to scroll.",default=1,examples=[1,2,5])

class Drag(SharedBaseModel):
    from_loc:tuple[int,int]=Field(...,description="The from coordinates of the drag.",examples=[(0,0)])
    to_loc:tuple[int,int]=Field(...,description="The to coordinates of the drag.",examples=[(100,100)])

class Move(SharedBaseModel):
    to_loc:tuple[int,int]=Field(...,description="The coordinates to move to.",examples=[(100,100)])

class Shortcut(SharedBaseModel):
    shortcut:list[str]=Field(...,description="The shortcut to execute by pressing the keys.",examples=[['ctrl','a'],['alt','f4']])

class Key(SharedBaseModel):
    key:str=Field(...,description="The key to press.",examples=['enter'])

class Wait(SharedBaseModel):
    duration:int=Field(...,description="The duration to wait in seconds.",examples=[5])

class Scrape(SharedBaseModel):
    url:str=Field(...,description="The url of the webpage to scrape.",examples=['https://google.com'])

class Screenshot(SharedBaseModel):
    filename:str=Field(...,description="The filename for the screenshot (without extension, .png will be added automatically).",examples=['ai_test','screenshot_2024'])
    folder:Literal['Desktop','Downloads','Documents']=Field(description="The folder to save the screenshot.",default='Downloads',examples=['Downloads'])

class Calculate(SharedBaseModel):
    expression:str=Field(...,description="The mathematical expression to calculate (e.g., '100+1000*200/500+900-350'). Use standard operators: +, -, *, /, (, )",examples=['100+50','(10+5)*2','1000/5+200'])

class WriteFile(SharedBaseModel):
    filename:str=Field(...,description="The name of the file to create (with extension, e.g., 'document.txt', 'notes.md')",examples=['notes.txt','report.md','todo.txt'])
    content:str=Field(...,description="The content to write to the file",examples=['Hello World','Meeting notes:\n- Topic 1\n- Topic 2'])
    folder:Literal['Desktop','Downloads','Documents']=Field(description="The folder where to save the file",default='Desktop',examples=['Desktop'])

class ReadFile(SharedBaseModel):
    filepath:str=Field(...,description="The full path to the file to read, or just filename if in common folders",examples=['C:\\Users\\user\\Desktop\\notes.txt','document.pdf'])

class SearchWeb(SharedBaseModel):
    query:str=Field(...,description="The search query to look up on Google",examples=['Python tutorials','Weather today','Latest AI news'])
    open_browser:bool=Field(description="Whether to open the first result in browser",default=True,examples=[True,False])

class SendEmail(SharedBaseModel):
    to:str=Field(...,description="Recipient email address",examples=['user@example.com'])
    subject:str=Field(...,description="Email subject line",examples=['Meeting Reminder','Project Update'])
    body:str=Field(...,description="Email body content",examples=['Hi,\n\nThis is a reminder...'])

class SystemInfo(SharedBaseModel):
    info_type:Literal['battery','memory','disk','cpu','network','all']=Field(description="Type of system information to retrieve",default='all',examples=['battery','all'])

class OpenURL(SharedBaseModel):
    url:str=Field(...,description="The URL to open in default browser (include http:// or https://)",examples=['https://google.com','https://github.com'])

class FileOperation(SharedBaseModel):
    operation:Literal['create_folder','delete','rename','move','copy']=Field(...,description="The file operation to perform")
    source:str=Field(...,description="Source file/folder path",examples=['C:\\Users\\user\\Desktop\\old_file.txt'])
    destination:str=Field(None,description="Destination path (for move/copy/rename operations)",examples=['C:\\Users\\user\\Documents\\new_file.txt'])

class TextToSpeech(SharedBaseModel):
    text:str=Field(...,description="The text to convert to speech",examples=['Hello, how are you?','This is a test message'])
    
class Reminder(SharedBaseModel):
    message:str=Field(...,description="The reminder message",examples=['Call John','Submit report'])
    minutes:int=Field(...,description="Number of minutes until reminder",examples=[5,30,60])

class WeatherInfo(SharedBaseModel):
    location:str=Field(None,description="City name or 'current' for current location",examples=['New York','London','current'])

class TranslateText(SharedBaseModel):
    text:str=Field(...,description="Text to translate",examples=['Hello world','Good morning'])
    target_language:str=Field(...,description="Target language code (en, es, fr, de, ar, etc.)",examples=['es','fr','ar'])

class MemoryOperation(SharedBaseModel):
    operation:Literal['save_template','load_template','list_templates','delete_template','recent_history','search_history','statistics','clear_history']=Field(...,description="Memory operation to perform")
    template_name:str=Field(None,description="Name of the template (for save/load/delete operations)",examples=['daily_workflow','report_routine'])
    command:str=Field(None,description="Command to save as template",examples=['Take screenshot and create report'])
    description:str=Field(None,description="Description of the template",examples=['Daily morning routine'])
    search_query:str=Field(None,description="Query to search in history",examples=['screenshot','calculator'])
    count:int=Field(5,description="Number of history items to return",examples=[5,10,20])

class OCRTool(SharedBaseModel):
    image_path:str=Field(...,description="Path to image file to extract text from",examples=['C:\\Users\\user\\Desktop\\image.png','screenshot.jpg'])

class PDFOperation(SharedBaseModel):
    operation:Literal['merge','split','extract_text','compress']=Field(...,description="PDF operation to perform")
    input_files:list[str]=Field(...,description="Input PDF file path(s)",examples=[['C:\\Users\\user\\Desktop\\file1.pdf','file2.pdf']])
    output_file:str=Field(...,description="Output file path",examples=['C:\\Users\\user\\Desktop\\merged.pdf'])
    pages:str=Field(None,description="Page range for split operation (e.g., '1-5', '1,3,5')",examples=['1-5','1,3,5'])