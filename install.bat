@echo off
:: Installs yolo in the user's home directory

::TARGET_DIR=~/yolo-ai-cmdbot  
::TARGET_FULLPATH=$TARGET_DIR/yolo.py
set TARGET_DIR= %HOME%yolo-ai-cmdbot
set TARGET_FULLPATH= %TARGET_DIR%\yolo.py

::mkdir -p $TARGET_DIR
::cp yolo.py prompt.txt $TARGET_DIR
::chmod +x $TARGET_FULLPATH
mkdir %TARGET_DIR%
copy yolo.py %TARGET_DIR%
copy prompt.txt %TARGET_DIR%

:: Windows: Copies .bat file to $HOME so it works similar to LINUX/MAC, avoiding having to type python.exe every time.
:: Note: Though that maybe making it an executable would make more sense but the 

::Copy to home directory
copy yolo.bat %HOME%