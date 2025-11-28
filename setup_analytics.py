#!/usr/bin/env python3
"""
Setup Analytics Tables in Supabase
Reads create_call_logs.sql and executes it via Supabase REST API
"""
import os
import sys
from pathlib import Path
from supabase import create_client, Client

def main():
    # Load environment variables from backend/.env
    env_path = Path(__file__).parent / 'v4liveKit' / 'backend' / '.env'

    # Simple env parser
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    supabase_url = env_vars.get('VITE_SUPABASE_URL')
    supabase_key = env_vars.get('VITE_SUPABASE_ANON_KEY')

    if not supabase_url or not supabase_key:
        print("[ERROR] VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY not found in .env")
        sys.exit(1)

    print(f"[INFO] Connecting to Supabase: {supabase_url}")

    # Read SQL file
    sql_path = Path(__file__).parent / 'v4liveKit' / 'backend' / 'create_call_logs.sql'
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    print("[INFO] SQL script loaded")
    print("=" * 60)

    # Create Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    print("[INFO] Executing SQL script...")
    print("=" * 60)

    try:
        # Execute SQL via RPC
        # Note: We need service_role key for DDL operations
        # The anon key might not have permission, but let's try
        result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()

        print("[SUCCESS] SQL executed successfully!")
        print(f"Result: {result}")

    except Exception as e:
        # If RPC doesn't work, we'll need to execute manually or use service_role key
        print(f"[WARNING] Could not execute via RPC: {e}")
        print("\n[INFO] MANUAL SETUP REQUIRED:")
        print("=" * 60)
        print("1. Go to your Supabase Dashboard")
        print("2. Navigate to SQL Editor")
        print("3. Create a new query")
        print("4. Copy the content from: v4liveKit/backend/create_call_logs.sql")
        print("5. Run the query")
        print("=" * 60)

        # Still, let's try to check if table exists
        try:
            result = supabase.table('call_logs').select('id').limit(1).execute()
            print("\n[SUCCESS] Table 'call_logs' already exists!")
        except Exception as check_error:
            print(f"\n[ERROR] Table 'call_logs' does not exist yet: {check_error}")

    print("\n[INFO] Setup process completed!")
    print("Next steps:")
    print("1. Verify in Supabase Dashboard that 'call_logs' table exists")
    print("2. Check that functions are created: get_analytics_summary, get_daily_call_volume, get_top_agents_analytics")
    print("3. Restart your backend: 3-STOP.bat && 2-START.bat")

if __name__ == '__main__':
    main()
