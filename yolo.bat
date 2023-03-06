@echo off

REM Work around to not have to type in python.exe yolo.py every time. 
REM Put in C:/Windows/System32 to allow command to work anywhere

set /P "prompt=Enter Prompt: "
cd ~
python.exe yolo-ai-cmdbot/yolo.py %prompt%