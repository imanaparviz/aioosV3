@echo off
REM ============================================
REM AIOOS Platform - Simple Stop Script
REM Nuclear option: Kills ALL python & node
REM Use if 3-STOP.bat doesn't work!
REM ============================================

echo.
echo ================================================
echo 🛑 SIMPLE STOP (Nuclear Option!)
echo ================================================
echo.
echo ⚠️  WARNING: This will kill ALL Python and Node processes!
echo ⚠️  Including any other projects you have running!
echo.
pause

echo.
echo 📍 Killing ALL Python processes...
taskkill /F /IM python.exe >nul 2>&1
if errorlevel 1 (
    echo    ✅ No Python processes found
) else (
    echo    ✅ Killed all Python processes
)

echo.
echo 📍 Killing ALL Node processes...
taskkill /F /IM node.exe >nul 2>&1
if errorlevel 1 (
    echo    ✅ No Node processes found
) else (
    echo    ✅ Killed all Node processes
)

echo.
echo ================================================
echo ✅ Done!
echo ================================================
echo.
echo 💡 To start again: Run 2-START.bat
echo.
pause
