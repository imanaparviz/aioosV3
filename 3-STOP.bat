@echo off
REM ============================================
REM AIOOS Platform - Stop Script (IMPROVED!)
REM Stops Backend, Agent Worker, and Frontend
REM ============================================

echo.
echo ================================================
echo 🛑 Stopping AIOOS Platform (All 3 Services)
echo ================================================
echo.

echo 🔍 Searching for running servers...
echo.

REM First, try to close windows gracefully
echo 📍 Attempting graceful shutdown...
taskkill /FI "WINDOWTITLE eq AIOOS Backend*" >nul 2>&1
taskkill /FI "WINDOWTITLE eq AIOOS Agent Worker*" >nul 2>&1
taskkill /FI "WINDOWTITLE eq AIOOS Frontend*" >nul 2>&1
timeout /t 2 /nobreak >nul
echo.

REM ============================================
REM Method 1: Kill by Port (More Reliable!)
REM ============================================

REM Kill Backend (Port 8000) - with /T to kill child processes
echo 📍 Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    echo    ✅ Found PID on port 8000: %%a
    taskkill /F /T /PID %%a >nul 2>&1
)

REM Also kill ALL python.exe running uvicorn (in case multiple instances)
echo 📍 Stopping all Python backend instances...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /C:"uvicorn" >nul
    if not errorlevel 1 (
        echo    ✅ Killing uvicorn python: %%a
        taskkill /F /T /PID %%a >nul 2>&1
    )
)

REM Also pythonw.exe (background Python processes)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq pythonw.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /C:"uvicorn" >nul
    if not errorlevel 1 (
        echo    ✅ Killing uvicorn pythonw: %%a
        taskkill /F /T /PID %%a >nul 2>&1
    )
)

REM Kill Frontend (Port 5173) - with /T to kill child processes
echo.
echo 📍 Stopping Frontend (Port 5173)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173 " ^| findstr "LISTENING"') do (
    echo    ✅ Found PID: %%a
    taskkill /F /T /PID %%a >nul 2>&1
    if errorlevel 1 (
        echo    ⚠️  Could not kill %%a
    ) else (
        echo    ✅ Killed %%a and children
    )
)

REM ============================================
REM Method 2: Kill by Command Window Title
REM ============================================

echo.
echo 📍 Force stopping windows by title...

REM Force kill windows opened by 2-START.bat (with /T for child processes)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq cmd.exe" /FO LIST ^| findstr "PID:"') do (
    for /f "tokens=*" %%t in ('tasklist /V /FI "PID eq %%a" /FO LIST ^| findstr "WINDOWTITLE:"') do (
        echo %%t | findstr /C:"AIOOS Backend" >nul && (
            echo    ✅ Killing Backend window (PID: %%a)
            taskkill /F /T /PID %%a >nul 2>&1
        )
        echo %%t | findstr /C:"AIOOS Agent Worker" >nul && (
            echo    ✅ Killing Agent Worker window (PID: %%a)
            taskkill /F /T /PID %%a >nul 2>&1
        )
        echo %%t | findstr /C:"AIOOS Frontend" >nul && (
            echo    ✅ Killing Frontend window (PID: %%a)
            taskkill /F /T /PID %%a >nul 2>&1
        )
    )
)

REM ============================================
REM Method 3: Cleanup Orphaned Processes (CAREFUL!)
REM ============================================

echo.
echo 📍 Checking for orphaned processes...

REM Kill python.exe running main.py (Backend)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine /format:list 2>nul | findstr /C:"v4liveKit\backend\main.py" >nul
    if not errorlevel 1 (
        echo    ✅ Killing backend (main.py): %%a
        taskkill /F /PID %%a >nul 2>&1
    )
)

REM Kill python.exe running agent_worker.py (Agent Worker)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine /format:list 2>nul | findstr /C:"v4liveKit\backend\agent_worker.py" >nul
    if not errorlevel 1 (
        echo    ✅ Killing agent worker (agent_worker.py): %%a
        taskkill /F /PID %%a >nul 2>&1
    )
)

REM Kill node.exe running vite (Frontend)
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq node.exe" /FO LIST ^| findstr "PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine /format:list 2>nul | findstr /C:"v4liveKit-frontend" >nul
    if not errorlevel 1 (
        echo    ✅ Killing frontend (vite): %%a
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo.
echo ================================================
echo ✅ All 3 services stopped!
echo ================================================
echo.
echo Stopped:
echo   ✅ Backend (main.py)
echo   ✅ Agent Worker (agent_worker.py)
echo   ✅ Frontend (vite)
echo.
echo 💡 To start again: Run 2-START.bat
echo.
pause
