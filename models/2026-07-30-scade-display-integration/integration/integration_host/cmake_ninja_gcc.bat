@REM # This sample script demonstrates the CMake commands used to configure and build with Ninja and GCC
@echo OFF
@setlocal
@set SCADE_DISPLAY_HOME=%SCADE_HOME%\SCADE Display
@set PATH=%SCADE_HOME%\contrib\cmake\bin;%SCADE_HOME%\contrib\ninja;%SCADE_HOME%\contrib\Msys64\mingw64\bin;%PATH%
cd /d "%~dp0"

echo #############################################
echo ## Build Example
echo #############################################

if exist "%~dp0ninja_gcc" rmdir /s /q "%~dp0ninja_gcc"

@REM Configure a solution for MinGW in a 'ninja_gcc' directory
cmake -B "%~dp0ninja_gcc" -G "Ninja" -S "%~dp0." 

@REM Build the Release configuration
cmake --build "%~dp0ninja_gcc" --config Release --clean-first 

echo #############################################
echo ## Build Complete:
echo ##   ninja_gcc/flightControlSystem.exe
echo #############################################
@endlocal

