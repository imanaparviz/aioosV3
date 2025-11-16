@echo off
REM ============================================
REM AIOOS Platform - Start Script
REM Runs both Backend and Frontend servers
REM ============================================

echo ================================================
echo 🚀 Starting AIOOS Voice AI Platform
echo ================================================
echo.

REM Check if backend venv exists
if not exist "v4liveKit\backend\venv" (
    echo ❌ Backend not installed yet!
    echo 📝 Please run: 1-INSTALL.bat first
    echo.
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "v4liveKit-frontend\node_modules" (
    echo ❌ Frontend not installed yet!
    echo 📝 Please run: 1-INSTALL.bat first
    echo.
    pause
    exit /b 1
)

echo ✅ Dependencies found
echo.
echo 📝 Starting servers in separate windows...
echo.
echo   Backend:  http://localhost:8000
echo   Agent Worker: Voice AI 🎤
echo   Frontend: http://localhost:5173
echo.
echo 💡 To stop servers: Run 3-STOP.bat or close the windows
echo.

REM Start Backend in new window
echo 🔧 Starting Backend Server...
start "AIOOS Backend (Port 8000)" /D "%~dp0v4liveKit\backend" cmd /k "call venv\Scripts\activate.bat && echo ================================================ && echo 🔧 AIOOS Backend Server && echo ================================================ && echo. && echo Backend running at: http://localhost:8000 && echo API Docs: http://localhost:8000/docs && echo. && echo Close this window to stop the backend && echo ================================================ && echo. && python main.py"

REM Wait 3 seconds for backend to start
echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start Agent Worker in new window (VOICE AGENT!)
echo 🎙️  Starting Agent Worker (Voice AI)...
start "AIOOS Agent Worker (Voice)" /D "%~dp0v4liveKit\backend" cmd /k "call venv\Scripts\activate.bat && echo ================================================ && echo 🎙️  AIOOS Voice Agent Worker && echo ================================================ && echo. && echo This enables voice conversations! && echo Using Azure Speech (German + English) && echo. && echo Close this window to stop the agent && echo ================================================ && echo. && python agent_worker.py dev"

REM Wait 3 seconds for agent worker to start
echo ⏳ Waiting for agent worker to start...
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo 🎨 Starting Frontend Server...
start "AIOOS Frontend (Port 5173)" /D "%~dp0v4liveKit-frontend" cmd /k "echo ================================================ && echo 🎨 AIOOS Frontend Server && echo ================================================ && echo. && echo Frontend running at: http://localhost:5173 && echo. && echo Close this window to stop the frontend && echo ================================================ && echo. && npm run dev"

REM Wait a bit for frontend to start
timeout /t 2 /nobreak >nul

echo.
echo ================================================
echo ✅ Servers Started!
echo ================================================
echo.
echo 🌐 Backend:  http://localhost:8000
echo 🎙️  Agent Worker: Voice AI Running
echo 🌐 Frontend: http://localhost:5173
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 💡 Tips:
echo   - Backend window will show API requests
echo   - Agent Worker window shows voice AI logs
echo   - Frontend window will show build logs
echo   - Close windows or run 3-STOP.bat to stop
echo.
echo 🎤 To test voice agent:
echo   1. Click on "Deutscher Kundenservice" agent
echo   2. Click "Test Agent"
echo   3. Say: "Hallo, wie geht es dir?"
echo.
echo 🎉 Opening frontend in browser...
echo.

REM Wait 5 seconds then open browser
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ✅ Platform is running! Enjoy!
echo.
pause
