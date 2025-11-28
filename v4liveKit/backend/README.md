# AIOOS Backend Server

Professional FastAPI backend bara AIOOS Voice AI Platform.

## Features

- ✅ **LiveKit Integration** - Room management & token generation
- ✅ **Voice Agents** - Spawn AI agents with Azure/OpenAI/Deepgram
- ✅ **RESTful API** - Complete API bara frontend
- ✅ **Supabase Ready** - Optional database integration
- 💰 **Cost Optimized** - Azure TTS is 5x cheaper than ElevenLabs!
- 🎯 **High Quality** - Azure Neural voices are comparable or better

## Why Azure over ElevenLabs?

### Cost Comparison:
- **Azure TTS**: ~$4 per 1M characters ⭐
- **OpenAI TTS**: ~$15 per 1M characters
- **ElevenLabs**: ~$22 per 1M characters ❌ (Too expensive!)

### Quality:
Azure Neural voices are incredibly natural and sometimes **better** than ElevenLabs!

Top Azure voices:
- `en-US-JennyNeural` - Female, warm, friendly ⭐ Recommended
- `en-US-GuyNeural` - Male, professional, clear
- `en-US-AriaNeural` - Female, conversational

[Full voice list](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support)

## Setup

### 1. Run Setup Script

```bash
cd backend
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment

Edit `backend/.env` and add your API keys:

```bash
# Required
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
OPENAI_API_KEY=sk-...
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=northeurope
DEEPGRAM_API_KEY=your_key

# Optional
SUPABASE_URL=https://...
SUPABASE_KEY=your_key
```

### 3. Get API Keys

#### LiveKit (Free tier available!)
1. Go to https://cloud.livekit.io
2. Sign up with GitHub
3. Create a project
4. Copy URL, API Key, and API Secret

#### Azure Speech (Best value!)
1. Go to https://portal.azure.com
2. Create "Speech Services" resource
3. Choose "North Europe" region (cheapest!)
4. Copy Key and Region

#### OpenAI
1. Go to https://platform.openai.com
2. Create API key
3. Add credits (GPT-4o-mini is very cheap!)

#### Deepgram (Optional - for STT)
1. Go to https://deepgram.com
2. Sign up and get API key
3. Free tier available!

### 4. Run Server

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
. venv/Scripts/activate  # Windows

# Run server
python main.py
```

Server runs at: http://localhost:8000

## API Endpoints

### Health Check
```
GET /api/health
```

### Agents

```
GET  /api/agents          - List all agents
GET  /api/agents/{id}     - Get agent by ID
POST /api/agents          - Create new agent
POST /api/agents/{id}/test - Test agent in browser
```

### Rooms

```
POST /api/rooms/create    - Create LiveKit room with agent
```

### Stats

```
GET  /api/stats           - Get platform statistics
```

## API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Agent Worker

The `agent_worker.py` file contains the voice agent logic.

**Features:**
- Azure TTS/STT (default - best value!)
- OpenAI TTS (alternative)
- Deepgram STT (alternative)
- Configurable via environment variables
- Natural conversation handling
- Chat message support

**Running standalone:**

```bash
python agent_worker.py dev
```

## Project Structure

```
backend/
├── main.py              # FastAPI server
├── agent_worker.py      # Voice agent worker
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (gitignored)
├── .env.example         # Example environment file
├── setup.sh             # Setup script
└── README.md            # This file
```

## Development

### Install in dev mode:

```bash
pip install -e .
```

### Hot reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production, use proper process management:

```bash
# Using gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Or using supervisor/systemd
```

## Troubleshooting

### Port 8000 already in use

```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Import errors

Make sure you installed LiveKit agents:

```bash
cd ..
pip install -e ./livekit-agents
pip install -e ./livekit-plugins/livekit-plugins-azure
```

### LiveKit connection fails

- Check your LIVEKIT_URL, API_KEY, and API_SECRET in .env
- Make sure URL starts with `wss://`
- Test connection at https://cloud.livekit.io

### Azure voice not working

- Check AZURE_SPEECH_KEY and AZURE_SPEECH_REGION
- Make sure region matches your Azure resource
- Common regions: `northeurope`, `westeurope`, `eastus`

## Support

- LiveKit Docs: https://docs.livekit.io
- Azure Speech Docs: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/
- OpenAI Docs: https://platform.openai.com/docs

---

**Made with ❤️ by AIOOS Team**
