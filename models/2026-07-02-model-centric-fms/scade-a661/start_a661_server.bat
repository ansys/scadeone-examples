@echo off
rem Start the ARINC 661 server (SCADE A661) on the FMS User Application DF.
rem Usage: start_a661_server.bat [ANSYS_INSTALL_DIR]
rem   ANSYS_INSTALL_DIR defaults to "%ProgramFiles%\ANSYS Inc\v261".
rem Run build_df.bat first to generate DF\UA_1.bin.
setlocal

set "ANSYS_INSTALL_DIR=%~1"
if not defined ANSYS_INSTALL_DIR set "ANSYS_INSTALL_DIR=%ProgramFiles%\ANSYS Inc\v261"

set "SERVER=%ANSYS_INSTALL_DIR%\SCADE\SCADE A661\bin\A661Server.exe"
set "DF=%~dp0DF\UA_1.bin"

if not exist "%SERVER%" (
    echo ERROR: A661Server.exe was not found: "%SERVER%"
    echo Usage: %~nx0 [ANSYS_INSTALL_DIR]
    exit /b 1
)

if not exist "%DF%" (
    echo ERROR: Definition File was not found: "%DF%"
    echo Run build_df.bat first.
    exit /b 1
)

pushd "%~dp0DF"
"%SERVER%" -udp "%DF%"
set "SERVER_EXIT_CODE=%ERRORLEVEL%"
popd
exit /b %SERVER_EXIT_CODE%
