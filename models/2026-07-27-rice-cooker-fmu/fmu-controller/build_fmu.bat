@REM Batch file to build FMU of the Rice Cooker Controller
@echo off

cd /d %~dp0

set SCADE_ONE_PATH=C:\Program Files\ANSYS Inc\v261\Scade One
set MODEL_DIR=RiceCookerController


:: Colors for console output (do not modify)
set GOLD=[33m
set GREEN=[92m
set MAGENTA=[95m
set RED=[91m
set EOL=[0m

:: Raise an error if "code" folder not found
if not exist "%MODEL_DIR%\jobs\codegen_c4483e5\out\code" (
    echo.
    echo %RED%Error: RiceCookerController code generation output folder not found.%EOL%
    echo Please launch first the code generation from Scade One:
    echo 1. Open RiceCookerController/RiceCookerController.sproj in Scade One
    echo 2. Open the "Job Explorer" - Alt + Shift + J
    echo 3. Select the code generation job "CodeGenerationController" from "RiceCookerController"
    echo 4. Click on "Start"
    echo.
    pause
    exit /b 1
)

:: Previous build artifacts might prevent exporting the FMU
call :cleanup

:: FMU export command leveraging pyscadeone
@REM NOTE: In 2027 R1, the FMU exporter became a dedicated module
python -c "import ansys.scadeone.exporters.fmu" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo %GOLD%WARNING: This script was designed for Scade One 2026 R1.%EOL%
    echo %GOLD%In Scade One 2027 R1+, the FMU exporter is now a dedicated module.%EOL%
    set FMU_EXPORTER=fmu_export
) else (
    set FMU_EXPORTER=pyscadeone fmu
)
set FMU_ARGS=-inst "%SCADE_ONE_PATH%" --kind CS --period 0.2 -args user_sources %MODEL_DIR%\resources -args swan_config_begin "#include \"int2char.h\""

set CMD=%FMU_EXPORTER% %MODEL_DIR%\RiceCookerController.sproj CodeGenerationController %FMU_ARGS% -o .
echo %MAGENTA%%CMD%%EOL%
%CMD%
set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% NEQ 0 (
    echo.
    echo %RED%Error: FMU build failed with exit code %EXIT_CODE%.%EOL%
    echo.
    pause
    exit /b %EXIT_CODE%
)

:: Keep it clean, without deleting a folder still in use by system
timeout /t 1 /nobreak >nul
call :cleanup

echo.
echo %GREEN%FMU build completed successfully.%EOL%
echo.
timeout /t 10
goto :eof


:cleanup
REM Cleanup temporary build artifacts (folders binaries and sources)
if exist binaries rmdir /s /q binaries & echo %GREEN%Deleted folder binaries.%EOL%
if exist sources rmdir /s /q sources & echo %GREEN%Deleted folder sources.%EOL%
goto :eof
