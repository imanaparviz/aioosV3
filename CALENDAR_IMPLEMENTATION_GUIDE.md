# 📅 AIOOS Calendar & Appointment Booking System
## Complete Implementation Guide

This guide shows you how to add appointment booking functionality to your voice agents.

---

## 🎯 Overview

Your voice agent will be able to:
- **Book appointments** when users request them via voice
- **Check availability** for specific dates
- **Cancel appointments** on request
- Validate time slots against business hours
- Handle conflicts automatically

---

## 📋 Implementation Steps

### Step 1: Create Database Tables

Run the SQL schema in Supabase:

```bash
# Open Supabase SQL Editor and run:
database_schema_calendar.sql
```

This creates:
- `calendar_events` - Stores appointments
- `business_hours` - Agent availability configuration
- `availability_exceptions` - Holidays, vacations, etc.
- Helper functions for checking availability

---

### Step 2: Update Backend API

Add the calendar endpoints to your FastAPI backend:

**File: `v4liveKit/backend/main.py`**

```python
# Add at the top with other imports
from calendar_api import add_calendar_routes

# Add after app initialization (around line 42)
# Import and register calendar routes
add_calendar_routes(app, supabase)
```

**That's it!** The `calendar_api.py` file contains all endpoints.

---

### Step 3: Update Agent Worker with Tools

Add appointment booking tools to your voice agent:

**File: `v4liveKit/backend/agent_worker.py`**

```python
# Add at the top with other imports
from agent_tools import get_agent_tools

# In the entrypoint() function, after creating the assistant (around line 234)
# Add tools to the agent
if agent_id:
    # Get tools for this agent
    tools = get_agent_tools(agent_id)

    # Register tools with the assistant
    # Note: Tool registration depends on your LiveKit Agents version
    # For VoicePipelineAgent, tools are passed during initialization

    # OPTION A: If using newer API (check LiveKit docs)
    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=stt,
        llm=llm_instance,
        tts=tts,
        chat_ctx=initial_ctx,
        before_tts_cb=before_tts_callback,
        tools=tools,  # Add this line
    )

    # OPTION B: If using older API with function calls
    # Register tools after creation
    # for tool in tools:
    #     assistant.register_function(tool)

    logger.info(f"✅ Registered {len(tools)} tools for agent")
```

---

### Step 4: Configure Business Hours (Frontend)

Users can configure agent availability in the Calendar view:

1. Go to **Calendar** page
2. Select your agent from dropdown
3. Configure:
   - Working hours (per day)
   - Break times (lunch, etc.)
   - Default appointment duration
4. Click **Save Changes**

---

## 🎤 Voice Interaction Examples

### Booking an Appointment

**User:** "I need to book an appointment"

**Agent:** "Sure! I'd be happy to help you book an appointment. Could you please tell me your name?"

**User:** "My name is John Smith"

**Agent:** "Great, John. What date would you like to schedule the appointment for?"

**User:** "How about next Friday at 2pm?"

**Agent:** "Perfect! I've successfully booked your appointment for Friday, January 17, 2025 at 02:00 PM. The appointment will last 30 minutes."

---

### Checking Availability

**User:** "What times are available on Monday?"

**Agent:** "Let me check the available slots for Monday, January 13, 2025... I have the following time slots available: 09:00 AM, 09:30 AM, 10:00 AM, 11:00 AM, 02:00 PM, 03:00 PM, 04:00 PM. Which time works best for you?"

**User:** "I'll take 11am"

**Agent:** "Excellent! Could you please tell me your name for the appointment?"

---

### Canceling an Appointment

**User:** "I need to cancel my appointment on Friday at 2pm"

**Agent:** "I've successfully cancelled your appointment on Friday, January 17, 2025 at 02:00 PM."

---

## 🔧 How It Works

### Architecture Flow

```
┌─────────────┐
│    User     │ "Book me an appointment for tomorrow at 2pm"
└──────┬──────┘
       │ (Voice)
       ▼
┌─────────────────┐
│  Voice Agent    │ (agent_worker.py)
│  (LiveKit)      │ - STT: Converts speech to text
└────────┬────────┘ - LLM: Understands intent
         │          - Calls tool: book_appointment()
         ▼
┌─────────────────┐
│  Agent Tools    │ (agent_tools.py)
│                 │ - BookAppointmentTool
└────────┬────────┘ - CheckAvailabilityTool
         │          - CancelAppointmentTool
         ▼
┌─────────────────┐
│  Backend API    │ (calendar_api.py)
│  (FastAPI)      │ - /api/calendar/book
└────────┬────────┘ - /api/calendar/available-slots
         │          - /api/business-hours/{agent_id}
         ▼
┌─────────────────┐
│   Database      │ (Supabase PostgreSQL)
│  (Supabase)     │ - calendar_events
└─────────────────┘ - business_hours
                     - availability_exceptions
```

---

## 📊 Database Schema Overview

### calendar_events

```sql
- id (UUID)
- agent_id (UUID) → agents.id
- title (VARCHAR)
- event_date (DATE)
- event_time (TIME)
- duration_minutes (INTEGER)
- status (pending|confirmed|cancelled|completed)
- participant_name (VARCHAR)
- participant_email (VARCHAR)
- participant_phone (VARCHAR)
```

### business_hours

```sql
- id (UUID)
- agent_id (UUID) → agents.id (UNIQUE)
- working_hours (JSONB)
  Example: {
    "monday": [{"start": "09:00", "end": "17:00"}],
    "tuesday": [{"start": "09:00", "end": "17:00"}],
    ...
  }
- break_times (JSONB)
  Example: [{
    "name": "Lunch Break",
    "start": "12:30",
    "end": "13:30",
    "days": ["monday", "tuesday", "wednesday"]
  }]
- default_appointment_duration (INTEGER)
```

---

## 🎯 Best Practices

### 1. **Conversation Design**

✅ **DO:**
- Always confirm details before booking
- Repeat back the date/time for confirmation
- Handle missing information gracefully
- Offer alternative times if slot is unavailable

❌ **DON'T:**
- Book without user confirmation
- Assume ambiguous dates ("next week" = which day?)
- Silently fail on errors

### 2. **Error Handling**

```python
# Tool should return user-friendly messages
if slot_unavailable:
    return "That time slot is not available. Would you like me to suggest alternatives?"

# NOT this:
if slot_unavailable:
    raise Exception("Slot unavailable")  # ❌ Bad UX
```

### 3. **Data Validation**

Tools validate:
- Date format (YYYY-MM-DD)
- Time format (HH:MM)
- Past dates (rejected)
- Far future dates (>90 days, rejected)
- Conflicting appointments

### 4. **Business Hours Integration**

```sql
-- Business hours are checked via SQL function
SELECT * FROM get_available_slots(
    'agent-id',
    '2025-01-15',
    30  -- duration in minutes
);
```

Returns only slots within:
- Working hours ✓
- Not during breaks ✓
- Not already booked ✓

---

## 🚀 Testing Guide

### 1. Test Database Setup

```sql
-- Run in Supabase SQL Editor
-- Check if tables were created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('calendar_events', 'business_hours', 'availability_exceptions');
```

### 2. Test Backend APIs

```bash
# Test health check
curl http://localhost:8000/api/health

# Test get business hours
curl http://localhost:8000/api/business-hours/YOUR-AGENT-ID

# Test available slots
curl -X POST http://localhost:8000/api/calendar/available-slots \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR-AGENT-ID",
    "date": "2025-01-15",
    "duration_minutes": 30
  }'

# Test booking
curl -X POST http://localhost:8000/api/calendar/book \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR-AGENT-ID",
    "participant_name": "Test User",
    "date": "2025-01-15",
    "start_time": "14:00",
    "duration_minutes": 30
  }'
```

### 3. Test Voice Agent

1. Start your platform: `2-START.bat`
2. Open frontend: http://localhost:5173
3. Click on your German agent
4. Click "Test Agent"
5. Say: **"I want to book an appointment"**
6. Follow the conversation flow

---

## 📝 Environment Variables

Add to `.env` if needed:

```env
# Backend API URL (for agent tools)
BACKEND_API_URL=http://localhost:8000

# Supabase (already configured)
VITE_SUPABASE_URL=your-supabase-url
VITE_SUPABASE_ANON_KEY=your-anon-key
```

---

## 🐛 Troubleshooting

### Issue: "Tool not found" error

**Solution:** Make sure tools are registered with the agent:

```python
# In agent_worker.py
from agent_tools import get_agent_tools

tools = get_agent_tools(agent_id)
# Register with assistant
```

### Issue: "Time slot not available" always returns false

**Solution:** Check business hours configuration:

```sql
-- Check agent has business hours
SELECT * FROM business_hours WHERE agent_id = 'YOUR-AGENT-ID';

-- Check working hours JSON structure
SELECT working_hours FROM business_hours WHERE agent_id = 'YOUR-AGENT-ID';
```

### Issue: Agent doesn't call the booking tool

**Solution:**
1. Check LLM system instructions mention booking capability
2. Verify tool description is clear
3. Check LiveKit Agents logs for tool registration

```python
# Add to system instructions
system_instructions = """
You are a professional assistant that can help users book appointments.
When a user wants to schedule a meeting or appointment, use the book_appointment tool.
Always confirm all details before booking.
"""
```

---

## 🎨 Customization

### Custom Appointment Types

Extend `event_type` in `calendar_events`:

```sql
-- Add custom types
ALTER TABLE calendar_events
DROP CONSTRAINT IF EXISTS valid_event_type;

ALTER TABLE calendar_events
ADD CONSTRAINT valid_event_type
CHECK (event_type IN ('appointment', 'meeting', 'call', 'consultation', 'demo', 'training'));
```

### Email/SMS Notifications

Add webhook after booking:

```python
# In calendar_api.py, after creating event
await send_confirmation_email(
    to=event.participant_email,
    subject="Appointment Confirmation",
    body=f"Your appointment is confirmed for {event.event_date} at {event.event_time}"
)
```

### Multi-language Support

Tools already support German agent:

```python
# Tool responses adapt to agent language
if agent_language == "de-DE":
    return f"Perfekt! Ich habe deinen Termin für {formatted_date} um {formatted_time} gebucht."
```

---

## 📚 API Reference

### POST /api/calendar/book

Book an appointment (used by agent tool).

**Request:**
```json
{
  "agent_id": "uuid",
  "participant_name": "John Smith",
  "date": "2025-01-15",
  "start_time": "14:00",
  "duration_minutes": 30,
  "description": "Initial consultation",
  "participant_email": "john@example.com",
  "participant_phone": "+1234567890"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Appointment booked successfully",
  "event": {
    "id": "uuid",
    "title": "Appointment with John Smith",
    "event_date": "2025-01-15",
    "event_time": "14:00:00",
    "status": "confirmed"
  }
}
```

### POST /api/calendar/available-slots

Get available time slots for a date.

**Request:**
```json
{
  "agent_id": "uuid",
  "date": "2025-01-15",
  "duration_minutes": 30
}
```

**Response:**
```json
{
  "date": "2025-01-15",
  "agent_id": "uuid",
  "slots": [
    {
      "start_time": "09:00:00",
      "end_time": "09:30:00",
      "is_available": true
    },
    {
      "start_time": "09:30:00",
      "end_time": "10:00:00",
      "is_available": false
    }
  ]
}
```

### GET /api/business-hours/{agent_id}

Get business hours configuration.

**Response:**
```json
{
  "agent_id": "uuid",
  "working_hours": {
    "monday": [{"start": "09:00", "end": "17:00"}],
    "tuesday": [{"start": "09:00", "end": "17:00"}]
  },
  "break_times": [
    {
      "name": "Lunch Break",
      "start": "12:30",
      "end": "13:30",
      "days": ["monday", "tuesday"]
    }
  ],
  "default_appointment_duration": 45
}
```

---

## ✅ Summary

You now have a complete appointment booking system integrated with your voice agents!

**What you created:**
1. ✅ Database schema with 3 tables
2. ✅ Backend API with 8 endpoints
3. ✅ 3 agent tools (book, check availability, cancel)
4. ✅ Conflict detection & validation
5. ✅ Business hours management
6. ✅ Frontend calendar UI (already existed)

**Next steps:**
1. Run the SQL schema in Supabase
2. Add calendar routes to main.py
3. Add tools to agent_worker.py
4. Configure business hours via frontend
5. Test with your German agent!

---

## 🙋 Support

Questions? Check:
- LiveKit Agents Docs: https://docs.livekit.io/agents/
- Supabase Docs: https://supabase.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/

Viel Erfolg! 🚀
