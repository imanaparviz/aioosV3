# ✅ Analytics Setup - Complete Guide

## Current Status

✅ **Table `call_logs` exists** - Already created in your database
❌ **Functions missing** - Need to create 3 analytics functions

## What You Need To Do

Since the analytics functions are not created yet, you need to run the SQL script manually:

### Option 1: Via Supabase Dashboard (Recommended)

1. **Open Supabase Dashboard**
   - Go to: https://wwwnfrfbynrktysnydyi.supabase.co
   - Sign in with your account

2. **Open SQL Editor**
   - Click on "SQL Editor" in the left sidebar
   - Click "New Query" button

3. **Copy & Paste SQL**
   - Open the file: `v4liveKit/backend/create_call_logs.sql`
   - Copy the ENTIRE content
   - Paste it into the SQL Editor

4. **Run the Script**
   - Click the "Run" button (or press Ctrl+Enter)
   - Wait for success message

### Option 2: Via Command Line (If you have psql)

```bash
# Navigate to backend folder
cd v4liveKit/backend

# Run SQL script
psql YOUR_DATABASE_CONNECTION_STRING -f create_call_logs.sql
```

## Verify Setup

After running the SQL script, verify it worked:

```bash
# Run verification script
python verify_analytics.py
```

You should see:
- ✅ Table 'call_logs' exists
- ✅ Function 'get_analytics_summary' exists
- ✅ Function 'get_daily_call_volume' exists
- ✅ Function 'get_top_agents_analytics' exists

## Test Analytics

1. **Start your backend**
   ```batch
   2-START.bat
   ```

2. **Make a test call**
   - Open your frontend
   - Connect to an agent
   - Talk for a few seconds
   - Hang up

3. **Check Analytics Page**
   - Go to Analytics page in frontend
   - You should see your call logged
   - Charts should update with data

## Troubleshooting

### Functions still not working?

Make sure you ran the ENTIRE SQL script, including:
- `CREATE OR REPLACE FUNCTION get_analytics_summary(...)`
- `CREATE OR REPLACE FUNCTION get_daily_call_volume(...)`
- `CREATE OR REPLACE FUNCTION get_top_agents_analytics(...)`

### No data showing up?

Check if calls are being logged:
```sql
-- Run this in SQL Editor
SELECT * FROM call_logs ORDER BY created_at DESC LIMIT 10;
```

If no rows exist, the backend might not be logging calls. Check:
- Backend is running (`2-START.bat`)
- No errors in backend console
- Agent is properly configured

## What These Functions Do

1. **get_analytics_summary**: Returns overall stats (total calls, duration, cost, success rate)
2. **get_daily_call_volume**: Returns calls per day for charts
3. **get_top_agents_analytics**: Returns most active agents

---

**Need Help?** Check the backend logs or Supabase logs for errors.
