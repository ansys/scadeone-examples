@echo off
REM --------------------------------------------------------------------------
REM Batch script to activate the .venv, install test requirements,
REM and run the proxy generation script.
REM
REM Usage: run this from the repository root (double-click or run from cmd).
REM
REM Requisites:
REM   * Python Virtual Environment created in .venv
REM   * A connection to the internet (or a local package repository/cache)
REM     to install dependencies not already installed.
REM --------------------------------------------------------------------------

:: Colors for console output (do not modify)
set GOLD=[33m
set GREEN=[92m
set MAGENTA=[95m
set RED=[91m
set EOL=[0m

:: Resolve script directory
SET SCRIPT_DIR=%~dp0

:: Ensure we use the repo root as current directory
CD /D "%SCRIPT_DIR%\.."

:: Path to venv activation script for cmd
SET ACTIVATE_CMD=.venv\Scripts\activate.bat

:: If the venv activation script exists, activate it
IF EXIST "%ACTIVATE_CMD%" (
    CALL "%ACTIVATE_CMD%"
    ECHO %GREEN%Virtual environment activated.%EOL%
    ECHO.
) ELSE (
    ECHO %RED%Virtual environment activation script not found: %ACTIVATE_CMD%%EOL%
    ECHO.
    ECHO %GOLD%Please create a Python Virtual Environment with: %MAGENTA%python -m venv .venv%EOL%
    ECHO %GOLD%Then run the script again ^(dependencies will be installed automatically^).%EOL%
    ECHO.
    pause
    EXIT /B 1
)

:: By default install test requirements if tests\requirements.txt exists.
IF EXIST "tests\requirements.txt" (
    ECHO %MAGENTA%Installing test dependencies from tests\requirements.txt...%EOL%
    ECHO.
    python -m pip install -r tests\requirements.txt
    ECHO %GREEN%=^> Test dependencies installed successfully!%
) ELSE (
    ECHO %GOLD%No tests\requirements.txt found; skipping dependency install.%EOL%
)
ECHO.

:: Run the generator script with python
ECHO %MAGENTA%Running code generation script...%EOL%
python tests\utils\generate_code.py %*
SET EXIT_CODE=%ERRORLEVEL%
IF %EXIT_CODE% NEQ 0 (
    ECHO %RED%Code generation script failed with exit code %EXIT_CODE%.%EOL%
    ECHO.
    pause
) ELSE (
    ECHO %GREEN%Code generation script completed successfully.%EOL%
    echo.
    timeout /t 10
)

:: Return exit code of python
EXIT /B %EXIT_CODE%
