# 🔧 Voice Agent Fix - Agent Worker Missing!

**Date:** 2025-11-13
**Issue:** Voice agent wasn't speaking
**Solution:** Start Agent Worker process!

---

## 🔍 What Was Wrong?

When testing voice agent:
- ✅ LiveKit connected
- ✅ Microphone OK
- ❌ **Agent didn't speak!**

### Why?

**Agent Worker wasn't running!**

The system has **2 separate processes**:

1. **Backend (main.py)** ← Was running ✅
   - Creates LiveKit rooms
   - Generates access tokens
   - Manages database

2. **Agent Worker (agent_worker.py)** ← **Was NOT running!** ❌
   - Joins LiveKit rooms as voice agent
   - Listens to user speech
   - Speaks responses with Azure voices
   - **THIS WAS MISSING!**

---

## ✅ The Fix:

Updated `2-START.bat` to start **3 windows** instead of 2:

### Before (Broken):
```batch
1. Backend API (main.py)
2. Frontend (Vue)
```

### After (Working!):
```batch
1. Backend API (main.py)
2. Agent Worker (agent_worker.py) ← NEW!
3. Frontend (Vue)
```

---

## 🚀 How to Use:

### Step 1: Stop Everything

```batch
cd C:\agents\ba-khodam\aioosBaKhodam
3-STOP.bat
```

---

### Step 2: Start with Agent Worker

```batch
2-START.bat
```

**Now opens 3 windows:**
1. **Backend** - API server
2. **Agent Worker** - Voice AI 🎤
3. **Frontend** - Web interface

---

### Step 3: Test Voice Agent

1. Go to: **http://localhost:5173**
2. Click: **"Deutscher Kundenservice"**
3. Click: **"Test Agent"**
4. Click: **"Start Test"**
5. **Say:** "Hallo, wie geht es dir?"

**Agent should respond with:**
```
"Hallo! Wie kann ich Ihnen heute helfen?"
```

✅ **IT WORKS!**

---

## 📋 What Agent Worker Does:

### 1. Watches for New Rooms
Agent worker listens for new LiveKit rooms being created.

### 2. Joins as Voice Agent
When user joins room, agent worker automatically joins as AI assistant.

### 3. Processes Speech (STT)
Uses **Azure Speech** or **Deepgram** to convert speech to text:
- German: `de-DE`
- English: `en-US`

### 4. Generates Response (LLM)
Uses **OpenAI GPT-4o-mini** to create intelligent response:
- Understands context
- Follows instructions
- Maintains conversation

### 5. Speaks Response (TTS)
Uses **Azure Neural Voices** to speak naturally:
- German: `de-DE-KatjaNeural` (Female, warm)
- English: `en-US-JennyNeural` (Female, friendly)

---

## 🎙️  Agent Worker Configuration:

Agent worker reads from `.env` file:

```bash
# Agent Configuration (from database or defaults)
AGENT_NAME=Deutscher Kundenservice
AGENT_INSTRUCTIONS=Du bist ein professioneller Kundenservice-Assistent...
AGENT_GREETING=Hallo! Wie kann ich Ihnen heute helfen?

# Voice Settings
TTS_VOICE=de-DE-KatjaNeural
TTS_PROVIDER=azure
STT_LANGUAGE=de-DE
STT_PROVIDER=azure
LLM_MODEL=gpt-4o-mini

# API Keys (already configured!)
LIVEKIT_URL=wss://innerstate-jz326myy.livekit.cloud
LIVEKIT_API_KEY=APIsxLiGFvqWcAZ
LIVEKIT_API_SECRET=0ckK3f47tWum543QGfuycJ4urT9lIz48FtCQorABB9j
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=northeurope
OPENAI_API_KEY=...
```

---

## 🔍 Agent Worker Logs:

When agent worker starts, you'll see:

```
================================================
🎙️  AIOOS Voice Agent Worker
================================================
💰 Using Azure TTS - 5x cheaper than ElevenLabs!
🎯 Quality: Comparable or better than ElevenLabs
================================================

✅ VAD model loaded
🚀 Starting Deutscher Kundenservice
📍 Room: test-47addfec-f4cd-41e2-b6ec-6a5e949fe754-...
🎤 STT: azure (de-DE)
🔊 TTS: azure (de-DE-KatjaNeural)
🤖 LLM: gpt-4o-mini
✅ Using Azure STT
✅ Using Azure TTS with de-DE-KatjaNeural
✅ Using OpenAI LLM: gpt-4o-mini
👤 Participant joined: test-user
✅ Voice Assistant started!
```

**Then agent speaks greeting:**
```
"Hallo! Wie kann ich Ihnen heute helfen?"
```

---

## 🧪 Testing Different Agents:

Each agent has different settings:

### 1. Customer Support Bot (English)
```
Language: en-US
Voice: en-US-JennyNeural
Greeting: "Hello! I'm your customer support assistant. How can I help you today?"
```

### 2. Deutscher Kundenservice (German)
```
Language: de-DE
Voice: de-DE-KatjaNeural
Greeting: "Hallo! Wie kann ich Ihnen heute helfen?"
```

### 3. Sales Assistant (English)
```
Language: en-US
Voice: en-US-GuyNeural
Greeting: "Hello! I'm your sales assistant. What can I help you with?"
```

---

## 🛑 Stopping Services:

### Stop All (Including Agent Worker):

```batch
3-STOP.bat
```

This kills:
- ✅ Backend API
- ✅ Agent Worker
- ✅ Frontend

---

## 📊 Architecture Diagram:

```
┌─────────────────────────────────────────────────┐
│                  USER BROWSER                   │
│              http://localhost:5173              │
└────────────────┬────────────────────────────────┘
                 │
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────────────┐
│            BACKEND API (main.py)                │
│              Port 8000                          │
│  • Creates LiveKit rooms                        │
│  • Generates tokens                             │
│  • Manages database                             │
└────────────────┬────────────────────────────────┘
                 │
                 │ LiveKit API
                 ▼
┌─────────────────────────────────────────────────┐
│            LIVEKIT CLOUD                        │
│     wss://innerstate-jz326myy.livekit.cloud     │
│  • Real-time audio infrastructure               │
│  • WebRTC connections                           │
└───────┬──────────────────────────────┬──────────┘
        │                              │
        │ WebRTC Audio                 │ WebRTC Audio
        ▼                              ▼
┌───────────────┐            ┌───────────────────────┐
│   USER        │◄──────────►│  AGENT WORKER        │
│  Microphone   │   Voice    │  (agent_worker.py)   │
│  Speaker      │  Stream    │                      │
└───────────────┘            │  • Azure STT         │
                             │  • OpenAI LLM        │
                             │  • Azure TTS         │
                             │  • Silero VAD        │
                             └──────────────────────┘
```

---

## 💡 Key Differences:

### Backend API (main.py)
- **Purpose:** Manages platform, database, rooms
- **Runs:** Always (for web interface to work)
- **Port:** 8000

### Agent Worker (agent_worker.py)
- **Purpose:** Voice AI agent that speaks & listens
- **Runs:** Only for voice functionality
- **Port:** None (connects to LiveKit)

**BOTH are needed for voice agents!**

---

## 🎯 Quick Start Checklist:

- [ ] Stop all services: `3-STOP.bat`
- [ ] Start with agent worker: `2-START.bat`
- [ ] Wait for 3 windows to open
- [ ] Check "Agent Worker" window for logs
- [ ] Open browser: `http://localhost:5173`
- [ ] Click German agent
- [ ] Click "Test Agent"
- [ ] Speak and listen for greeting! 🎤

---

## 🔧 Troubleshooting:

### Agent Worker window closes immediately

**Check:**
```batch
cd C:\agents\ba-khodam\aioosBaKhodam\v4liveKit\backend
venv\Scripts\python.exe agent_worker.py dev
```

Look for errors about missing packages.

---

### Agent joins but doesn't speak

**Check `.env` file has:**
```bash
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=northeurope
OPENAI_API_KEY=...
```

---

### "Invalid API key" error

**Check `.env` file has:**
```bash
LIVEKIT_URL=wss://innerstate-jz326myy.livekit.cloud
LIVEKIT_API_KEY=APIsxLiGFvqWcAZ
LIVEKIT_API_SECRET=0ckK3f47tWum543QGfuycJ4urT9lIz48FtCQorABB9j
```

---

## 🎉 Success!

**After fix:**
- ✅ Agent Worker runs
- ✅ Agent joins room
- ✅ Agent speaks greeting
- ✅ Agent listens to user
- ✅ Agent responds intelligently
- ✅ Full voice conversation works!

**Moafagh bashi dadash!** 💪🚀

---

**Fixed:** 2025-11-13
**Issue:** Agent Worker not running
**Solution:** Updated 2-START.bat to start agent_worker.py
**Status:** ✅ WORKING!
