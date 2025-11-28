@echo off
REM ============================================
REM AIOOS Platform - Start Script
REM Runs Backend, Agent Worker, and Frontend
REM ============================================

REM Set the base directory to THIS script's location
set "BASEDIR=%~dp0"
cd /d "%BASEDIR%"

echo ================================================
echo 🚀 Starting AIOOS Voice AI Platform
echo 📁 From: %BASEDIR%
echo ================================================
echo.

REM Check if backend venv exists
if not exist "%BASEDIR%v4liveKit\backend\venv" (
    echo ❌ Backend not installed yet!
    echo 📝 Please run: 1-INSTALL.bat first
    echo.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "%BASEDIR%v4liveKit-frontend\node_modules" (
    echo ❌ Frontend not installed yet!
    echo 📝 Please run: 1-INSTALL.bat first
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies found. Starting services...
echo.

REM 1. Start Backend
echo 🔧 Starting Backend Server (Port 8000)...
start "AIOOS Backend" /D "%BASEDIR%v4liveKit\backend" cmd /k "call venv\Scripts\activate.bat && python main.py"

REM Wait for backend to initialize
timeout /t 3 /nobreak >nul

REM 2. Start Agent Worker
echo 🎙️  Starting Voice Agent Worker...
start "AIOOS Agent Worker" /D "%BASEDIR%v4liveKit\backend" cmd /k "call venv\Scripts\activate.bat && python agent_worker.py dev"

REM Wait for worker to initialize
timeout /t 2 /nobreak >nul

REM 3. Start Frontend
echo 🎨 Starting Frontend Server (Port 5173)...
start "AIOOS Frontend" /D "%BASEDIR%v4liveKit-frontend" cmd /k "npm run dev"

REM Wait for frontend to initialize
timeout /t 4 /nobreak >nul

echo.
echo ================================================
echo ✅ All Systems Operational!
echo ================================================
echo.
echo 🌐 Backend:  http://localhost:8000
echo 🎙️  Worker:   Listening for jobs...
echo 🎨 Frontend: http://localhost:5173
echo.
echo 🎉 Opening browser...
start http://localhost:5173

echo.
echo 💡 Press any key to close this launcher (servers will keep running)...
pause >nul
