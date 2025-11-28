# 🔧 Troubleshooting Guide: Analytics & Transcripts

If you are seeing **404 Not Found** errors for analytics or missing transcripts, follow these steps.

## 1. Enable Transcripts (Database Setup)

You MUST run the SQL script to create the transcript fields in your database.

1. Go to your **Supabase Dashboard**.
2. Go to **SQL Editor**.
3. Click **New Query**.
4. Copy the content of: `v4liveKit/backend/add_transcript_fields.sql`
5. Click **Run**.

## 2. Fix 404 Errors (Backend Restart)

The backend might be running an old version of the code. We need to force-kill it.

1. **Stop Everything**:
   Double-click `3-STOP.bat`.
   *Wait 10 seconds.*

2. **Verify Stopped**:
   Open a terminal and run:
   ```powershell
   netstat -ano | findstr :8000
   ```
   If you see any output, run `3-STOP.bat` again!

3. **Start Fresh**:
   Double-click `2-START.bat`.

4. **Check Logs**:
   Look at the **Backend** window. You should see:
   > 🚀 Starting AIOOS Backend Server (WITH ANALYTICS FIX)...
   > 📋 Registered Routes:
   >    - /api/analytics/summary [GET]
   >    - /api/analytics/chart [GET]
   >    ...

   If you see "WITH ANALYTICS FIX" and the routes listed, it is working!

## 3. Test It

1. Open http://localhost:5173/analytics
2. It should load without errors (might show 0s if no calls yet).
3. Make a test call to an agent.
4. Hang up.
5. Refresh the Analytics page.
