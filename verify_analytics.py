#!/usr/bin/env python3
"""
Verify Analytics Setup
Check if call_logs table and analytics functions exist
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

    # Create Supabase client
    supabase: Client = create_client(supabase_url, supabase_key)

    print("\n" + "=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)

    # Check 1: Table exists
    print("\n1. Checking call_logs table...")
    try:
        result = supabase.table('call_logs').select('*').limit(1).execute()
        print("   [SUCCESS] Table 'call_logs' exists!")
        print(f"   Data count: {len(result.data)}")
    except Exception as e:
        print(f"   [ERROR] Table check failed: {e}")

    # Check 2: Try to call get_analytics_summary
    print("\n2. Checking get_analytics_summary function...")
    try:
        # This function requires auth.uid(), so it might fail with anon key
        # But if it exists, we'll get a different error
        result = supabase.rpc('get_analytics_summary', {}).execute()
        print("   [SUCCESS] Function 'get_analytics_summary' exists and works!")
        print(f"   Result: {result.data}")
    except Exception as e:
        error_msg = str(e)
        if 'PGRST202' in error_msg or 'not find the function' in error_msg:
            print(f"   [ERROR] Function 'get_analytics_summary' NOT FOUND")
        else:
            print(f"   [WARNING] Function exists but error: {e}")

    # Check 3: Try to call get_daily_call_volume
    print("\n3. Checking get_daily_call_volume function...")
    try:
        result = supabase.rpc('get_daily_call_volume', {}).execute()
        print("   [SUCCESS] Function 'get_daily_call_volume' exists and works!")
        print(f"   Result: {result.data}")
    except Exception as e:
        error_msg = str(e)
        if 'PGRST202' in error_msg or 'not find the function' in error_msg:
            print(f"   [ERROR] Function 'get_daily_call_volume' NOT FOUND")
        else:
            print(f"   [WARNING] Function exists but error: {e}")

    # Check 4: Try to call get_top_agents_analytics
    print("\n4. Checking get_top_agents_analytics function...")
    try:
        result = supabase.rpc('get_top_agents_analytics', {}).execute()
        print("   [SUCCESS] Function 'get_top_agents_analytics' exists and works!")
        print(f"   Result: {result.data}")
    except Exception as e:
        error_msg = str(e)
        if 'PGRST202' in error_msg or 'not find the function' in error_msg:
            print(f"   [ERROR] Function 'get_top_agents_analytics' NOT FOUND")
        else:
            print(f"   [WARNING] Function exists but error: {e}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("If you see any [ERROR] Function NOT FOUND, you need to:")
    print("1. Go to Supabase Dashboard -> SQL Editor")
    print("2. Open and run: v4liveKit/backend/create_call_logs.sql")
    print("=" * 60)

if __name__ == '__main__':
    main()
