@echo off
REM ============================================
REM AIOOS Platform - Complete Start Script
REM Starts: Backend + Agent Worker + Frontend
REM ============================================

echo.
echo ================================================
echo 🚀 Starting AIOOS Platform (WITH VOICE AGENT!)
echo ================================================
echo.

echo 📝 This will open 3 windows:
echo    1. Backend API (Port 8000)
echo    2. Agent Worker (Voice Agent)
echo    3. Frontend (Port 5173)
echo.

pause

REM ============================================
REM Window 1: Backend API
REM ============================================
start "AIOOS Backend (Port 8000)" /D "%~dp0v4liveKit\backend" cmd /k "echo ================================================ && echo. && echo 🔧 AIOOS Backend Server && echo ================================================ && echo. && echo Backend running at: http://localhost:8000 && echo API Docs: http://localhost:8000/docs && echo. && echo Close this window to stop the backend && echo ================================================ && echo. && call venv\Scripts\activate.bat && python main.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM ============================================
REM Window 2: Agent Worker (VOICE AGENT!)
REM ============================================
start "AIOOS Agent Worker (Voice)" /D "%~dp0v4liveKit\backend" cmd /k "echo ================================================ && echo. && echo 🎙️  AIOOS Voice Agent Worker && echo ================================================ && echo. && echo This enables voice conversations! && echo Using Azure Speech (German + English) && echo. && echo Close this window to stop the agent && echo ================================================ && echo. && call venv\Scripts\activate.bat && python agent_worker.py dev"

REM Wait a bit for agent worker to start
timeout /t 3 /nobreak >nul

REM ============================================
REM Window 3: Frontend
REM ============================================
start "AIOOS Frontend (Port 5173)" /D "%~dp0v4liveKit-frontend" cmd /k "echo ================================================ && echo. && echo 🎨 AIOOS Frontend && echo ================================================ && echo. && echo Frontend running at: http://localhost:5173 && echo. && echo Close this window to stop the frontend && echo ================================================ && echo. && npm run dev"

echo.
echo ================================================
echo ✅ All services starting...
echo ================================================
echo.
echo 📝 Opening 3 windows:
echo.
echo    1. Backend API: http://localhost:8000
echo    2. Agent Worker: Voice agent running
echo    3. Frontend: http://localhost:5173
echo.
echo ⏳ Wait 10 seconds for everything to start...
echo.
echo 🌐 Frontend will open automatically!
echo.

REM Wait 10 seconds
timeout /t 10 /nobreak >nul

REM Open browser
start http://localhost:5173

echo.
echo ================================================
echo ✅ Platform started successfully!
echo ================================================
echo.
echo 🎤 To test voice agent:
echo    1. Go to: http://localhost:5173
echo    2. Click on "Deutscher Kundenservice"
echo    3. Click "Test Agent"
echo    4. Say: "Hallo, wie geht es dir?"
echo.
echo 🛑 To stop: Run 3-STOP.bat
echo.
pause
