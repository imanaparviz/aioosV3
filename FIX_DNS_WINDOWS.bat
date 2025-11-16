@echo off
REM ============================================
REM Fix Windows DNS for Supabase Connection
REM Run as Administrator!
REM ============================================

echo.
echo ================================================
echo 🔧 Windows DNS Fix for Supabase
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

echo 📝 Step 1: Finding active network adapter...
echo.

REM Get active network adapter name
for /f "tokens=1" %%i in ('powershell -Command "Get-NetAdapter | Where-Object {$_.Status -eq 'Up' -and $_.InterfaceDescription -like '*Wi-Fi*'} | Select-Object -ExpandProperty Name"') do set ADAPTER_NAME=%%i

if "%ADAPTER_NAME%"=="" (
    echo ⚠️  Wi-Fi adapter not found, trying WLAN...
    set ADAPTER_NAME=WLAN
)

echo ✅ Found adapter: %ADAPTER_NAME%
echo.

echo 📝 Step 2: Setting DNS to Google (8.8.8.8, 1.1.1.1)...
echo.

powershell -Command "Set-DnsClientServerAddress -InterfaceAlias '%ADAPTER_NAME%' -ServerAddresses ('8.8.8.8','1.1.1.1')"

if %errorLevel% equ 0 (
    echo ✅ DNS updated successfully
) else (
    echo ❌ Failed to update DNS automatically
    echo.
    echo 📝 Manual fix required:
    echo    1. Open: Control Panel ^> Network Connections
    echo    2. Right-click: %ADAPTER_NAME%
    echo    3. Properties ^> IPv4 ^> Properties
    echo    4. Set DNS: 8.8.8.8, 1.1.1.1
    echo.
    pause
    exit /b 1
)

echo.
echo 📝 Step 3: Flushing DNS cache...
echo.

ipconfig /flushdns >nul 2>&1
powershell -Command "Clear-DnsClientCache" >nul 2>&1

echo ✅ DNS cache cleared
echo.

echo 📝 Step 4: Testing connection to Supabase...
echo.

ping -n 2 tctfeentpoafteuphpls.supabase.co

if %errorLevel% equ 0 (
    echo.
    echo ================================================
    echo ✅ SUCCESS! DNS is working!
    echo ================================================
    echo.
    echo 🚀 Next step: Start backend
    echo    cd C:\agents\ba-khodam\aioosBaKhodam
    echo    2-START.bat
    echo.
) else (
    echo.
    echo ================================================
    echo ❌ Still cannot reach Supabase
    echo ================================================
    echo.
    echo 🔧 Troubleshooting options:
    echo.
    echo 1. Check if firewall is blocking connection
    echo 2. Try manual DNS configuration (see above)
    echo 3. Restart computer and try again
    echo 4. Check if VPN is interfering
    echo.
    echo 📝 To test manually after restart:
    echo    ping tctfeentpoafteuphpls.supabase.co
    echo.
)

pause
