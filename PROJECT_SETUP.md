# AIOOS Voice AI Platform - Complete Setup Guide

Professional voice AI platform ba LiveKit + Azure/OpenAI/Deepgram

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Cost Analysis](#cost-analysis)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Running the Platform](#running-the-platform)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

AIOOS is a professional voice AI platform that connects your users with intelligent voice agents. It's built with:

- **Backend**: Python FastAPI + LiveKit Agents
- **Frontend**: Vue 3 + LiveKit Client
- **AI Services**: Azure Speech (TTS/STT), OpenAI (LLM), Deepgram (STT)
- **Database**: Supabase (optional)

### Key Features

✅ **Real-time Voice Communication** - Powered by LiveKit
✅ **Natural Voice AI** - Azure Neural voices (high quality, low cost)
✅ **Smart LLM** - GPT-4o-mini for intelligent responses
✅ **Professional UI** - Vue 3 with Tailwind CSS
✅ **Cost Optimized** - 5x cheaper than ElevenLabs!
✅ **Production Ready** - Scalable architecture

## 🏗️ Architecture

```
┌─────────────────┐
│  Vue Frontend   │ (Port 5173)
│  (User Interface)│
└────────┬────────┘
         │ HTTP/WebSocket
         ▼
┌─────────────────┐
│ FastAPI Backend │ (Port 8000)
│  (API Server)   │
└────────┬────────┘
         │ LiveKit API
         ▼
┌─────────────────┐       ┌──────────────┐
│  LiveKit Cloud  │◄──────┤ Agent Worker │
│   (Rooms/SFU)   │       │  (Voice AI)  │
└────────┬────────┘       └──────┬───────┘
         │                        │
         │                        ▼
         │              ┌─────────────────┐
         │              │  AI Services:   │
         │              │  - Azure TTS/STT│
         │              │  - OpenAI LLM   │
         │              │  - Deepgram STT │
         │              └─────────────────┘
         ▼
┌─────────────────┐
│    Supabase     │
│   (Database)    │
└─────────────────┘
```

## 💰 Cost Analysis

### Why We DON'T Use ElevenLabs

| Service | Cost per 1M chars | Quality | Verdict |
|---------|------------------|---------|---------|
| **Azure TTS** | ~$4 | Excellent ⭐ | ✅ **BEST VALUE** |
| OpenAI TTS | ~$15 | Very Good | ✅ Good alternative |
| ElevenLabs | ~$22 | Excellent | ❌ Too expensive! |

**Result**: Azure saves you **$18 per 1M characters** compared to ElevenLabs!

For 1M characters per month:
- Azure: **$4/month** 💚
- ElevenLabs: **$22/month** 💸

**Quality**: Azure Neural voices are incredibly natural and often **better** than ElevenLabs!

## 📦 Prerequisites

### Required Software

1. **Python 3.9+**
   ```bash
   python3 --version
   ```

2. **Node.js 16+**
   ```bash
   node --version
   ```

3. **Git**
   ```bash
   git --version
   ```

### Required API Keys

1. **LiveKit** (FREE tier available!)
   - Sign up: https://cloud.livekit.io
   - Get: URL, API Key, API Secret

2. **Azure Speech** (Best value!)
   - Portal: https://portal.azure.com
   - Create "Speech Services"
   - Region: North Europe (cheapest!)
   - Get: Key, Region

3. **OpenAI** (For LLM)
   - Portal: https://platform.openai.com
   - Get: API Key
   - Add credits (GPT-4o-mini is very cheap!)

4. **Deepgram** (Optional - for STT)
   - Portal: https://deepgram.com
   - Free tier available!
   - Get: API Key

5. **Supabase** (Optional - for database)
   - Portal: https://supabase.com
   - Free tier available!
   - Get: URL, Anon Key

## 🚀 Quick Start

### 1. Clone Repository

```bash
cd /mnt/c/agents/ba-khodam/aioosBaKhodam
```

### 2. Backend Setup

```bash
# Go to backend
cd v4liveKit/backend

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env file
nano .env  # or vim .env

# Add your API keys:
# - LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
# - OPENAI_API_KEY
# - AZURE_SPEECH_KEY, AZURE_SPEECH_REGION
# - DEEPGRAM_API_KEY (optional)
# - SUPABASE_URL, SUPABASE_KEY (optional)

# Activate venv
source venv/bin/activate

# Run server
python main.py
```

Backend runs at: **http://localhost:8000**

### 3. Frontend Setup

```bash
# Open new terminal
cd /mnt/c/agents/ba-khodam/aioosBaKhodam/v4liveKit-frontend

# Install dependencies
npm install

# Check .env file
cat .env

# Should have:
# VITE_API_URL=http://localhost:8000
# VITE_SUPABASE_URL=...
# VITE_SUPABASE_ANON_KEY=...

# Run dev server
npm run dev
```

Frontend runs at: **http://localhost:5173**

## 🔧 Backend Setup (Detailed)

### Directory Structure

```
v4liveKit/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── agent_worker.py      # Voice agent
│   ├── requirements.txt     # Dependencies
│   ├── .env                 # Config (gitignored)
│   ├── .env.example         # Example config
│   ├── setup.sh             # Setup script
│   └── README.md            # Backend docs
├── examples/
│   └── azure_voice_assistant.py
├── livekit-agents/          # LiveKit SDK
└── livekit-plugins/         # AI plugins
```

### Install Dependencies

```bash
cd v4liveKit/backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
. venv/Scripts/activate  # Windows

# Install packages
pip install -r requirements.txt

# Install LiveKit agents
cd ..
pip install -e ./livekit-agents
pip install -e ./livekit-plugins/livekit-plugins-azure
pip install -e ./livekit-plugins/livekit-plugins-openai
pip install -e ./livekit-plugins/livekit-plugins-deepgram
pip install -e ./livekit-plugins/livekit-plugins-silero
cd backend
```

### Configure Environment

```bash
cp .env.example .env
nano .env
```

Required variables:
```bash
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=northeurope
```

### Run Backend

```bash
python main.py
```

Or with hot reload:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs: **http://localhost:8000/docs**

## 🎨 Frontend Setup (Detailed)

### Directory Structure

```
v4liveKit-frontend/
├── src/
│   ├── App.vue              # Root component
│   ├── main.js              # Entry point
│   ├── components/          # UI components
│   ├── views/               # Pages
│   │   ├── AgentTestView.vue    # Test agents
│   │   ├── DashboardView.vue    # Dashboard
│   │   └── ...
│   ├── services/
│   │   └── api.js           # API client
│   ├── stores/              # Pinia stores
│   └── router/              # Vue Router
├── public/
├── package.json
├── vite.config.js
└── .env
```

### Install Dependencies

```bash
cd v4liveKit-frontend
npm install
```

### Configure Environment

```bash
# .env should have:
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://...
VITE_SUPABASE_ANON_KEY=...
```

### Run Frontend

```bash
npm run dev
```

Open: **http://localhost:5173**

### Build for Production

```bash
npm run build
npm run preview
```

## 🎯 Configuration

### Backend Configuration

Edit `backend/.env`:

```bash
# AI Service Providers
DEFAULT_TTS_PROVIDER=azure      # azure, openai
DEFAULT_TTS_VOICE=en-US-JennyNeural
DEFAULT_STT_PROVIDER=azure      # azure, deepgram
DEFAULT_STT_LANGUAGE=en-US
DEFAULT_LLM_MODEL=gpt-4o-mini

# Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO
```

### Frontend Configuration

Edit `frontend/src/services/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### Agent Configuration

In `backend/agent_worker.py`, you can customize:

- TTS voice (150+ Azure voices available!)
- STT language
- LLM model and temperature
- System instructions
- Greeting message

Example:
```python
tts_voice = "en-US-JennyNeural"  # Female, friendly
# or "en-US-GuyNeural"            # Male, professional
# or "fa-IR-DilaraNeural"         # Farsi female
```

## 🏃 Running the Platform

### Development Mode

**Terminal 1 - Backend:**
```bash
cd v4liveKit/backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd v4liveKit-frontend
npm run dev
```

**Terminal 3 - Agent Worker (optional):**
```bash
cd v4liveKit/backend
source venv/bin/activate
python agent_worker.py dev
```

### Access Platform

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧪 Testing

### 1. Test Backend Health

```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "services": {
    "livekit": "configured",
    "supabase": "connected"
  }
}
```

### 2. Test Frontend Connection

Open browser console:
```javascript
// In browser console
fetch('http://localhost:8000/api/agents')
  .then(r => r.json())
  .then(console.log)
```

### 3. Test Voice Agent

1. Go to http://localhost:5173
2. Login / Signup
3. Go to "Test Agent"
4. Select an agent
5. Click "Start Voice Test"
6. Allow microphone access
7. Speak naturally!

## 🚀 Deployment

### Backend Deployment

**Option 1: Railway.app**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

**Option 2: Heroku**
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create aioos-backend
git push heroku main
```

**Option 3: VPS (Ubuntu)**
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone and setup
cd /opt
git clone <repo>
cd v4liveKit/backend
./setup.sh

# Create systemd service
sudo nano /etc/systemd/system/aioos.service

# Enable and start
sudo systemctl enable aioos
sudo systemctl start aioos

# Configure nginx reverse proxy
sudo nano /etc/nginx/sites-available/aioos
```

### Frontend Deployment

**Option 1: Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd v4liveKit-frontend
vercel
```

**Option 2: Netlify**
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build and deploy
npm run build
netlify deploy --prod
```

## 🔍 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -i :8000
kill -9 <PID>
```

**Import errors:**
```bash
# Reinstall LiveKit agents
cd v4liveKit
pip install -e ./livekit-agents
```

**LiveKit connection fails:**
- Check LIVEKIT_URL starts with `wss://`
- Verify API Key and Secret
- Test at https://cloud.livekit.io

**Azure voice not working:**
- Check AZURE_SPEECH_KEY and AZURE_SPEECH_REGION
- Make sure region matches (e.g., `northeurope`)
- Try different voice name

### Frontend Issues

**API connection fails:**
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check .env has correct VITE_API_URL
cat .env
```

**LiveKit connection fails:**
- Check browser console for errors
- Verify microphone permissions
- Check CORS settings in backend

**Build errors:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
```

### Agent Issues

**Agent not responding:**
- Check backend logs
- Verify API keys are correct
- Check LiveKit dashboard for active rooms

**Poor voice quality:**
- Try different Azure voice (e.g., `en-US-AriaNeural`)
- Check internet connection
- Verify AZURE_SPEECH_REGION is closest to you

**High latency:**
- Use Deepgram for STT (faster than Azure)
- Choose closer LiveKit region
- Optimize system instructions (shorter = faster)

## 📚 Resources

### Documentation
- [LiveKit Docs](https://docs.livekit.io)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Vue 3 Docs](https://vuejs.org)
- [Azure Speech Docs](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [OpenAI Docs](https://platform.openai.com/docs)

### Azure Voices
- [Voice Gallery](https://speech.microsoft.com/portal/voicegallery)
- [Language Support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support)

### Community
- [LiveKit Slack](https://livekit.io/join-slack)
- [LiveKit Discord](https://discord.gg/livekit)

## 🎉 Success Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:5173
- [ ] Health check returns "healthy"
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can see agents list in frontend
- [ ] Can start voice test
- [ ] Microphone access granted
- [ ] Can hear agent speaking
- [ ] Agent responds to voice input

## 📞 Support

Age moshkeli dashti:

1. Check logs in terminal
2. Check browser console (F12)
3. Verify all API keys are correct
4. Test each service individually
5. Check firewall/antivirus settings

---

**Sakht shode ba ❤️ bara AIOOS Platform**

**Cost Optimized • High Quality • Production Ready**
