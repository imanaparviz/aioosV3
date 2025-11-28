# 📝 Conversation Summary Feature - Analysis & Implementation Plan

## 🔍 Current Status: **NOT IMPLEMENTED**

After searching the entire codebase, I found that:

### ❌ What's Missing:
1. **No transcript storage** - Conversations are NOT being saved to database
2. **No conversation summary** - No LLM summarization after calls
3. **No transcript field** in `call_logs` table
4. **No summary field** in `call_logs` table

### ✅ What EXISTS:
- Call metadata is saved (start_time, end_time, duration, cost, status)
- Agent worker connects and handles calls
- STT (Speech-to-Text) is working during calls via Azure/Deepgram
- TTS (Text-to-Speech) is working

### 🤔 Why Transcripts Aren't Saved:
The agent worker (`agent_worker.py`) handles real-time conversation but:
- STT transcription happens in real-time for the agent to understand
- Transcription is processed and discarded (not saved anywhere)
- Only metadata gets saved to `call_logs` table at the end

---

## 🎯 Implementation Plan

To add conversation summary feature, we need to:

### Phase 1: Save Transcripts ✍️

#### 1.1 Update Database Schema
```sql
-- Add transcript and summary fields to call_logs
ALTER TABLE call_logs ADD COLUMN transcript TEXT;
ALTER TABLE call_logs ADD COLUMN transcript_json JSONB;  -- Detailed with timestamps
ALTER TABLE call_logs ADD COLUMN summary TEXT;
ALTER TABLE call_logs ADD COLUMN summary_json JSONB;     -- Structured summary
```

#### 1.2 Update Agent Worker to Save Transcripts

**File**: `v4liveKit/backend/agent_worker.py`

Add transcript collection:
```python
# At the top, add:
conversation_transcript = []

# During conversation, capture STT results:
@session.on("user_speech_committed")
def on_user_speech(text: str):
    conversation_transcript.append({
        "role": "user",
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    })

@session.on("agent_speech_committed")
def on_agent_speech(text: str):
    conversation_transcript.append({
        "role": "agent",
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    })

# In finally block, save transcript:
if conversation_transcript:
    # Convert to text format
    transcript_text = "\n".join([
        f"{msg['role'].upper()}: {msg['text']}"
        for msg in conversation_transcript
    ])

    # Save to database
    update_data["transcript"] = transcript_text
    update_data["transcript_json"] = conversation_transcript
```

---

### Phase 2: Generate AI Summary 🤖

#### 2.1 Add Summary Generation Function

**File**: Create new file `v4liveKit/backend/summarizer.py`

```python
"""
Conversation Summarizer - Generate AI summaries of call transcripts
"""
import openai
import os
from typing import Dict, List

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_call_summary(transcript: List[Dict]) -> Dict:
    """
    Generate structured summary using GPT-4

    Returns:
    {
        "summary": "Brief overview...",
        "key_points": ["Point 1", "Point 2", ...],
        "customer_sentiment": "positive/neutral/negative",
        "action_items": ["Action 1", "Action 2", ...],
        "tags": ["appointment", "billing", "support"]
    }
    """
    # Convert transcript to text
    conversation = "\n".join([
        f"{msg['role'].upper()}: {msg['text']}"
        for msg in transcript
    ])

    # GPT-4 prompt for summarization
    prompt = f"""You are an AI assistant that summarizes customer service calls.

Analyze the following conversation and provide a structured summary.

CONVERSATION:
{conversation}

Provide a JSON response with:
1. "summary": A brief 2-3 sentence overview
2. "key_points": Array of main discussion points
3. "customer_sentiment": "positive", "neutral", or "negative"
4. "action_items": Array of follow-up actions needed
5. "tags": Array of relevant tags (e.g., "appointment", "billing", "support")

Respond ONLY with valid JSON."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",  # Fast and cheap
        messages=[
            {"role": "system", "content": "You are a call summarization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )

    import json
    summary_data = json.loads(response.choices[0].message.content)

    return summary_data
```

#### 2.2 Update Agent Worker to Generate Summary

**File**: `v4liveKit/backend/agent_worker.py`

In the `finally` block, after saving transcript:

```python
# Generate AI summary if transcript exists
if conversation_transcript and len(conversation_transcript) > 2:
    try:
        from summarizer import generate_call_summary

        logger.info("🤖 Generating AI summary...")
        summary_data = await generate_call_summary(conversation_transcript)

        # Add to update data
        update_data["summary"] = summary_data.get("summary", "")
        update_data["summary_json"] = summary_data

        logger.info(f"✅ Summary generated: {summary_data.get('summary', '')[:100]}...")
    except Exception as e:
        logger.error(f"❌ Failed to generate summary: {e}")
```

---

### Phase 3: Display in Frontend 🎨

#### 3.1 Add Summary Tab to Call Detail Page

**Create**: `v4liveKit-frontend/src/views/CallDetailView.vue`

```vue
<template>
  <div class="call-detail">
    <h1>Call Details</h1>

    <!-- Tabs -->
    <div class="tabs">
      <button @click="activeTab = 'summary'" :class="{active: activeTab === 'summary'}">
        Summary
      </button>
      <button @click="activeTab = 'transcript'" :class="{active: activeTab === 'transcript'}">
        Full Transcript
      </button>
      <button @click="activeTab = 'metadata'" :class="{active: activeTab === 'metadata'}">
        Metadata
      </button>
    </div>

    <!-- Summary Tab -->
    <div v-if="activeTab === 'summary'" class="summary-view">
      <h2>AI Summary</h2>
      <p class="summary-text">{{ call.summary }}</p>

      <h3>Key Points</h3>
      <ul>
        <li v-for="point in call.summary_json?.key_points" :key="point">
          {{ point }}
        </li>
      </ul>

      <h3>Sentiment</h3>
      <span :class="`sentiment-badge ${call.summary_json?.customer_sentiment}`">
        {{ call.summary_json?.customer_sentiment }}
      </span>

      <h3>Action Items</h3>
      <ul class="action-items">
        <li v-for="action in call.summary_json?.action_items" :key="action">
          <input type="checkbox" /> {{ action }}
        </li>
      </ul>

      <h3>Tags</h3>
      <div class="tags">
        <span v-for="tag in call.summary_json?.tags" :key="tag" class="tag">
          {{ tag }}
        </span>
      </div>
    </div>

    <!-- Transcript Tab -->
    <div v-if="activeTab === 'transcript'" class="transcript-view">
      <div v-for="msg in call.transcript_json" :key="msg.timestamp"
           :class="`message ${msg.role}`">
        <strong>{{ msg.role.toUpperCase() }}:</strong> {{ msg.text }}
        <span class="timestamp">{{ formatTime(msg.timestamp) }}</span>
      </div>
    </div>

    <!-- Metadata Tab -->
    <div v-if="activeTab === 'metadata'">
      <!-- Call metadata: duration, cost, agent, etc. -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCallById } from '@/services/api'

const route = useRoute()
const call = ref({})
const activeTab = ref('summary')

onMounted(async () => {
  const callId = route.params.id
  call.value = await getCallById(callId)
})

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString()
}
</script>
```

#### 3.2 Update CallLogsView to Link to Detail

In `CallLogsView.vue`, the caller ID already links to detail page:
```vue
<router-link :to="`/call-logs/${log.id}`">
  {{ log.callerId }}
</router-link>
```

Just need to add the route in `router/index.js`:
```javascript
{
  path: '/call-logs/:id',
  name: 'CallDetail',
  component: () => import('../views/CallDetailView.vue')
}
```

---

## 💰 Cost Estimation

**Using GPT-4o-mini for summarization:**
- Cost: ~$0.15 per 1M input tokens
- Average call: ~500 tokens (5 min conversation)
- Cost per summary: **~$0.00008** (less than 0.01 cent!)

**Storage:**
- PostgreSQL text storage is cheap
- 100k calls with transcripts: ~500MB
- Supabase Free Tier: 500MB database ✅

---

## 🚀 Quick Implementation (Minimal)

If you want to start simple:

### Option A: Basic Text Summary (No AI)
Just save transcript as plain text:
```python
# Simple transcript without AI summary
transcript_text = "\n".join([f"{role}: {text}" for role, text in messages])
supabase.table("call_logs").update({"transcript": transcript_text}).eq("id", call_id).execute()
```

### Option B: Full AI Summary (Recommended)
Follow all 3 phases above for complete feature.

---

## 📊 What You'll Get

After implementation:

1. **Call Logs Table** - Add "View Summary" button
2. **Call Detail Page** with tabs:
   - **Summary Tab**: AI-generated summary, key points, sentiment, action items
   - **Transcript Tab**: Full conversation with timestamps
   - **Metadata Tab**: Call info (duration, cost, agent, etc.)

3. **Search by Summary**: Add full-text search on summaries
4. **Analytics**: Aggregate insights (sentiment trends, common issues, etc.)

---

## ⏱️ Implementation Time

- **Phase 1** (Save Transcripts): ~1-2 hours
- **Phase 2** (AI Summary): ~2-3 hours
- **Phase 3** (Frontend UI): ~3-4 hours

**Total**: 6-9 hours for complete feature

---

## 🎯 Priority

**Recommend**: Start with Phase 1 (save transcripts) immediately.

This way you start collecting data NOW, and can add AI summary later.

**Quick Start:**
1. Run SQL to add transcript fields
2. Update agent_worker.py to save transcripts
3. Deploy and make test calls
4. Later: Add AI summarization and UI

---

## ❓ Questions?

Let me know if you want me to implement this feature! I can:
- ✅ Write the code for all 3 phases
- ✅ Create the database migrations
- ✅ Build the frontend UI
- ✅ Test everything end-to-end

**Mikhay shoro' konim?** 🚀
