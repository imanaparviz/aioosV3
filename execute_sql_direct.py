#!/usr/bin/env python3
"""
Execute SQL directly via Supabase Management API
This requires SUPABASE_SERVICE_ROLE_KEY, not just anon key
"""
import os
import sys
import requests
from pathlib import Path

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
    # We need service_role key, not anon key for DDL operations
    service_key = env_vars.get('SUPABASE_SERVICE_ROLE_KEY') or env_vars.get('VITE_SUPABASE_ANON_KEY')

    if not supabase_url or not service_key:
        print("[ERROR] VITE_SUPABASE_URL and service role key not found in .env")
        print("\n[INFO] To use service_role key:")
        print("1. Go to Supabase Dashboard -> Settings -> API")
        print("2. Copy the 'service_role' key (not anon key)")
        print("3. Add to .env: SUPABASE_SERVICE_ROLE_KEY=your_key_here")
        sys.exit(1)

    print(f"[INFO] Connecting to Supabase: {supabase_url}")

    # Read SQL file
    sql_path = Path(__file__).parent / 'v4liveKit' / 'backend' / 'create_call_logs.sql'
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    print("[INFO] SQL script loaded")
    print("=" * 60)

    # Split SQL into separate statements
    statements = []
    current_statement = []
    in_function = False

    for line in sql_content.split('\n'):
        current_statement.append(line)

        # Track if we're inside a function (they end with $$;)
        if 'CREATE' in line.upper() and 'FUNCTION' in line.upper():
            in_function = True

        # End of statement
        if in_function and line.strip().endswith('$$;'):
            statements.append('\n'.join(current_statement))
            current_statement = []
            in_function = False
        elif not in_function and line.strip().endswith(';') and not line.strip().startswith('--'):
            statements.append('\n'.join(current_statement))
            current_statement = []

    print(f"[INFO] Split into {len(statements)} SQL statements")

    # Execute each statement via REST API
    headers = {
        'apikey': service_key,
        'Authorization': f'Bearer {service_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

    success_count = 0
    error_count = 0

    for i, statement in enumerate(statements, 1):
        statement = statement.strip()
        if not statement or statement.startswith('--'):
            continue

        print(f"\n[INFO] Executing statement {i}/{len(statements)}...")
        print(f"Preview: {statement[:100]}...")

        # Use PostgreSQL REST API endpoint
        # Note: This is not standard Supabase REST API, might not work
        # Better approach is to use psql or dashboard
        try:
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/query",
                headers=headers,
                json={'query': statement}
            )

            if response.status_code < 300:
                print(f"   [SUCCESS] Statement executed")
                success_count += 1
            else:
                print(f"   [ERROR] Failed: {response.status_code} - {response.text}")
                error_count += 1
        except Exception as e:
            print(f"   [ERROR] Exception: {e}")
            error_count += 1

    print("\n" + "=" * 60)
    print(f"RESULT: {success_count} successful, {error_count} errors")
    print("=" * 60)

    if error_count > 0:
        print("\n[WARNING] Some statements failed!")
        print("Recommended: Execute SQL manually in Supabase Dashboard:")
        print("1. Go to Supabase Dashboard -> SQL Editor")
        print("2. Copy content from: v4liveKit/backend/create_call_logs.sql")
        print("3. Paste and click Run")

if __name__ == '__main__':
    main()
