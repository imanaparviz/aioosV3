"""
Test Knowledge Search - Direct API call to debug RAG
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Test query
QUERY = "Was ist Iman sein Lieblingsbuch?"
AGENT_ID = "823dfd3b-af97-46a0-beb1-5e14a4ec0137"

print("=" * 60)
print("Testing Knowledge Search API")
print("=" * 60)
print(f"Query: {QUERY}")
print(f"Agent ID: {AGENT_ID}")
print()

# Test 1: Call search API
print("Step 1: Calling /api/knowledge/search endpoint...")
try:
    response = requests.post(
        "http://localhost:8000/api/knowledge/search",
        data={
            "agent_id": AGENT_ID,
            "query": QUERY,
            "limit": 5
        },
        timeout=15
    )

    print(f"Status Code: {response.status_code}")
    print()

    if response.status_code == 200:
        result = response.json()
        print(f"[OK] Response JSON:")
        print(f"   Status: {result.get('status')}")
        print(f"   Count: {result.get('count')}")
        print(f"   Results: {len(result.get('results', []))}")
        print()

        if result.get('results'):
            print("Search Results:")
            for idx, item in enumerate(result['results'], 1):
                print(f"\n   Result {idx}:")
                print(f"   - Content: {item.get('content', '')[:200]}...")
                print(f"   - File: {item.get('file_name', 'Unknown')}")
                print(f"   - Similarity: {item.get('similarity', 0):.3f}")
        else:
            print("[ERROR] No results returned!")
            print("   This means:")
            print("   1. No chunks matched the similarity threshold (0.5)")
            print("   2. OR search_knowledge_base function returned empty")
    else:
        print(f"[ERROR] Error Response:")
        print(response.text)

except Exception as e:
    print(f"[ERROR] Request failed: {e}")

print()
print("=" * 60)

# Test 2: Direct database query to verify chunks exist
print("Step 2: Checking database for chunks...")
print()

from supabase import create_client

SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    # Get all chunks for this agent
    response = supabase.table("document_chunks") \
        .select("id, content, metadata") \
        .eq("agent_id", AGENT_ID) \
        .execute()

    if response.data:
        print(f"[OK] Found {len(response.data)} chunks in database:")
        for idx, chunk in enumerate(response.data, 1):
            print(f"\n   Chunk {idx}:")
            print(f"   - Content: {chunk['content'][:200]}...")
            print(f"   - Metadata: {chunk.get('metadata')}")
    else:
        print("[ERROR] No chunks found in database!")

except Exception as e:
    print(f"[ERROR] Database query failed: {e}")

print()
print("=" * 60)
print("[OK] Test complete!")
print("=" * 60)
