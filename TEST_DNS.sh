#!/bin/bash
# Test DNS Resolution After Fix

echo "================================================"
echo "🧪 Testing DNS Resolution"
echo "================================================"
echo ""

echo "📝 Test 1: Check /etc/resolv.conf"
echo "-------------------------------------------"
cat /etc/resolv.conf
echo ""

echo "📝 Test 2: Ping Supabase"
echo "-------------------------------------------"
if ping -c 2 tctfeentpoafteuphpls.supabase.co &>/dev/null; then
    echo "✅ SUCCESS! Can reach Supabase!"
    ping -c 2 tctfeentpoafteuphpls.supabase.co
else
    echo "❌ FAILED! Still can't reach Supabase"
    echo "   Try running FIX_WSL2_DNS.bat again as Administrator"
fi
echo ""

echo "📝 Test 3: Python DNS Lookup"
echo "-------------------------------------------"
if python3 -c "import socket; ip = socket.gethostbyname('tctfeentpoafteuphpls.supabase.co'); print(f'✅ Resolved to: {ip}')" 2>/dev/null; then
    :
else
    echo "❌ Python DNS lookup failed"
    echo "   Run: sudo apt install python3 python3-pip"
fi
echo ""

echo "================================================"
echo "🎯 Next Step: Start Backend"
echo "================================================"
echo ""
echo "If all tests passed, run:"
echo ""
echo "  cd /mnt/c/agents/ba-khodam/aioosBaKhodam"
echo "  2-START.bat"
echo ""
echo "Or manually:"
echo ""
echo "  cd /mnt/c/agents/ba-khodam/aioosBaKhodam/v4liveKit/backend"
echo "  venv/Scripts/python.exe main.py"
echo ""
