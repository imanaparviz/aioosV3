@echo off
echo ================================================
echo 🎙️  Starting AIOOS Voice Agent Worker
echo ================================================
echo.

cd backend
call venv\Scripts\activate.bat

echo.
echo 🚀 Starting worker...
echo.

python agent_worker.py dev

pause
