"""
Test server to debug route registration
"""
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Set working directory
os.chdir(r'C:\agents\ba-khodam\aioosBaKhodam\v4liveKit\backend')
sys.path.insert(0, r'C:\agents\ba-khodam\aioosBaKhodam\v4liveKit\backend')

print("=" * 60)
print("TESTING BACKEND SERVER")
print("=" * 60)

try:
    print("\n1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   [OK] FastAPI imported")

    print("\n2. Importing knowledge_api...")
    from knowledge_api import add_knowledge_routes
    print("   [OK] knowledge_api imported")

    print("\n3. Importing calendar_api...")
    from calendar_api import add_calendar_routes
    print("   [OK] calendar_api imported")

    print("\n4. Creating Supabase client...")
    from supabase import create_client
    SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")

    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"   [OK] Supabase client created: {SUPABASE_URL[:30]}...")
    else:
        supabase = None
        print("   [WARN] No Supabase credentials")

    print("\n5. Creating FastAPI app...")
    app = FastAPI(title="Test Server")
    print("   [OK] FastAPI app created")

    print("\n6. Registering calendar routes...")
    if supabase:
        add_calendar_routes(app, supabase)
        print("   [OK] Calendar routes registered")
    else:
        print("   [WARN] Skipped (no Supabase)")

    print("\n7. Registering knowledge routes...")
    if supabase:
        add_knowledge_routes(app, supabase)
        print("   [OK] Knowledge routes registered")
    else:
        print("   [WARN] Skipped (no Supabase)")

    print("\n8. Listing all routes:")
    print("-" * 60)
    for route in app.routes:
        if hasattr(route, 'path'):
            methods = list(route.methods) if hasattr(route, 'methods') else ['GET']
            print(f"   {methods[0]:6s} {route.path}")
    print("-" * 60)

    print("\n9. Checking knowledge routes specifically:")
    knowledge_routes = [r for r in app.routes if hasattr(r, 'path') and 'knowledge' in r.path]
    if knowledge_routes:
        print(f"   [OK] Found {len(knowledge_routes)} knowledge routes:")
        for r in knowledge_routes:
            methods = list(r.methods) if hasattr(r, 'methods') else ['GET']
            print(f"      {methods[0]:6s} {r.path}")
    else:
        print("   [ERROR] NO KNOWLEDGE ROUTES FOUND!")

    print("\n" + "=" * 60)
    print("[OK] ALL TESTS PASSED - Server should work!")
    print("=" * 60)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("FAILED!")
    print("=" * 60)
