@echo off
REM Fix DNS Resolution Issue for Supabase

echo ================================================
echo 🔧 DNS Fix for Supabase Connection
echo ================================================
echo.

echo 📝 This will temporarily use Google DNS (8.8.8.8)
echo    to resolve Supabase hostnames
echo.

REM Flush DNS cache
echo 🔄 Flushing DNS cache...
ipconfig /flushdns

REM Display current DNS
echo.
echo 📍 Current DNS servers:
ipconfig /all | findstr /C:"DNS Servers"

echo.
echo ================================================
echo ✅ DNS cache flushed!
echo ================================================
echo.
echo 📝 Next Steps:
echo.
echo 1. If problem persists, manually change DNS:
echo    - Open: Control Panel ^> Network ^> Adapter Settings
echo    - Right-click your network adapter ^> Properties
echo    - Select: Internet Protocol Version 4 (TCP/IPv4)
echo    - Use these DNS servers:
echo      • Preferred: 8.8.8.8 (Google)
echo      • Alternate: 1.1.1.1 (Cloudflare)
echo.
echo 2. Or use this quick PowerShell command (Run as Admin):
echo    netsh interface ip set dns "Wi-Fi" static 8.8.8.8
echo.
echo 3. Test Supabase connection:
echo    ping tctfeentpoafteuphpls.supabase.co
echo.
pause
