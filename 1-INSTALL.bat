@echo off
REM ============================================
REM AIOOS Platform - Installation Script
REM Install all backend and frontend dependencies
REM ============================================

echo ================================================
echo 🚀 AIOOS Platform - Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.9 or higher
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js 16 or higher
    echo Download: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found:
node --version
echo.

REM ==================== BACKEND INSTALLATION ====================
echo.
echo ================================================
echo 📦 Installing Backend Dependencies...
echo ================================================
echo.

cd v4liveKit\backend

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo 📦 Installing Python packages...
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install backend requirements
pip install -r requirements.txt

REM Install LiveKit agents from parent directory
echo 📦 Installing LiveKit agents...
cd ..
pip install -e ./livekit-agents
pip install -e ./livekit-plugins/livekit-plugins-azure
pip install -e ./livekit-plugins/livekit-plugins-openai
pip install -e ./livekit-plugins/livekit-plugins-deepgram
pip install -e ./livekit-plugins/livekit-plugins-silero

cd backend

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found
    echo 📝 Copying .env.example to .env
    copy .env.example .env
    echo.
    echo ❗ IMPORTANT: Edit backend\.env and add your API keys!
    echo.
) else (
    echo ✅ .env file exists
)

deactivate
cd ..\..

REM ==================== FRONTEND INSTALLATION ====================
echo.
echo ================================================
echo 📦 Installing Frontend Dependencies...
echo ================================================
echo.

cd v4liveKit-frontend

REM Install npm packages
echo 📦 Installing npm packages...
call npm install

if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed

REM Check frontend .env
if not exist ".env" (
    echo.
    echo ⚠️  Frontend .env not found
    echo Creating default .env...
    (
        echo # Backend API URL
        echo VITE_API_URL=http://localhost:8000
        echo.
        echo # Supabase Configuration ^(Optional^)
        echo VITE_SUPABASE_URL=
        echo VITE_SUPABASE_ANON_KEY=
    ) > .env
    echo ✅ Frontend .env created
) else (
    echo ✅ Frontend .env exists
)

cd ..

REM ==================== DONE ====================
echo.
echo ================================================
echo ✅ Installation Complete!
echo ================================================
echo.
echo 📝 Next Steps:
echo.
echo   1. Edit backend\.env and add your API keys:
echo      - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
echo      - OPENAI_API_KEY
echo      - AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
echo      - DEEPGRAM_API_KEY
echo.
echo   2. Run: 2-START.bat to start the platform
echo.
echo   3. Backend will run at: http://localhost:8000
echo      Frontend will run at: http://localhost:5173
echo.
echo ================================================
echo.
pause
