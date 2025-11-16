# 🚀 AIOOS - Quick Start Guide

Berim ba 3 ghadam platform ro bolandesh konim!

## Step 1: Get API Keys (10 daghighe)

### LiveKit (FREE!) ⭐
1. Boro https://cloud.livekit.io
2. Sign up ba GitHub
3. Create project
4. Copy: URL, API Key, API Secret

### Azure Speech (BEST VALUE!) 💰
1. Boro https://portal.azure.com
2. Create "Speech Services" resource
3. Region: **North Europe** (arzoontar!)
4. Copy: Key, Region

### OpenAI (Bara LLM) 🤖
1. Boro https://platform.openai.com
2. Create API key
3. Add credits ($5-10 kheili kafe!)

### Deepgram (Optional - bara STT) 🎤
1. Boro https://deepgram.com
2. Sign up (free tier dare!)
3. Copy API key

## Step 2: Setup Backend (5 daghighe)

```bash
# Boro backend directory
cd v4liveKit/backend

# Run setup script
chmod +x setup.sh
./setup.sh

# Edit .env file
nano .env  # ya vim .env

# Add your API keys:
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=northeurope
DEEPGRAM_API_KEY=your_key

# Save and close (Ctrl+X, Y, Enter)

# Run backend
source venv/bin/activate
python main.py
```

✅ Backend running at: **http://localhost:8000**

## Step 3: Setup Frontend (2 daghighe)

Open **NEW terminal**:

```bash
# Boro frontend directory
cd v4liveKit-frontend

# Install dependencies (yek bar!)
npm install

# Check .env
cat .env

# Should have:
# VITE_API_URL=http://localhost:8000

# Run frontend
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

## Step 4: Test It! (1 daghighe)

1. Open browser: http://localhost:5173
2. Sign up / Login
3. Go to **"Test Agent"**
4. Select agent
5. Click **"Start Voice Test"**
6. Allow microphone
7. **Harf bezan!** 🎤

## Easy Startup (Next Time)

### Option 1: Automatic (ba tmux)

```bash
chmod +x START_PROJECT.sh
./START_PROJECT.sh
```

### Option 2: Manual (2 terminals)

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

## Troubleshooting

### Backend nemiad bala:

```bash
# Check port 8000
lsof -i :8000
kill -9 <PID>

# Check .env file
cat backend/.env

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Frontend nemiad bala:

```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check .env
cat .env
```

### LiveKit connection error:

- Check LIVEKIT_URL has `wss://` at start
- Check API Key & Secret are correct
- Test at https://cloud.livekit.io

### Voice kar nemikone:

- Check AZURE_SPEECH_KEY & AZURE_SPEECH_REGION
- Check browser microphone permission
- Check backend logs

## Quick Commands

```bash
# Check backend health
curl http://localhost:8000/api/health

# View backend logs
cd v4liveKit/backend
source venv/bin/activate
python main.py

# View frontend in browser
open http://localhost:5173

# Stop everything
# Press Ctrl+C in each terminal
```

## Cost Estimates

For **1000 concurrent users / month**:

| Service | Usage | Cost |
|---------|-------|------|
| LiveKit | 1000 hours | **FREE** (10,000 hours free) |
| Azure TTS | 1M chars | **$4** ⭐ |
| OpenAI LLM | 100M tokens | **~$20** |
| Deepgram STT | 1000 hours | **~$12** |
| **Total** | | **~$36/month** 💚 |

Age ElevenLabs estefade mikardi:
- ElevenLabs: **$22** faqat bara 1M chars!
- Total: **~$54/month** ❌

**Savings: $18/month** ba Azure! 🎉

## Success Checklist

- [ ] Backend runs at http://localhost:8000
- [ ] Frontend runs at http://localhost:5173
- [ ] Health check: `curl http://localhost:8000/api/health`
- [ ] Can login to frontend
- [ ] Can see agents list
- [ ] Can start voice test
- [ ] Mic permission granted
- [ ] Can hear agent voice
- [ ] Agent responds to my voice

## Next Steps

1. **Read Full Docs**: `PROJECT_SETUP.md`
2. **Customize Agent**: Edit `backend/agent_worker.py`
3. **Add More Voices**: Check Azure voice gallery
4. **Deploy to Production**: See deployment section in docs

---

**Moafagh bashi! 🚀**

Age soali dashti, check `PROJECT_SETUP.md` bara detailed guide.
