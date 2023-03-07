@echo off
:: Installs yolo in the user's home directory

set TARGET_DIR= %HOME%yolo-ai-cmdbot
set TARGET_FULLPATH= %TARGET_DIR%\yolo.py

mkdir %TARGET_DIR%
copy yolo.py %TARGET_DIR%
copy prompt.txt %TARGET_DIR%

:: Windows: Creates a yolo.bat file into %HOME% directory which will let you run similar to Linux/MacOS
:: Example: Input: ".\yolo.bat print hello" to "yolo print hello"

:: yolo.bat can only be used in same directory; or, any directory if put in a $PATH directory (type $env:PATH in PowerShell and pick an appropriate path to paste in)
:: C:\Windows\System32 is the $PATH directory everyone is likely to have

:: Create yolo.bat and if it isn't already there input its code.
find "@echo off" "%HOME%\yolo.bat" && (
    echo "yolo.bat" Already Exists
) || (
    copy /y nul %HOME% yolo.bat
    echo @echo off>>"%HOME%yolo.bat"
    echo python.exe %HOME%yolo-ai-cmdbot\yolo.py %%*>>"%HOME%\yolo.bat"
    echo Created "yolo.bat" in %HOME%
)