# 🚀 AIOOS Voice AI Platform - Windows Quick Guide

Super easy setup bara Windows! Faqat 3 ghadam!

## 📂 Chi Dari:

```
aioosBaKhodam/
├── 1-INSTALL.bat          ⭐ Ghadam 1: Nasb e hamechiz
├── 2-START.bat            ⭐ Ghadam 2: Run kardane platform
├── 3-STOP.bat             ⭐ Ghadam 3: Khamosh kardane servers
│
├── QUICK_START.md         📚 Quick guide (Finglish)
├── GERMAN_VOICES.md       🇩🇪 German language guide
├── WHY_AZURE_NOT_ELEVENLABS.md  💰 Cost analysis
├── PROJECT_SETUP.md       📖 Detailed setup
│
├── v4liveKit/
│   └── backend/           🔧 Backend API
│       ├── main.py
│       ├── agent_worker.py
│       └── .env          ⚙️  API keys inja!
│
└── v4liveKit-frontend/    🎨 Frontend UI
    └── .env              ⚙️  Frontend config
```

## ⚡ Super Quick Start (3 Ghadam)

### Ghadam 1: Install All Dependencies

**Double-click:**
```
1-INSTALL.bat
```

In script:
- ✅ Check mikone Python dary ya na
- ✅ Check mikone Node.js dary ya na
- ✅ Install mikone backend dependencies
- ✅ Install mikone frontend dependencies
- ✅ Create mikone .env files

**Time: ~5-10 daghighe** (vasabaste be internet speed)

### Ghadam 2: Configure API Keys

**Edit backend config:**
```
notepad v4liveKit\backend\.env
```

**Add your API keys:**
```bash
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=northeurope
DEEPGRAM_API_KEY=your_key
```

**Koja API keys begiram?**
- LiveKit: https://cloud.livekit.io (FREE!)
- OpenAI: https://platform.openai.com
- Azure: https://portal.azure.com
- Deepgram: https://deepgram.com (FREE tier!)

**Time: ~5-10 daghighe**

### Ghadam 3: Start Platform

**Double-click:**
```
2-START.bat
```

In script:
- ✅ Open mikone 2 ta window (Backend + Frontend)
- ✅ Backend miad bala on port 8000
- ✅ Frontend miad bala on port 5173
- ✅ Browser automatically baz mishe!

**Access:**
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 🛑 How to Stop?

**Double-click:**
```
3-STOP.bat
```

Automatically tamame servers ro khamosh mikone!

## 🎤 Language Support

### English (Default)
```bash
# In backend/.env
TTS_VOICE=en-US-JennyNeural
STT_LANGUAGE=en-US
```

### 🇩🇪 German (Deutsch)
```bash
# In backend/.env
TTS_VOICE=de-DE-KatjaNeural
STT_LANGUAGE=de-DE
AGENT_GREETING=Hallo! Wie kann ich dir helfen?
```

**Full German guide:** `GERMAN_VOICES.md`

### 🇮🇷 Farsi (Persian)
```bash
# In backend/.env
TTS_VOICE=fa-IR-DilaraNeural
STT_LANGUAGE=fa-IR
AGENT_GREETING=سلام! چطور می‌تونم کمکت کنم؟
```

### Multi-language Support

Platform supports **140+ languages** including:
- 🇬🇧 English
- 🇩🇪 German (Standard, Austrian, Swiss)
- 🇮🇷 Farsi
- 🇸🇦 Arabic
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇮🇹 Italian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇨🇳 Chinese
- And many more!

## 💰 Why Azure Not ElevenLabs?

| Feature | Azure | ElevenLabs |
|---------|-------|------------|
| **Cost** | **$4/1M chars** ⭐ | $22/1M chars ❌ |
| **Quality** | **9.5/10** ⭐ | 9.4/10 |
| **Voices** | **400+** ⭐ | ~100 |
| **Languages** | **140+** ⭐ | ~30 |
| **SLA** | **99.9%** ⭐ | 99.5% |

**Savings: 5.5x cheaper!** 💰

Full analysis: `WHY_AZURE_NOT_ELEVENLABS.md`

## 🎯 Best Voices

### English
- `en-US-JennyNeural` - Female, warm, friendly ⭐
- `en-US-GuyNeural` - Male, professional
- `en-US-AriaNeural` - Female, conversational

### German
- `de-DE-KatjaNeural` - Female, warm ⭐
- `de-DE-ConradNeural` - Male, professional
- `de-AT-IngridNeural` - Austrian Female
- `de-CH-LeniNeural` - Swiss Female

### Farsi
- `fa-IR-DilaraNeural` - Female ⭐
- `fa-IR-FaridNeural` - Male

Full list: https://speech.microsoft.com/portal/voicegallery

## 🔧 Troubleshooting

### "Python not found"
- Download: https://python.org/downloads/
- Install Python 3.9 or higher
- Check "Add to PATH" during installation
- Run `1-INSTALL.bat` again

### "Node.js not found"
- Download: https://nodejs.org/
- Install Node.js 16 or higher
- Run `1-INSTALL.bat` again

### "Port 8000 already in use"
- Run `3-STOP.bat` first
- Or manually: `netstat -ano | findstr :8000`
- Kill process: `taskkill /F /PID <PID>`

### "Backend not starting"
- Check `backend\.env` has correct API keys
- Check LIVEKIT_URL starts with `wss://`
- Check internet connection
- Check backend logs in window

### "Frontend not connecting"
- Check backend is running (http://localhost:8000/api/health)
- Check `frontend\.env` has `VITE_API_URL=http://localhost:8000`
- Clear browser cache (Ctrl+Shift+Delete)

### "Voice not working"
- Check AZURE_SPEECH_KEY and AZURE_SPEECH_REGION
- Check browser microphone permission
- Check backend logs
- Try different voice

## 📝 Files Overview

### Batch Files (Windows)

| File | Purpose | When to Use |
|------|---------|-------------|
| `1-INSTALL.bat` | Install all dependencies | First time only |
| `2-START.bat` | Start both servers | Every time you want to run |
| `3-STOP.bat` | Stop all servers | When done working |

### Documentation

| File | Content | Audience |
|------|---------|----------|
| `README_WINDOWS.md` | This file! Windows guide | Windows users |
| `QUICK_START.md` | 3-step guide (Finglish) | Beginners |
| `GERMAN_VOICES.md` | German setup | German speakers |
| `PROJECT_SETUP.md` | Complete technical guide | Developers |
| `WHY_AZURE_NOT_ELEVENLABS.md` | Cost analysis | Decision makers |

### Configuration

| File | Purpose | Edit? |
|------|---------|-------|
| `backend\.env` | Backend API keys | ✅ YES! |
| `frontend\.env` | Frontend config | ⚠️  Maybe |
| `backend\.env.example` | Template | ❌ No |

## ✅ Success Checklist

After running `2-START.bat`, check:

- [ ] Backend window shows "Application startup complete"
- [ ] Frontend window shows "ready in XXXms"
- [ ] Browser opens to http://localhost:5173
- [ ] Can login/signup
- [ ] Can see agents list
- [ ] Can click "Test Agent"
- [ ] Microphone permission granted
- [ ] Can hear agent voice
- [ ] Agent responds to your voice

## 🎉 Quick Commands

```batch
REM Install everything
1-INSTALL.bat

REM Edit API keys
notepad v4liveKit\backend\.env

REM Start platform
2-START.bat

REM Stop platform
3-STOP.bat

REM Check backend health
curl http://localhost:8000/api/health

REM View API docs
start http://localhost:8000/docs

REM View frontend
start http://localhost:5173
```

## 💡 Pro Tips

1. **First Time Setup:**
   - Run `1-INSTALL.bat` once
   - Edit API keys in `backend\.env`
   - Run `2-START.bat` to start

2. **Daily Usage:**
   - Just run `2-START.bat` to start
   - Run `3-STOP.bat` when done

3. **Multiple Languages:**
   - Create multiple agent configs
   - Each agent can have different voice/language
   - See `GERMAN_VOICES.md` for examples

4. **Development:**
   - Backend code: `v4liveKit\backend\main.py`
   - Frontend code: `v4liveKit-frontend\src\`
   - Changes auto-reload (hot reload enabled)

5. **Production:**
   - Don't use `.bat` files in production
   - Deploy backend to Railway/Heroku
   - Deploy frontend to Vercel/Netlify
   - See `PROJECT_SETUP.md` for details

## 📊 Cost Estimates (Real Numbers)

### Small Business (1000 hours/month)
```
Azure TTS: $180/month
Azure STT: $1,000/month
OpenAI LLM: $60/month
Total: ~$1,240/month

vs ElevenLabs: ~$2,050/month
Savings: $810/month = $9,720/year! 💰
```

### Enterprise (10,000 hours/month)
```
Azure: ~$12,400/month
ElevenLabs: ~$20,500/month
Savings: $8,100/month = $97,200/year! 🤑
```

## 🚀 Next Steps

1. ✅ Run `1-INSTALL.bat`
2. ✅ Edit `backend\.env` with API keys
3. ✅ Run `2-START.bat`
4. ✅ Test voice agent in browser
5. ✅ Read `GERMAN_VOICES.md` for German support
6. ✅ Read `PROJECT_SETUP.md` for advanced features
7. ✅ Deploy to production!

## 📚 More Resources

- **Quick Start:** `QUICK_START.md`
- **German Support:** `GERMAN_VOICES.md`
- **Cost Analysis:** `WHY_AZURE_NOT_ELEVENLABS.md`
- **Full Guide:** `PROJECT_SETUP.md`
- **Backend Docs:** `backend/README.md`

## 🆘 Need Help?

1. Check logs in backend/frontend windows
2. Check browser console (F12)
3. Verify API keys in `backend\.env`
4. Run `3-STOP.bat` then `2-START.bat` again
5. Check firewall settings
6. Read troubleshooting section above

---

**Moafagh bashi! 🎉**

**Professional voice AI platform ready in 3 clicks!** ⚡

**Made with ❤️ for Windows users**
