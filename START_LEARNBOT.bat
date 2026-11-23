@echo off
title LearnBot Launcher
cd /d "%~dp0"
echo ==========================================
echo              LEARNBOT
echo ==========================================
where py >nul 2>nul
if %errorlevel%==0 (
    set PY=py
) else (
    set PY=python
)
if not exist ".venv\Scripts\python.exe" (
    echo Creating LearnBot environment...
    %PY% -m venv .venv
    if errorlevel 1 goto error
)
echo Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Starting LearnBot in your browser...
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto error
pause
exit /b 0
:error
echo.
echo Something went wrong. Check that Python 3.10 or newer is installed and available.
echo Read README_FIRST.txt for troubleshooting.
pause
