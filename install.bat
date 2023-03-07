@echo off
setlocal enabledelayedexpansion
:: Note: "~" or %HOME% is equivalent to "%HOMEDRIVE%%HOMEPATH%\" but the latter is set in VM environments (from what I can tell)

:: INSTALL_DIR = Directory the "yolo-ai-cmdbot\" will go to.
:: SCRIPT_DIR = Directory the "yolo.bat" script will go to.
:: createDIR = Whether or not a seperate "yolo-ai-cmdbot\" directory will be made/used to hold "yolo.py" and "prompt.txt". 1=Yes, 2=Just_use_Repo (the folder this is in)
:: createAPIKEY = Whether to create a ".openai.apikey" at %HOMEDRIVE%%HOMEPATH%\. 1=Yes, 2=No
:: createSafetyOff = Whether to create a ".yolo-safety-off" at %HOMEDRIVE%%HOMEPATH%\. 1=Yes, 2=No

:: Default values:
set "INSTALL_DIR=%HOMEDRIVE%%HOMEPATH%\"
set "SCRIPT_DIR=%HOMEDRIVE%%HOMEPATH%\"
set /a "createDIR=1"
set /a "createAPIKEY=2"
set /a "createSafetyOff=2"
set "installing=1"

:: Set Variables To User Defined If Needed 
:: (This was as painful to make as it looks)
choice /n /c YNCO /m "Do you want to install with default settings (or (C)ancel) (or create (O)ptional files)? <Y/N/C/O>:"
set installing=%ERRORLEVEL%
goto :choice_default_!ERRORLEVEL!
:choice_default_2
choice /n /c YN /m "Do you want to install a seperate 'yolo-ai-cmdbot\' directory (otherwise will use this repository folder)? <Y/N>:"
set /a createDIR=%ERRORLEVEL%
goto :choice_use_directory_!ERRORLEVEL!
:choice_use_directory_1
choice /n /c NY /m "Currently 'yolo-ai-cmdbot\' will be made in '!INSTALL_DIR!' . Is this OK? <Y/N>:"
goto :choice_install_!ERRORLEVEL!
:choice_install_1
set /p INSTALL_DIR="Enter a path for 'yolo-ai-cmdbot\' to be made:"
goto :choice_use_directory_1
:choice_install_2
:choice_use_directory_2
choice /n /c NY /m "Currently 'yolo.bat' will be made in '!SCRIPT_DIR!' . Is this OK? <Y/N>:"
goto :choice_script_!ERRORLEVEL!
:choice_script_1
set /p SCRIPT_DIR="Enter a path for 'yolo.bat' to be made:"
goto :choice_use_directory_2
:choice_script_2
:choice_default_1
set "TARGET_DIR=!INSTALL_DIR!\yolo-ai-cmdbot\"
set "TARGET_FULLPATH=!TARGET_DIR!\yolo.py"

::Actually Install
cls
if /i %createDIR%==1 ( call :install_yolo_directory ) else ( call :install_yolo_repository )

::Optional files:
:choice_default_4
choice /n /c YN /m "Do you want to make a '.openai.apikey' file at %HOMEDRIVE%%HOMEPATH%\ to hold your apikey? <Y/N>:"
set /a createAPIKEY=!ERRORLEVEL!
choice /n /c YN /m "Do you want to make a '.yolo-safety-off' file at %HOMEDRIVE%%HOMEPATH%\ to disable safety? <Y/N>:"
set /a createSafetyOff=!ERRORLEVEL!

if /i !createAPIKEY!==1 ( call :create_openai_apikey )
if /i !createSafetyOff!==1 ( call :create_safety_off )

::Show a guide
if /i !installing!==1 ( call :print_guide )
if /i !installing!==2 ( call :print_guide )

:choice_default_3
pause
goto :EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::                                              Functions                                                             ::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::                                             Installation                                                           ::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Installs yolo using created directory
:install_yolo_directory
echo Installing Yolo (Using Created Directory)
call :create_yolo_directory
call :create_yolo_bat_from_directory
call :create_env_in_directory
goto :EOF

::Installs yolo using cloned repositiory
:install_yolo_repository
echo Installing Yolo (Using Cloned Repository)
call :create_yolo_bat_from_repository
call :create_env_in_repository
goto :EOF

:: Creates a directory to hold yolo.py and prompt.txt
:create_yolo_directory
echo Yolo Directory:
echo Installing to !TARGET_DIR!
mkdir !TARGET_DIR!
copy  %~dp0\yolo.py !TARGET_DIR!
copy  %~dp0\prompt.txt !TARGET_DIR!
goto :EOF

:: Create yolo.bat and input code linking to created directory
:create_yolo_bat_from_directory
echo Yolo Batch (Directory):
echo yolo.py should be in !TARGET_DIR!...
if not exist !TARGET_FULLPATH! ( echo Not Found: Aborting "create_yolo_bat_from_directory" ) else (
    echo Found: Creating "yolo.bat" in !SCRIPT_DIR!
    copy nul !SCRIPT_DIR!\yolo.bat
    echo @echo off>!SCRIPT_DIR!\"yolo.bat"
    echo python.exe !TARGET_DIR!\yolo.py %%*>>!SCRIPT_DIR!\"yolo.bat"
)
goto :EOF

:: Create yolo.bat and input code linking to repository
:create_yolo_bat_from_repository
echo Yolo Batch (Repository):
echo yolo.py should be in %~dp0...
if not exist %~dp0\yolo.py ( echo Not Found: Aborting "create_yolo_bat_from_repository") else (
    echo Found: Creating "yolo.bat" in !SCRIPT_DIR!
    copy nul !SCRIPT_DIR!\yolo.bat
    echo @echo off>!SCRIPT_DIR!\"yolo.bat"
    echo python.exe %~dp0\yolo.py %%*>>!SCRIPT_DIR!\"yolo.bat"
)
goto :EOF

:: Creates the safety off file and puts it in ~ for you
:create_safety_off
echo Yolo Safety Off:
echo Creating ".yolo-safety-off" in %HOMEDRIVE%%HOMEPATH%\
copy nul %HOMEDRIVE%%HOMEPATH%\.yolo-safety-off
goto :EOF

:: Creates the .openai.apikey if it doesn't already exists (otherwise, does nothing)
:create_openai_apikey
echo Yolo OpenAi ApiKey:
echo Creating ".open.apikey" (if not already exists) in %HOMEDRIVE%%HOMEPATH%\
copy nul %~dp0\.openai.apikey
robocopy %~dp0 %HOMEDRIVE%%HOMEPATH%\ .openai.apikey /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np
del %~dp0\.openai.apikey
goto :EOF

:: Creates the .env if it doesn't already exists in chosen install directory (otherwise, does nothing)
:create_env_in_directory
echo Yolo .Env:
echo Creating ".env" (if not already exists) in !TARGET_DIR!
if not exist %~dp0\.env ( copy nul %~dp0\.env  & robocopy %~dp0 !TARGET_DIR! .env /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np & del %~dp0\.env ) else ( robocopy %~dp0 !TARGET_DIR! .env /xc /xn /xo /nfl /ndl /njh /njs /nc /ns /np )
goto :EOF

:: Creates the .env if it doesn't already exists in chosen install directory (otherwise, does nothing)
:create_env_in_repository
echo Yolo .Env:
echo Creating ".env" (if not already exists) in %~dp0
if not exist %~dp0\.env ( copy nul %~dp0\.env ) else ( echo Already Exists )
goto :EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::                                              General                                                               ::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:print_guide
echo ...
echo Finished installing yolo-ai-cmdbot...
echo You can run commands by being in the same directory as your "yolo.bat" file ( It is in !SCRIPT_DIR! ) with the following command:
echo ".\yolo.bat <prompt>"
echo You can also put your "yolo.bat" file into a $PATH directory and run it like so, instead:
echo "yolo <prompt>"
echo You should have "C:\Windows\System32" as a path in the $PATH environment variable but you can write the command "echo $env:PATH" into PowerShell for more options...
goto :EOF