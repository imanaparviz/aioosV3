@echo off
REM ========================================
REM Fix WSL2 DNS Issue for Supabase
REM Run as Administrator!
REM ========================================

echo.
echo ================================================
echo 🔧 WSL2 DNS Fix for Supabase Connection
echo ================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ ERROR: This script must be run as Administrator!
    echo.
    echo Right-click this file and select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Running as Administrator
echo.

echo 📝 Step 1: Creating /etc/wsl.conf in WSL...
wsl -d Ubuntu -u root -- bash -c "cat > /etc/wsl.conf << 'EOF'^

[network]^

generateResolvConf = false^

EOF"

if %errorLevel% equ 0 (
    echo ✅ /etc/wsl.conf created
) else (
    echo ❌ Failed to create wsl.conf
    echo    Try running: wsl -l -v
    echo    Make sure Ubuntu is installed
    pause
    exit /b 1
)

echo.
echo 📝 Step 2: Creating /etc/resolv.conf with Google DNS...
wsl -d Ubuntu -u root -- bash -c "cat > /etc/resolv.conf << 'EOF'^

nameserver 8.8.8.8^

nameserver 1.1.1.1^

EOF"

if %errorLevel% equ 0 (
    echo ✅ /etc/resolv.conf created with Google DNS
) else (
    echo ❌ Failed to create resolv.conf
    pause
    exit /b 1
)

echo.
echo 📝 Step 3: Restarting WSL to apply changes...
wsl --shutdown

if %errorLevel% equ 0 (
    echo ✅ WSL restarted successfully
) else (
    echo ⚠️  WSL shutdown returned error, but might still work
)

echo.
echo ================================================
echo ✅ DNS Fix Applied!
echo ================================================
echo.

echo 📝 Next Steps:
echo.
echo 1. Open a NEW WSL terminal
echo.
echo 2. Test DNS resolution:
echo    ping -c 2 tctfeentpoafteuphpls.supabase.co
echo.
echo 3. Start backend:
echo    cd /mnt/c/agents/ba-khodam/aioosBaKhodam
echo    2-START.bat
echo.
echo 4. Test agent creation in frontend!
echo.

echo ⚠️  If problem persists:
echo    - Check Windows Firewall settings
echo    - Run: FIX_DNS_ISSUE.bat (flushes Windows DNS cache)
echo    - Check: FIX_WSL2_DNS.md for manual steps
echo.

pause
