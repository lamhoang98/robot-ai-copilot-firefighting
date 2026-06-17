@echo off
echo.
echo ========================================
echo Robot AI Copilot - Installation
echo ========================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo Install from: https://www.python.org
    pause
    exit /b 1
)
echo [1/5] Python OK
python --version
echo [2/5] Creating venv...
if not exist venv python -m venv venv
echo [3/5] Activating...
call venv\Scripts\activate.bat
echo [4/5] Installing packages...
pip install -q --upgrade pip
pip install -r requirements.txt
echo [5/5] Creating directories...
if not exist output mkdir output
if not exist output\logs mkdir output\logs
if not exist models mkdir models
echo.
echo @echo off > Run_Robot_AI.bat
echo cd /d "%%~dp0" >> Run_Robot_AI.bat
echo call venv\Scripts\activate.bat >> Run_Robot_AI.bat
echo python main.py >> Run_Robot_AI.bat
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next: Double-click Run_Robot_AI.bat
echo.
pause
