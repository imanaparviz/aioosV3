# 🚀 AIOOS Voice AI Platform - Linux Installation Guide

Complete setup guide for running the AIOOS Voice AI Platform on Linux (Ubuntu/Debian).

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Prerequisites Installation](#prerequisites-installation)
3. [Project Setup](#project-setup)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)
8. [Architecture Overview](#architecture-overview)

---

## 🖥️ System Requirements

- **OS**: Ubuntu 20.04+ / Debian 11+ (or any modern Linux distribution)
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Storage**: 2GB free space
- **Internet**: Stable connection for API calls

---

## 📦 Prerequisites Installation

### 1. Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Python 3.10+

```bash
# Check Python version
python3 --version

# If Python < 3.10, install it:
sudo apt install python3.10 python3.10-venv python3-pip -y
```

### 3. Install Node.js 18+

```bash
# Using NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Verify installation
node --version  # Should be v18.x or higher
npm --version   # Should be 9.x or higher
```

### 4. Install Git

```bash
sudo apt install git -y
```

### 5. Install Additional Dependencies

```bash
# For PDF processing
sudo apt install poppler-utils -y

# For system builds
sudo apt install build-essential -y
```

---

## 🛠️ Project Setup

### 1. Clone or Copy the Project

If you have the project folder, navigate to it:

```bash
cd /path/to/aioosBaKhodam
```

Or clone from repository (if available):

```bash
git clone <repository-url>
cd aioosBaKhodam
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd v4liveKit/backend

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install LiveKit Agents framework
cd ..
pip install -e livekit-agents
pip install -e livekit-plugins/livekit-plugins-openai
pip install -e livekit-plugins/livekit-plugins-azure
pip install -e livekit-plugins/livekit-plugins-deepgram
pip install -e livekit-plugins/livekit-plugins-silero

cd backend
```

### 3. Frontend Setup

Open a **new terminal** and run:

```bash
cd /path/to/aioosBaKhodam/v4liveKit/frontend

# Install Node.js dependencies
npm install

# This will install:
# - Vue 3
# - Vite
# - Tailwind CSS
# - Supabase client
# - Vue Router
```

---

## ⚙️ Configuration

### 1. Create Backend Environment File

```bash
cd v4liveKit/backend

# Copy example environment file
cp .env.example .env

# Edit the .env file
nano .env  # or use vim, gedit, etc.
```

### 2. Configure Environment Variables

Edit the `.env` file with your API keys:

```bash
# ============================================
# LIVEKIT CONNECTION (REQUIRED!)
# ============================================
# Get free tier at: https://cloud.livekit.io
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here

# ============================================
# AI SERVICES (REQUIRED!)
# ============================================

# OpenAI (for LLM + RAG Embeddings)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Deepgram (for Speech-to-Text)
DEEPGRAM_API_KEY=xxxxxxxxxxxxx

# Azure Speech (for Text-to-Speech - BEST VALUE!)
AZURE_SPEECH_KEY=xxxxxxxxxxxxx
AZURE_SPEECH_REGION=northeurope  # or your region

# ============================================
# DATABASE (REQUIRED for multi-user!)
# ============================================

# Supabase (for agents, calendar, knowledge base)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# ============================================
# AGENT DEFAULTS
# ============================================

DEFAULT_TTS_PROVIDER=azure
DEFAULT_TTS_VOICE=en-US-JennyNeural  # or de-DE-KatjaNeural for German
DEFAULT_STT_PROVIDER=azure
DEFAULT_STT_LANGUAGE=en-US
DEFAULT_LLM_MODEL=gpt-4o-mini
DEFAULT_LLM_TEMPERATURE=0.7

# ============================================
# SERVER CONFIG
# ============================================

BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_RELOAD=true
LOG_LEVEL=INFO
```

### 3. Get Required API Keys

#### LiveKit (Free Tier Available)
1. Go to https://cloud.livekit.io
2. Sign up for free account
3. Create a new project
4. Copy: **URL**, **API Key**, **API Secret**

#### OpenAI
1. Go to https://platform.openai.com
2. Create account / Login
3. Go to API Keys section
4. Create new key
5. **Important**: Add credits ($5-10 recommended)

#### Deepgram (Free Trial: 45,000 minutes)
1. Go to https://deepgram.com
2. Sign up for free
3. Get API key from dashboard

#### Azure Speech (Free Tier: 5 hours/month)
1. Go to https://portal.azure.com
2. Create Speech Service resource
3. Choose Free (F0) tier
4. Get Key and Region from resource

#### Supabase (Free Tier Available)
1. Go to https://supabase.com
2. Create new project
3. Copy **Project URL** and **anon public key**

---

## 🗄️ Database Setup

### 1. Enable pgvector Extension in Supabase

Go to your Supabase Dashboard → SQL Editor → New Query:

```sql
-- Enable pgvector extension for RAG/Knowledge Base
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Create Required Tables

Run the following SQL in Supabase SQL Editor:

```sql
-- ============================================
-- AGENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS agents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    system_instructions TEXT,
    tts_provider TEXT DEFAULT 'azure',
    tts_voice TEXT DEFAULT 'en-US-JennyNeural',
    stt_provider TEXT DEFAULT 'azure',
    stt_language TEXT DEFAULT 'en-US',
    llm_model TEXT DEFAULT 'gpt-4o-mini',
    llm_temperature FLOAT DEFAULT 0.7,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies for agents
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own agents" ON agents
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own agents" ON agents
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own agents" ON agents
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own agents" ON agents
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- CALENDAR TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies for calendar
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own calendar events" ON calendar_events
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own calendar events" ON calendar_events
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own calendar events" ON calendar_events
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own calendar events" ON calendar_events
    FOR DELETE USING (auth.uid() = user_id);

-- ============================================
-- KNOWLEDGE BASE TABLE (RAG System)
-- ============================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size_bytes INTEGER,
    content_preview TEXT,
    upload_status TEXT DEFAULT 'processing',
    total_chunks INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    knowledge_base_id UUID REFERENCES knowledge_base(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies for knowledge base
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own knowledge base" ON knowledge_base
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own knowledge base" ON knowledge_base
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own knowledge base" ON knowledge_base
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own document chunks" ON document_chunks
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM knowledge_base kb
            WHERE kb.id = document_chunks.knowledge_base_id
            AND kb.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert own document chunks" ON document_chunks
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM knowledge_base kb
            WHERE kb.id = document_chunks.knowledge_base_id
            AND kb.user_id = auth.uid()
        )
    );

-- Auto-populate user_id trigger
CREATE OR REPLACE FUNCTION set_user_id_from_auth()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.user_id IS NULL THEN
    NEW.user_id := auth.uid();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER set_user_id_knowledge_base
  BEFORE INSERT ON knowledge_base
  FOR EACH ROW
  EXECUTE FUNCTION set_user_id_from_auth();

-- Vector search function
CREATE OR REPLACE FUNCTION search_knowledge_base(
  query_embedding vector(1536),
  agent_uuid uuid,
  match_threshold double precision DEFAULT 0.3,
  match_count integer DEFAULT 5
)
RETURNS TABLE (
  chunk_id uuid,
  content text,
  similarity double precision,
  file_name text,
  metadata jsonb
)
LANGUAGE plpgsql
SECURITY DEFINER  -- Bypass RLS for search
AS $$
BEGIN
  RETURN QUERY
  SELECT
    dc.id AS chunk_id,
    dc.content,
    1 - (dc.embedding <=> query_embedding) AS similarity,
    kb.file_name,
    dc.metadata
  FROM document_chunks dc
  JOIN knowledge_base kb ON dc.knowledge_base_id = kb.id
  WHERE
    dc.agent_id = agent_uuid
    AND dc.embedding IS NOT NULL
    AND 1 - (dc.embedding <=> query_embedding) > match_threshold
  ORDER BY dc.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Create index for faster vector search
CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx
ON document_chunks
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 3. Create Your First User

Go to Supabase Dashboard → Authentication → Users → Add User

Or sign up through your frontend application.

---

## 🚀 Running the Application

### Terminal 1: Start Backend

```bash
cd v4liveKit/backend

# Activate virtual environment
source venv/bin/activate

# Start FastAPI backend
python3 main.py

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start Frontend

```bash
cd v4liveKit/frontend

# Start Vite development server
npm run dev

# You should see:
# VITE v5.4.21  ready in XXX ms
# ➜  Local:   http://localhost:5173/
```

### Access the Application

Open your browser and go to:

```
http://localhost:5173
```

You should see the AIOOS Voice AI Platform!

---

## 🧪 Testing the Setup

### 1. Test Backend API

```bash
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2025-11-16T..."}
```

### 2. Test Agent Creation

1. Open browser: http://localhost:5173
2. Log in with Supabase credentials
3. Go to "Agents" page
4. Create a new agent
5. Test voice conversation

### 3. Test Knowledge Base (RAG)

1. Go to "Knowledge Base" page
2. Select an agent
3. Upload a `.txt` or `.pdf` file
4. Wait for processing (status: "Completed")
5. Test voice conversation asking about the uploaded document

---

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Backend shows "404 Not Found" for `/api/agents`

**Solution:**
Check that `main.py` includes the agent routes:
```bash
grep "include_router" v4liveKit/backend/main.py
```

### Issue: Frontend shows blank page

**Solution:**
```bash
# Check browser console for errors
# Verify backend is running on port 8000
curl http://localhost:8000/health

# Rebuild frontend
cd v4liveKit/frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Issue: "CORS policy" error in browser

**Solution:**
Backend `main.py` should have CORS middleware configured for `http://localhost:5173`

### Issue: Knowledge Base upload fails

**Solution:**
1. Check OpenAI API key is valid
2. Verify Supabase pgvector extension is enabled
3. Check backend logs for errors

### Issue: Voice agent doesn't respond

**Solution:**
1. Verify LiveKit credentials in `.env`
2. Check OpenAI API key has credits
3. Check Azure Speech / Deepgram keys are valid
4. Look at backend terminal for error messages

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     USER BROWSER                         │
│              http://localhost:5173                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│               FRONTEND (Vue 3 + Vite)                   │
│  - Agent Management UI                                  │
│  - Knowledge Base UI (RAG)                              │
│  - Calendar UI                                          │
│  - Voice Chat Interface                                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│            BACKEND (FastAPI + Python)                   │
│               http://localhost:8000                     │
│                                                          │
│  Routes:                                                │
│  - /api/agents       → Agent CRUD                       │
│  - /api/calendar     → Calendar Events                  │
│  - /api/knowledge    → RAG File Upload/Search          │
│  - /api/token        → LiveKit Token Generation        │
│                                                          │
│  Services:                                              │
│  - agent_worker.py   → LiveKit Voice Agent             │
│  - agent_tools_v2.py → Calendar + Knowledge Tools      │
│  - knowledge_api.py  → RAG Processing (Embeddings)     │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│  LiveKit   │ │ Supabase │ │  AI Services │
│  Cloud     │ │ Database │ │              │
│            │ │          │ │ - OpenAI     │
│ - WebRTC   │ │ - Agents │ │ - Deepgram   │
│ - Audio    │ │ - Events │ │ - Azure      │
│ - Rooms    │ │ - Files  │ │              │
└────────────┘ └──────────┘ └──────────────┘
```

### Key Components:

1. **Frontend (Vue 3)**
   - Single Page Application (SPA)
   - Tailwind CSS for styling
   - Supabase client for authentication
   - LiveKit client for voice chat

2. **Backend (FastAPI)**
   - RESTful API server
   - LiveKit Agents framework
   - RAG (Retrieval-Augmented Generation)
   - Calendar management
   - File processing

3. **Database (Supabase)**
   - PostgreSQL with pgvector
   - Row Level Security (RLS)
   - Real-time subscriptions
   - Authentication & Storage

4. **AI Services**
   - **OpenAI**: GPT-4o-mini for LLM + text-embedding-3-small for RAG
   - **Deepgram**: Fast speech-to-text
   - **Azure Speech**: High-quality text-to-speech (best value!)

---

## 📚 Additional Resources

- **LiveKit Documentation**: https://docs.livekit.io
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vue 3 Docs**: https://vuejs.org

---

## 🆘 Getting Help

If you encounter issues:

1. Check backend terminal for error messages
2. Check browser console for frontend errors
3. Verify all API keys are correct
4. Ensure database tables are created
5. Test API endpoints individually with `curl`

---

## 🎉 Success!

If everything is working:

✅ Backend running on `http://localhost:8000`
✅ Frontend running on `http://localhost:5173`
✅ Voice agents responding
✅ Calendar working
✅ Knowledge Base (RAG) operational

**You're all set! Enjoy your AI voice agents! 🚀**

---

*Last Updated: 2025-11-16*
