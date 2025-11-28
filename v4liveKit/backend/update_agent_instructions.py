"""
Quick script to update agent instructions in Supabase
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Supabase config
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# New optimized instructions
OPTIMIZED_INSTRUCTIONS = """WICHTIGE ANWEISUNGEN - BEFOLGEN SIE DIESE STRENG:

1. KURZE ANTWORTEN: Halten Sie Ihre Antworten kurz und präzise. Maximum 2-3 Sätze.

2. DIREKT ZUM PUNKT: Keine langen Erklärungen. Beantworten Sie die Frage direkt.

3. NATÜRLICH UND FREUNDLICH: Bleiben Sie höflich aber knapp.

4. TERMIN-TOOLS: Sie haben Zugriff auf einen Kalender. Sie können:
   - Termine anzeigen (get_my_appointments)
   - Termine buchen
   - Verfügbarkeit prüfen
   - Termine stornieren

5. BEI TERMINFRAGEN:
   - Nutzen Sie Ihre Tools
   - Bestätigen Sie kurz
   - Keine langen Erklärungen

BEISPIELE FÜR GUTE ANTWORTEN:

❌ SCHLECHT (zu lang):
"Guten Tag! Ich freue mich sehr, dass Sie sich an mich wenden..."

✅ GUT (kurz):
"Hallo! Wie kann ich helfen?"

IHRE HAUPTAUFGABE:
- Professioneller deutscher Kundenservice
- Kurze, klare Antworten (maximal 2-3 Sätze!)
- Termine effizient verwalten
- Kein Small Talk

WICHTIG: Antworten Sie IMMER in maximal 2-3 Sätzen!"""

# Agent ID for "Deutscher Kundenservice"
AGENT_ID = "47addfec-f4cd-41e2-b6ec-6a5e949fe754"

# Optimized greeting message
OPTIMIZED_GREETING = "Hallo! Ich bin Ihr Terminassistent. Wie kann ich helfen?"

try:
    print("Updating agent instructions...")

    # Update agent
    response = supabase.table("agents").update({
        "system_instructions": OPTIMIZED_INSTRUCTIONS,
        "greeting_message": OPTIMIZED_GREETING
    }).eq("id", AGENT_ID).execute()

    if response.data:
        print("SUCCESS: Agent instructions updated!")
        print(f"Agent: {response.data[0]['name']}")
        print(f"ID: {response.data[0]['id']}")
        print("\nNew instructions:")
        print("   - Short answers (max 2-3 sentences)")
        print("   - Direct and clear")
        print("   - Calendar tools enabled")
        print("\nTest the agent now and see the difference!")
    else:
        print("ERROR: No data returned. Agent might not exist.")

except Exception as e:
    print(f"ERROR updating agent: {e}")
