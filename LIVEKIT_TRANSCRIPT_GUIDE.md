# 📚 LiveKit Transcript & Recording - Implementation Guide

## ✅ What LiveKit Docs Tell Us

Based on official LiveKit documentation, we have TWO ways to save conversation data:

---

## 🎤 Option 1: Audio/Video Recording (Egress)

**Uses**: LiveKit Egress Service
**Saves**: Audio/video files to S3, GCS, or Azure Blob

### How it Works:
```python
from livekit import api

async def entrypoint(ctx: JobContext):
    # Start recording when agent joins
    req = api.RoomCompositeEgressRequest(
        room_name=ctx.room.name,
        audio_only=True,  # or False for video
        file_outputs=[
            api.EncodedFileOutput(
                file_type=api.EncodedFileType.OGG,
                filepath="recordings/call.ogg",
                s3=api.S3Upload(
                    bucket=os.getenv("AWS_BUCKET_NAME"),
                    region=os.getenv("AWS_REGION"),
                    access_key=os.getenv("AWS_ACCESS_KEY_ID"),
                    secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
                )
            )
        ],
    )

    lkapi = api.LiveKitAPI()
    res = await lkapi.egress.start_room_composite_egress(req)
    await lkapi.aclose()

    # Rest of agent code...
```

**Output**: Audio file saved to S3/GCS/Azure

---

## 📝 Option 2: Text Transcripts (Recommended!)

**Uses**: `session.history` property
**Saves**: Full conversation as JSON

### How it Works:

```python
from datetime import datetime
import json

def entrypoint(ctx: JobContext):
    # Define transcript save function
    async def write_transcript():
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/tmp/transcript_{ctx.room.name}_{current_date}.json"

        with open(filename, 'w') as f:
            json.dump(session.history.to_dict(), f, indent=2)

        print(f"Transcript for {ctx.room.name} saved to {filename}")

    # Register shutdown callback
    ctx.add_shutdown_callback(write_transcript)

    # Rest of agent code...
```

### What `session.history` Contains:

```json
{
  "messages": [
    {
      "role": "user",
      "text": "Hello, I need help",
      "timestamp": "2024-11-24T10:15:30Z"
    },
    {
      "role": "assistant",
      "text": "Hello! How can I help you today?",
      "timestamp": "2024-11-24T10:15:32Z"
    }
  ]
}
```

---

## 🎯 OUR Implementation Plan

### Phase 1: Save Transcripts to Database ✍️

**Step 1: Add Database Fields**

Already documented in `CONVERSATION_SUMMARY_FEATURE.md`:
```sql
ALTER TABLE call_logs ADD COLUMN transcript TEXT;
ALTER TABLE call_logs ADD COLUMN transcript_json JSONB;
```

**Step 2: Update `agent_worker.py`**

Add shutdown callback to save transcript:

```python
async def entrypoint(ctx: JobContext):
    # ... existing code ...

    # Define transcript save function
    async def save_transcript_to_db():
        if session and session.history:
            try:
                # Get conversation history
                history_dict = session.history.to_dict()

                # Format as text
                transcript_text = "\n".join([
                    f"{msg.get('role', 'unknown').upper()}: {msg.get('text', '')}"
                    for msg in history_dict.get('messages', [])
                ])

                # Save to database
                if call_log_id:
                    supabase.table("call_logs").update({
                        "transcript": transcript_text,
                        "transcript_json": history_dict
                    }).eq("id", call_log_id).execute()

                    logger.info(f"✅ Transcript saved for call: {call_log_id}")
            except Exception as e:
                logger.error(f"❌ Failed to save transcript: {e}")

    # Register shutdown callback BEFORE connecting
    ctx.add_shutdown_callback(save_transcript_to_db)

    # ... rest of code ...
```

---

## 🔄 Real-Time Events (Optional)

LiveKit also provides real-time events:

### 1. `conversation_item_added`
Triggered when new message added to chat history:

```python
@session.on("conversation_item_added")
async def on_item_added(item):
    print(f"New message: {item.text}")
    # Save to database in real-time
```

### 2. `user_input_transcribed`
Triggered when user speech transcribed:

```python
@session.on("user_input_transcribed")
async def on_transcribed(text):
    print(f"User said: {text}")
```

---

## 📊 What We'll Build

### Minimal Version (Phase 1 - Recommended Start):
1. ✅ Save `session.history` to database on call end
2. ✅ Store as both text and JSON
3. ✅ Display in Call Logs UI

### Complete Version (Phase 2 & 3):
1. ✅ Everything from Phase 1
2. ✅ Generate AI summary with GPT-4o-mini
3. ✅ Beautiful UI with tabs (Summary, Transcript, Metadata)
4. ✅ Sentiment analysis
5. ✅ Action items extraction

---

## 🚀 Implementation Steps

### Step 1: Database Setup (5 min)
```sql
-- Run in Supabase SQL Editor
ALTER TABLE call_logs ADD COLUMN transcript TEXT;
ALTER TABLE call_logs ADD COLUMN transcript_json JSONB;
ALTER TABLE call_logs ADD COLUMN summary TEXT;
ALTER TABLE call_logs ADD COLUMN summary_json JSONB;
```

### Step 2: Update Agent Worker (30 min)
- Add `ctx.add_shutdown_callback(save_transcript_to_db)`
- Implement `save_transcript_to_db()` function
- Test with a call

### Step 3: Test (5 min)
- Make a test call
- Check database: `SELECT transcript FROM call_logs WHERE id='...'`
- Should see conversation!

### Step 4: Add AI Summary (Optional - 1 hour)
- Create `summarizer.py`
- Generate summary on shutdown
- Save to database

### Step 5: Build UI (Optional - 2 hours)
- Create `CallDetailView.vue`
- Add tabs for Summary/Transcript
- Style beautifully

---

## 💡 Key Insights from LiveKit Docs

1. **`session.history`** is the key! It contains full conversation
2. **`add_shutdown_callback`** runs when call ends - perfect for saving
3. **Transcriptions are automatic** - LiveKit handles STT for us
4. **Real-time events** available if we need live updates
5. **Recording (Egress)** is separate - for audio/video files

---

## 🎯 Next Steps

**Want me to implement Phase 1 now?** (Save transcripts to database)

It's just:
1. Run SQL (2 min)
2. Update `agent_worker.py` (15 min)
3. Test (5 min)

**Total time: ~20 minutes!** 🚀

Should we do it?
