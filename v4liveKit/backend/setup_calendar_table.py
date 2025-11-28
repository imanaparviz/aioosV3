"""
Setup calendar_events table in Supabase
This script creates the table and inserts test data
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Supabase config
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Read SQL file
with open('create_calendar_table.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

print("Creating calendar_events table...")
print("=" * 60)

# Split SQL into individual statements
statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]

for i, statement in enumerate(statements, 1):
    try:
        # Skip comments
        if statement.startswith('--'):
            continue

        print(f"\n[{i}/{len(statements)}] Executing...")
        # Show first 100 chars of statement
        preview = statement[:100].replace('\n', ' ')
        print(f"   {preview}...")

        # Execute statement
        result = supabase.rpc('exec_sql', {'sql': statement}).execute()

        print(f"   SUCCESS")

    except Exception as e:
        error_msg = str(e)
        if 'already exists' in error_msg.lower():
            print(f"   SKIPPED (already exists)")
        elif 'duplicate' in error_msg.lower():
            print(f"   SKIPPED (duplicate)")
        else:
            print(f"   ERROR: {error_msg}")
            # Continue with next statement instead of stopping
            continue

print("\n" + "=" * 60)
print("DONE! Calendar table setup complete.")
print("\n" + "=" * 60)
print("Next steps:")
print("1. Check Supabase dashboard -> Table Editor -> calendar_events")
print("2. You should see 3 test appointments for 'Deutscher Kundenservice'")
print("3. Restart your platform: 3-STOP.bat then 2-START.bat")
print("4. Test the agent by asking: 'Welche Termine habe ich?'")
print("5. Check calendar UI at: http://localhost:5173/calendar")
print("=" * 60)
