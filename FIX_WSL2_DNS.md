# 🔧 Fix WSL2 DNS Issue (Supabase Connection)

## Problem Peida Shode

**WSL2 nemitone Supabase hostname ro resolve kone!**

```
❌ ping tctfeentpoafteuphpls.supabase.co
   Name or service not known

❌ DNS Server: 10.255.255.254 (WSL2 default)
   In nameserver kar nemikone!
```

## ✅ Hal-e Moshkel (3 Steps)

### Option 1: PowerShell Script (EASIEST!) ⭐

Run this from **Windows PowerShell as Administrator**:

```powershell
# Create wsl.conf in WSL
wsl -d Ubuntu -u root -- bash -c "cat > /etc/wsl.conf << 'EOF'
[network]
generateResolvConf = false
EOF"

# Create resolv.conf with Google DNS
wsl -d Ubuntu -u root -- bash -c "cat > /etc/resolv.conf << 'EOF'
nameserver 8.8.8.8
nameserver 1.1.1.1
EOF"

# Restart WSL
wsl --shutdown
```

Then open a **NEW** WSL terminal and test:
```bash
ping -c 2 tctfeentpoafteuphpls.supabase.co
```

---

### Option 2: Manual Fix (Step by Step)

#### Step 1: Create `/etc/wsl.conf`

Open WSL terminal and run:
```bash
sudo nano /etc/wsl.conf
```

Add this content:
```ini
[network]
generateResolvConf = false
```

Save with `Ctrl+O`, exit with `Ctrl+X`.

#### Step 2: Create `/etc/resolv.conf`

```bash
sudo nano /etc/resolv.conf
```

Add this content:
```
nameserver 8.8.8.8
nameserver 1.1.1.1
```

Save and exit.

#### Step 3: Restart WSL

From **Windows PowerShell**:
```powershell
wsl --shutdown
```

Open a **NEW** WSL terminal.

#### Step 4: Test DNS

```bash
ping -c 2 tctfeentpoafteuphpls.supabase.co
```

Should work now! ✅

---

### Option 3: Batch File (Windows) 🪟

I've created: **`FIX_WSL2_DNS.bat`**

Just **Right-click → Run as Administrator**

---

## ✅ Verification

After applying fix, test these:

### Test 1: DNS Resolution
```bash
ping -c 2 tctfeentpoafteuphpls.supabase.co
```

Expected:
```
PING tctfeentpoafteuphpls.supabase.co (xx.xx.xx.xx) 56(84) bytes of data.
64 bytes from xx.xx.xx.xx: icmp_seq=1 ttl=xx time=xx ms
```

### Test 2: Python Connection
```bash
cd /mnt/c/agents/ba-khodam/aioosBaKhodam/v4liveKit/backend
source venv/bin/activate  # Or: . venv/Scripts/activate
python -c "import socket; print(socket.gethostbyname('tctfeentpoafteuphpls.supabase.co'))"
```

Should print Supabase IP address! ✅

### Test 3: Backend Health Check
```bash
cd /mnt/c/agents/ba-khodam/aioosBaKhodam/v4liveKit/backend
venv/Scripts/python.exe main.py
```

Open another terminal:
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "services": {
    "supabase": "connected"
  }
}
```

---

## 🚀 Run Backend After Fix

### From WSL2:
```bash
cd /mnt/c/agents/ba-khodam/aioosBaKhodam/v4liveKit/backend
venv/Scripts/python.exe main.py
```

### From Windows CMD:
```batch
cd C:\agents\ba-khodam\aioosBaKhodam
2-START.bat
```

---

## 📝 Why This Happened?

WSL2 uses a virtual network adapter with its own DNS server (`10.255.255.254`).

Sometimes this DNS server can't resolve external hostnames properly, especially:
- Supabase domains
- Custom subdomains
- Some cloud services

**Solution**: Use public DNS servers (Google 8.8.8.8 or Cloudflare 1.1.1.1) instead!

---

## 🔄 If Problem Persists

### Check Windows Firewall:
```powershell
# Windows PowerShell (as Admin)
Get-NetFirewallRule -DisplayName "*WSL*"
```

### Check Windows DNS:
```powershell
# Windows PowerShell
Get-DnsClientServerAddress
```

Should include `8.8.8.8` or similar.

### Flush All DNS Caches:
```powershell
# Windows PowerShell (as Admin)
ipconfig /flushdns
Clear-DnsClientCache

# Then in WSL:
sudo systemd-resolve --flush-caches  # If systemd available
```

---

## ✅ Success Checklist

- [ ] `/etc/wsl.conf` created with `generateResolvConf = false`
- [ ] `/etc/resolv.conf` has `nameserver 8.8.8.8`
- [ ] WSL restarted with `wsl --shutdown`
- [ ] `ping tctfeentpoafteuphpls.supabase.co` works ✅
- [ ] Backend starts without DNS errors ✅
- [ ] Can create agents in frontend ✅

---

**Fixed:** 2024-11-13
**Issue:** WSL2 DNS can't resolve Supabase hostname
**Solution:** Use Google DNS (8.8.8.8) instead of WSL2 default
**Status:** ✅ READY TO FIX
