#!/usr/bin/env python3
"""
Check call_logs table structure
"""
import sys
from pathlib import Path
from supabase import create_client, Client

def main():
    # Load environment variables from backend/.env
    env_path = Path(__file__).parent / 'v4liveKit' / 'backend' / '.env'

    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    supabase_url = env_vars.get('VITE_SUPABASE_URL')
    supabase_key = env_vars.get('VITE_SUPABASE_ANON_KEY')

    print(f"[INFO] Connecting to Supabase: {supabase_url}")

    supabase: Client = create_client(supabase_url, supabase_key)

    print("\n[INFO] Checking table structure...")
    try:
        # Try to select with limit to see structure
        result = supabase.table('call_logs').select('*').limit(1).execute()
        print(f"[SUCCESS] Table exists")
        print(f"[INFO] Data sample: {result.data}")

        # Try to get column info via information_schema if possible
        print("\n[INFO] Trying to fetch column details...")

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()
