@REM This sample script demonstrates the CMake commands used to configure and build with Visual Studio 2022
@echo OFF
@setlocal
@set SCADE_DISPLAY_HOME=%SCADE_HOME%\SCADE Display
@set PATH=%SCADE_HOME%\contrib\cmake\bin;%SCADE_HOME%\contrib\ninja;%SCADE_HOME%\contrib\Msys64\mingw64\bin;%PATH%
cd /d "%~dp0"

echo #############################################
echo ## Build Example
echo #############################################

if exist "%~dp0msvc2022" rmdir /s /q "%~dp0msvc2022"

@REM Configure a solution for Visual Studio 2022 in 'msvc2022' directory
cmake -B "%~dp0msvc2022" -G "Visual Studio 17 2022" -A Win32 -S "%~dp0."

@REM Build the Release configuration
cmake --build "%~dp0msvc2022" --config Release --clean-first 

echo #############################################
echo ## Build Complete:
echo ##   msvc2022/Release/flightControlSystem.exe
echo #############################################
@endlocal

