# 📊 Real Analytics Setup Guide

To enable real analytics for your voice agents, you need to create the `call_logs` table and helper functions in your Supabase database.

## 1. Run SQL Script

1. Go to your **Supabase Dashboard**.
2. Go to the **SQL Editor** (on the left sidebar).
3. Click **New Query**.
4. Copy and paste the content of `v4liveKit/backend/create_call_logs.sql`.
5. Click **Run**.

## 2. Verify Setup

After running the script, you should see:
- A new table `call_logs`.
- 3 new functions: `get_analytics_summary`, `get_daily_call_volume`, `get_top_agents_analytics`.

## 3. Restart Backend

If your backend is running, restart it to ensure it picks up any changes (though not strictly necessary for database changes, it's good practice).

```batch
3-STOP.bat
2-START.bat
```

## 4. Test It

1. Make a call to an agent.
2. Talk for a few seconds.
3. Hang up.
4. Go to the **Analytics** page in the frontend.
5. You should see the call count increase and the chart update!

## Notes

- **Cost Estimation**: The system estimates cost based on call duration ($0.10/hour placeholder). You can adjust this logic in `agent_worker.py`.
- **Data Retention**: The analytics functions default to showing data for the last 30 days.
