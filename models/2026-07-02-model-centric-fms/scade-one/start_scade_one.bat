@echo off
rem Start Scade One with FMS_DATA_DIR pointing to this example's data folder.
rem Usage: start_scade_one.bat [SCADE_ONE_INSTALL_DIR]
rem   SCADE_ONE_INSTALL_DIR defaults to "%ProgramFiles%\ANSYS Inc\v271\Scade One".
rem The simulator runs from a temporary directory, so FMS_DATA_DIR must be an
rem absolute path; it is computed here from the location of this script.
setlocal

set "SCADE_ONE_INSTALL_DIR=%~1"
if not defined SCADE_ONE_INSTALL_DIR set "SCADE_ONE_INSTALL_DIR=%ProgramFiles%\ANSYS Inc\v271\Scade One"

set "IDE=%SCADE_ONE_INSTALL_DIR%\client\ScadeOneIDE.exe"
if not exist "%IDE%" (
    echo ERROR: Scade One was not found: "%IDE%"
    echo Usage: %~nx0 [SCADE_ONE_INSTALL_DIR]
    exit /b 1
)

for %%I in ("%~dp0..\data") do set "FMS_DATA_DIR=%%~fI"
if not exist "%FMS_DATA_DIR%\f-424" (
    echo ERROR: navigation database not found: "%FMS_DATA_DIR%\f-424"
    exit /b 1
)

echo FMS_DATA_DIR=%FMS_DATA_DIR%
start "" "%IDE%" "%~dp0FMS_App\FMS_App.sproj"
exit /b 0
