@echo off
rem Generate the ARINC 661 Definition File (DF) of the FMS User Application.
rem Usage: build_df.bat [ANSYS_INSTALL_DIR]
rem   ANSYS_INSTALL_DIR defaults to "%ProgramFiles%\ANSYS Inc\v261".
rem Output: DF\UA_1.bin (and UA_1.df.xml, a readable dump of the DF).
setlocal

set "ANSYS_INSTALL_DIR=%~1"
if not defined ANSYS_INSTALL_DIR set "ANSYS_INSTALL_DIR=%ProgramFiles%\ANSYS Inc\v261"

set "DFGEN=%ANSYS_INSTALL_DIR%\SCADE\SCADE A661\DFGEN681\bin\dfgen.exe"
set "A661_XML=%ANSYS_INSTALL_DIR%\SCADE\SCADE Display\config\a661_description\a661.xml"
set "HERE=%~dp0"

if not exist "%DFGEN%" (
    echo ERROR: dfgen.exe was not found: "%DFGEN%"
    echo Usage: %~nx0 [ANSYS_INSTALL_DIR]
    exit /b 1
)

if not exist "%HERE%DF" mkdir "%HERE%DF"

"%DFGEN%" -n "%A661_XML%" -outdir "%HERE%DF" -o UA_1 -no_timestamp "%HERE%FMS_UA.sgfx"
exit /b %ERRORLEVEL%
