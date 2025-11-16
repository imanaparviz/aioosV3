# 🔧 Fix Calendar & Agent Tools Issue

## Problem Discovered

Your calendar UI and agent tools are empty because:
- ❌ Backend expects: `calendar_events` table
- ✅ Database has: `appointments` table

This is why when you ask the agent "Welche Termine habe ich?" (What appointments do I have?), it says yes but the calendar is empty!

---

## Solution: Create `calendar_events` Table

Follow these steps to create the missing table and add test data:

### Step 1: Open Supabase Dashboard

1. Go to [https://supabase.com](https://supabase.com)
2. Log in to your account
3. Select your project: **aioosBaKhodam** (or your project name)

### Step 2: Open SQL Editor

1. Click on **SQL Editor** in the left sidebar (icon looks like `</>`)
2. Click **"New Query"** button

### Step 3: Copy & Run SQL

1. Open the file: `v4liveKit/backend/create_calendar_table.sql`
2. Copy ALL the SQL code
3. Paste it into the Supabase SQL Editor
4. Click **"Run"** button (or press Ctrl+Enter)

You should see:
```
Success. No rows returned
```

### Step 4: Verify Table Created

1. Go to **Table Editor** in left sidebar
2. You should see a new table: `calendar_events`
3. Click on it
4. You should see 3 test appointments:
   - Hans Müller - Nov 14, 10:00 AM (confirmed)
   - Anna Schmidt - Nov 15, 2:30 PM (pending)
   - Thomas Weber - Nov 18, 11:00 AM (confirmed)

All for agent: "Deutscher Kundenservice"

### Step 5: Test the Calendar

1. Go to your frontend: `http://localhost:5173/calendar`
2. Select agent: **Deutscher Kundenservice**
3. Navigate to **November 2025**
4. You should see the 3 appointments displayed!

### Step 6: Test the Agent

1. Click on agent "Deutscher Kundenservice"
2. Click **"Test Agent"**
3. Ask: **"Welche Termine habe ich?"** (What appointments do I have?)
4. The agent should respond with the 3 appointments!

Expected response:
```
Sie haben 3 Termine:

1. Freitag, 14. November 2025 um 10:00 Uhr - Beratungstermin mit Hans Müller (45 Minuten)
2. Samstag, 15. November 2025 um 14:30 Uhr - Termin mit Frau Schmidt (30 Minuten)
3. Dienstag, 18. November 2025 um 11:00 Uhr - Telefongespräch mit Herr Weber (30 Minuten)
```

---

## Alternative: Run via psql (Advanced)

If you have `psql` installed:

```bash
cd v4liveKit/backend

# Get your database connection string from Supabase:
# Settings -> Database -> Connection string (URI)

psql "your-connection-string" -f create_calendar_table.sql
```

---

## What This Fixes

After creating the table:

✅ **Calendar UI** will show appointments
✅ **Agent tools** will work:
   - `get_my_appointments` - Shows appointments
   - `book_appointment` - Books new appointments
   - `check_availability` - Checks free slots
   - `cancel_appointment` - Cancels appointments

✅ **Agent can:**
   - Answer "Welche Termine habe ich?" correctly
   - Book appointments when you ask
   - Check available times
   - Cancel appointments

---

## Testing the Full Flow

### 1. Check Existing Appointments
**Ask:** "Welche Termine habe ich diese Woche?"
**Expected:** Agent lists the 3 test appointments

### 2. Check Availability
**Ask:** "Wann haben Sie am Montag Zeit?"
**Expected:** Agent shows available time slots

### 3. Book New Appointment
**Ask:** "Ich möchte einen Termin für Freitag um 15 Uhr buchen. Mein Name ist Peter Wagner."
**Expected:** Agent books the appointment and confirms

### 4. Verify in Calendar
1. Go to calendar UI
2. Navigate to the date
3. You should see the new appointment!

---

## Troubleshooting

### Issue: SQL fails with "permission denied"

**Solution:** Make sure you're running the SQL in Supabase SQL Editor, NOT via the Python script (anon key doesn't have permission to create tables).

### Issue: Table already exists

**Solution:** The SQL has `CREATE TABLE IF NOT EXISTS`, so it's safe to run multiple times. If table exists, it will just insert test data.

### Issue: Foreign key constraint fails

**Solution:** Make sure your `agents` table has the agent with ID `47addfec-f4cd-41e2-b6ec-6a5e949fe754`. If not, update the INSERT statements in the SQL with your actual agent ID.

### Issue: Agent still says "no appointments"

**Solution:**
1. Check backend logs for errors
2. Make sure agent_id matches in both table and agent_worker.py
3. Restart the platform: `3-STOP.bat` then `2-START.bat`

---

## Next Steps

After the table is created and you've tested it:

1. **Add more appointments** via the calendar UI "Create Event" button
2. **Test booking via voice** - ask the agent to book appointments
3. **Configure business hours** in the calendar UI
4. **Add calendar tool to other agents** if needed

---

## Files Created

- `v4liveKit/backend/create_calendar_table.sql` - SQL to create table
- `v4liveKit/backend/setup_calendar_table.py` - Python helper (won't work with anon key)
- `FIX_CALENDAR_ISSUE.md` - This guide

---

**Need Help?** Check the calendar API implementation in:
- `v4liveKit/backend/calendar_api.py` - Backend API
- `v4liveKit/backend/agent_tools_v2.py` - Agent tools
- `v4liveKit-frontend/src/views/CalendarView.vue` - Frontend UI
