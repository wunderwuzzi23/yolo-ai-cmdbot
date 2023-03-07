@echo off
:: INSTALL_DIR = Directory the "\yolo-ai-cmdbot" will go to
:: SCRIPT_DIR = Directory the "yolo.bat" script will go to
set INSTALL_DIR=%HOME%
set SCRIPT_DIR=%HOME%
set TARGET_DIR=%INSTALL_DIR%yolo-ai-cmdbot\
set TARGET_FULLPATH=%TARGET_DIR%\yolo.py\

:: COMMENT (::) FUNCTIONS YOU DO NOT WANT TO RUN
:: UNCOMMENT FUNCTIONS YOU DO WANT TO RUN
:: DO NOT UNCOMMENT BOTH "call :install_yolo_directory" and "call :install_yolo_repository" (will just overwrite the yolo.bat file)

:: Install Yolo using created directory
call :install_yolo_directory

:: Install Yolo using cloned repository
::call :install_yolo_repository

::Optional functions:

::call :create_openai_apikey

::call :create_safety_off

pause
exit /b 0

:: Installs yolo using created directory
:install_yolo_directory
echo Installing Yolo (Using Created Directory)

call :create_yolo_directory
call :create_yolo_bat_from_directory
call :create_env_in_directory

exit /b 0

::Installs yolo using cloned repositiory
:install_yolo_repository

echo Installing Yolo (Using Cloned Repository)

call :create_yolo_bat_from_repository
call :create_env_in_repository

exit /b 0

:: Creates a directory to hold yolo.py and prompt
:create_yolo_directory
echo Yolo Directory:
echo Installing to %TARGET_DIR%

mkdir %TARGET_DIR%
copy  yolo.py %TARGET_DIR%
copy  prompt.txt %TARGET_DIR%

exit /b 0

:: Create yolo.bat and input code linking to created directory
:create_yolo_bat_from_directory
echo Yolo Batch (Directory):
echo yolo.py should be in %TARGET_DIR%...
if exist %TARGET_FULLPATH% (
    echo Found: Creating "yolo.bat" in %SCRIPT_DIR%

    copy nul yolo.bat
    echo @echo off>"yolo.bat"
    echo python.exe %TARGET_DIR%yolo.py %%*>>"yolo.bat"
    copy  yolo.bat %SCRIPT_DIR%
    del yolo.bat
) else (
    echo Not Found: Aborting "create_yolo_bat_from_directory"
)

exit /b 0

:: Create yolo.bat and input code linking to repository
:create_yolo_bat_from_repository
echo Yolo Batch (Repository):
echo yolo.py should be in %~dp0...
if exist %~dp0\yolo.py (
    echo Found: Creating "yolo.bat" in %SCRIPT_DIR%

    copy nul yolo.bat
    echo @echo off>"yolo.bat"
    echo python.exe %~dp0yolo.py %%*>>"yolo.bat"
    copy  yolo.bat %SCRIPT_DIR%
    del yolo.bat
) else (
    echo Not Found: Aborting "create_yolo_bat_from_repository"
)

exit /b 0

:: Creates the safety off file and puts it in ~ for you (uncomment to work)
:create_safety_off
echo Yolo Safety Off:
echo Creating ".yolo-safety-off" in %HOME%

copy nul .yolo-safety-off
copy .yolo-safety-off %HOME%
del .yolo-safety-off

exit /b 0

:: Creates the .openai.apikey if it doesn't already exists (otherwise, does nothing)
:create_openai_apikey
echo Yolo OpenAi ApiKey:
echo Creating ".open.apikey" (if not already exists) in %HOME%

copy nul .openai.apikey
robocopy %~dp0 %HOME% .openai.apikey /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np
del .openai.apikey

exit /b 0

:: Creates the .env if it doesn't already exists in chosen install directory (otherwise, does nothing)
:create_env_in_directory
echo Yolo .Env:
echo Creating ".env" (if not already exists) in %TARGET_DIR%

if exist .env (
    robocopy %~dp0 %TARGET_DIR% .env /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np
) else (
    copy nul .env
    robocopy %~dp0 %TARGET_DIR% .env /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np
)

exit /b 0

:: Creates the .env if it doesn't already exists in chosen install directory (otherwise, does nothing)
:create_env_in_repository
echo Yolo .Env:
echo Creating ".env" (if not already exists) in %~dp0

if exist .env (
    echo Already Exists
) else (
    copy nul .env
)

exit /b 0