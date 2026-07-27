@REM Batch file to build FMU of the Rice Cooker Controller
@echo off

cd /d %~dp0

set SCADE_ONE_PATH=C:\Program Files\ANSYS Inc\v261\Scade One
set MODEL_DIR=RiceCookerController

:: Install requirements (pyscadeone) => NOTE: consider using a Virtual Environment
pip install ansys-scadeone-core

:: Previous build artifacts might prevent exporting the FMU
call :cleanup

:: FMU export command leveraging pyscadeone
pyscadeone fmu %MODEL_DIR%\RiceCookerController.sproj CodeGenerationController --install "%SCADE_ONE_PATH%" --kind CS --period 0.2 -args user_sources %MODEL_DIR%\resources -args swan_config_begin "#include \"int2char.h\"" -o .

set EXIT_CODE=%ERRORLEVEL%
if %EXIT_CODE% NEQ 0 (
    echo.
    echo Error: FMU build failed with exit code %EXIT_CODE%.
    echo.
    pause
    exit /b %EXIT_CODE%
)

:: Keep it clean, without deleting a folder still in use by system
timeout /t 1 /nobreak >nul
call :cleanup

echo.
echo FMU build completed successfully.
echo.
timeout /t 10
goto :eof


:cleanup
REM Cleanup temporary build artifacts (folders binaries and sources)
if exist binaries rmdir /s /q binaries & echo Deleted folder binaries
if exist sources rmdir /s /q sources & echo Deleted folder sources
goto :eof
