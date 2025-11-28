"""
AIOOS Agent Worker - Professional Voice Agent ba Azure/OpenAI/Deepgram
This file spawns voice agents bara LiveKit rooms

Cost Comparison:
- Azure TTS: ~$4 per 1M characters (⭐ BEST VALUE!)
- OpenAI TTS: ~$15 per 1M characters
- ElevenLabs: ~$22 per 1M characters (EXPENSIVE!)

Quality: Azure Neural voices are comparable to ElevenLabs, sometimes better!
"""

import asyncio
import logging
import os
import re
from typing import Optional
from datetime import datetime
import pytz

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import azure, openai, deepgram, silero, google
from supabase import create_client, Client
from agent_tools_v2 import get_appointments, check_availability, book_appointment, cancel_appointment, search_knowledge

load_dotenv()
logger = logging.getLogger("aioos-agent-worker")
logger.setLevel(logging.INFO)

# Import AI summary - optional feature
try:
    from ai_summary import generate_call_summary
    AI_SUMMARY_AVAILABLE = True
    logger.info("✅ AI Summary module loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ AI Summary not available: {e}")
    AI_SUMMARY_AVAILABLE = False
    generate_call_summary = None

# Initialize Supabase client
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL", "")
# Use SERVICE_ROLE key for backend (bypasses RLS policies)
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
logger.info(f"✅ Supabase initialized: {SUPABASE_URL}")


from utils import clean_text_for_speech


def prewarm(proc: JobProcess):
    """Prewarm the worker - load VAD model"""
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("✅ VAD model loaded")


async def entrypoint(ctx: JobContext):
    """
    Main entrypoint bara agent worker
    This creates a voice assistant that connects to LiveKit room
    """

    logger.info(f"📍 Room: {ctx.room.name}")

    # Extract agent_id from job metadata (preferred) or room name (fallback)
    agent_id = None
    
    # Check job metadata first (LiveKit standard)
    if ctx.job and ctx.job.metadata:
        try:
            # Metadata can be JSON or just a string
            import json
            try:
                metadata = json.loads(ctx.job.metadata)
                agent_id = metadata.get("agent_id")
            except json.JSONDecodeError:
                # Maybe it's just the agent_id string?
                agent_id = ctx.job.metadata
                
            if agent_id:
                logger.info(f"🔍 Extracted agent_id from metadata: {agent_id}")
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse job metadata: {e}")

    # Fallback: Extract from room name
    if not agent_id:
        match = re.search(r'test-([a-f0-9-]+)-[\d.]+', ctx.room.name)  # Fixed: Accept decimal timestamp
        if match:
            agent_id = match.group(1)
            logger.info(f"🔍 Extracted agent_id from room name: {agent_id}")

    # Fetch agent settings from database
    agent_settings = None
    if agent_id:
        try:
            response = supabase.table("agents").select("*").eq("id", agent_id).execute()
            if response.data and len(response.data) > 0:
                agent_settings = response.data[0]
                logger.info(f"✅ Loaded agent settings from database: {agent_settings['name']}")
        except Exception as e:
            logger.error(f"❌ Failed to fetch agent settings: {e}")

    # Use agent settings from database, or fall back to environment variables
    if agent_settings:
        agent_name = agent_settings.get("name", "AIOOS Assistant")
        agent_instructions = agent_settings.get("system_instructions",
            "You are a professional voice assistant. Keep your answers concise and friendly.")
        greeting_message = agent_settings.get("greeting_message",
            "Hello! How can I help you today?")
        tts_voice = agent_settings.get("tts_voice", "en-US-JennyNeural")
        tts_provider = agent_settings.get("tts_provider", "azure")
        stt_language = agent_settings.get("language", "en-US")
        stt_provider = agent_settings.get("stt_provider", "azure")
        llm_model = agent_settings.get("llm_model", "gpt-4o-mini")
    else:
        # Fallback to environment variables
        agent_name = os.getenv("AGENT_NAME", "AIOOS Assistant")
        agent_instructions = os.getenv(
            "AGENT_INSTRUCTIONS",
            "You are a professional voice assistant powered by Azure AI. "
            "You provide clear, natural, and helpful responses. "
            "Keep your answers concise and friendly."
        )
        greeting_message = os.getenv(
            "AGENT_GREETING",
            f"Hello! I'm {agent_name}, your AI voice assistant. How can I help you today?"
        )
        tts_voice = os.getenv("TTS_VOICE", "en-US-JennyNeural")
        tts_provider = os.getenv("TTS_PROVIDER", "azure")
        stt_language = os.getenv("STT_LANGUAGE", "en-US")
        stt_provider = os.getenv("STT_PROVIDER", "azure")
        llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    logger.info(f"🚀 Starting {agent_name}")
    logger.info(f"📍 Room: {ctx.room.name}")
    logger.info(f"🎤 STT: {stt_provider} ({stt_language})")
    logger.info(f"🔊 TTS: {tts_provider} ({tts_voice})")
    logger.info(f"🤖 LLM: {llm_model}")

    # Add current date/time to agent instructions (so agent always knows what day/time it is)
    berlin_tz = pytz.timezone('Europe/Berlin')
    now = datetime.now(berlin_tz)

    # German day names mapping
    day_names_de = {
        'Monday': 'Montag',
        'Tuesday': 'Dienstag',
        'Wednesday': 'Mittwoch',
        'Thursday': 'Donnerstag',
        'Friday': 'Freitag',
        'Saturday': 'Samstag',
        'Sunday': 'Sonntag'
    }

    # German month names mapping
    month_names_de = {
        'January': 'Januar', 'February': 'Februar', 'March': 'März',
        'April': 'April', 'May': 'Mai', 'June': 'Juni',
        'July': 'Juli', 'August': 'August', 'September': 'September',
        'October': 'Oktober', 'November': 'November', 'December': 'Dezember'
    }

    day_name = day_names_de.get(now.strftime('%A'), now.strftime('%A'))
    month_name = month_names_de.get(now.strftime('%B'), now.strftime('%B'))

    current_datetime_context = f"""
AKTUELLE ZEIT-INFORMATION (wichtig für Termine!):
Heute ist: {day_name}, {now.day}. {month_name} {now.year}
Aktuelle Uhrzeit: {now.strftime('%H:%M')} Uhr

"""

    # Prepend date/time to agent instructions
    agent_instructions = current_datetime_context + agent_instructions
    logger.info(f"📅 Current date/time injected: {day_name}, {now.day}. {month_name} {now.year} - {now.strftime('%H:%M')} Uhr")

    # Connect to room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait bara first participant
    participant = await ctx.wait_for_participant()
    logger.info(f"👤 Participant joined: {participant.identity}")

    # ==================== Select STT Provider ====================
    if stt_provider == "deepgram":
        # Deepgram STT - Fast and accurate
        stt = deepgram.STT(
            language=stt_language,
            model="nova-2",  # Latest model
        )
        logger.info("✅ Using Deepgram STT (Nova-2 model)")
    else:
        # Azure STT - Default, cheap and reliable
        stt = azure.STT(
            language=stt_language,  # API 1.2.18: Uses singular 'language' parameter
        )
        logger.info(f"✅ Using Azure STT with language: {stt_language}")

    # ==================== Select TTS Provider ====================
    if tts_provider == "openai":
        # OpenAI TTS - Good quality, medium cost
        tts = openai.TTS(
            voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
            model="tts-1",  # or tts-1-hd for higher quality
        )
        logger.info("✅ Using OpenAI TTS")
    else:
        # Azure TTS - Default, BEST VALUE!
        # Neural voices are incredibly natural and cheap
        tts = azure.TTS(
            voice=tts_voice,
            # Optional: Adjust speaking style
            # speaking_rate=1.0,  # 0.5 to 2.0
            # speaking_pitch=1.0,  # 0.5 to 2.0
        )
        logger.info(f"✅ Using Azure TTS with {tts_voice}")

    # ==================== Select LLM Provider ====================
    # Support both OpenAI and Google Gemini models
    if "gemini" in llm_model.lower():
        # Google Gemini (gemini-2.0-flash, gemini-pro, etc.)
        llm_instance = google.LLM(model=llm_model)
        logger.info(f"✅ Using Google Gemini LLM: {llm_model}")
    else:
        # Default: OpenAI (gpt-4o-mini, gpt-4, etc.)
        llm_instance = openai.LLM(model=llm_model)
        logger.info(f"✅ Using OpenAI LLM: {llm_model}")

    # ==================== Create Initial Chat Context ====================
    initial_chat_ctx = llm.ChatContext().append(
        role="system",
        text=agent_instructions
    )

    # ==================== Create Function Context with Tools ====================
    fnc_ctx = llm.FunctionContext()

    # Add calendar and knowledge tools if we have agent_id
    if agent_id:
        try:
            # Calendar tool - use @fnc_ctx.ai_callable() decorator
            @fnc_ctx.ai_callable()
            async def get_my_appointments() -> str:
                """
                Zeigt Ihre aktuellen Termine an.
                Verwenden Sie dies, wenn der Benutzer nach seinen Terminen fragt.
                """
                try:
                    # Note: For VoicePipelineAgent, we can't access context parameter
                    # so we use the agent_id from closure
                    from livekit.agents import RunContext
                    context = RunContext.get_current()
                    return await get_appointments(context, agent_id)
                except Exception as e:
                    logger.error(f"❌ Error in get_my_appointments tool: {e}")
                    return f"Es tut mir leid, ich konnte Ihre Termine nicht abrufen. Fehler: {str(e)}"

            # Knowledge search tool
            @fnc_ctx.ai_callable()
            async def search_my_knowledge(query: str) -> str:
                """
                Durchsucht die Wissensdatenbank nach relevanten Informationen.
                Verwenden Sie dies, wenn der Benutzer eine Frage stellt, die durch hochgeladene Dokumente beantwortet werden kann.
                """
                try:
                    from livekit.agents import RunContext
                    context = RunContext.get_current()
                    return await search_knowledge(context, agent_id, query)
                except Exception as e:
                    logger.error(f"❌ Error in search_my_knowledge tool: {e}")
                    return f"Es tut mir leid, ich konnte die Wissensdatenbank nicht durchsuchen. Fehler: {str(e)}"

            logger.info(f"✅ Created 2 tool(s) for agent {agent_id}")
        except Exception as e:
            logger.error(f"❌ Failed to create tools: {e}")

    logger.info(f"✅ Function context created")

    # ==================== Call Logging ====================
    call_log_id = None
    start_time = datetime.utcnow()

    # ==================== Create Voice Pipeline Agent ====================
    assistant = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=stt,
        llm=llm_instance,
        tts=tts,
        chat_ctx=initial_chat_ctx,
        fnc_ctx=fnc_ctx if agent_id else None,
    )
    logger.info(f"✅ Voice Pipeline Agent created")

    # ==================== Transcript Collection ====================
    # Collect transcript messages in real-time using event listeners
    transcript_messages = []

    @assistant.on("user_speech_committed")
    def on_user_speech_committed(msg: llm.ChatMessage):
        """Capture user messages as they're committed"""
        content = msg.content
        if isinstance(content, list):
            # Handle list of content (images + text)
            content = "\n".join(
                "[image]" if isinstance(x, llm.ChatImage) else str(x) for x in content
            )

        transcript_messages.append({
            "role": "user",
            "text": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"📝 User message captured: {content[:50]}...")

    @assistant.on("agent_speech_committed")
    def on_agent_speech_committed(msg: llm.ChatMessage):
        """Capture agent messages as they're committed"""
        content = msg.content
        if isinstance(content, list):
            content = "\n".join(str(x) for x in content)

        transcript_messages.append({
            "role": "assistant",
            "text": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"📝 Agent message captured: {content[:50]}...")

    logger.info("✅ Transcript event listeners attached")

    if agent_id:
        try:
            # Create initial call log
            log_data = {
                "agent_id": agent_id,
                "room_name": ctx.room.name,
                "start_time": start_time.isoformat(),
                "status": "ongoing",
                # "user_id": user_id  # TODO: Pass user_id from main.py
            }

            # If we have the user_id from the agent settings (fetched above), use it
            if agent_settings and "user_id" in agent_settings:
                log_data["user_id"] = agent_settings["user_id"]

            response = supabase.table("call_logs").insert(log_data).execute()
            if response.data and len(response.data) > 0:
                call_log_id = response.data[0]['id']
                logger.info(f"✅ Call log created: {call_log_id}")
        except Exception as e:
            logger.error(f"❌ Failed to create call log: {e}")

    try:
        # Start the voice assistant
        assistant.start(ctx.room)
        logger.info("✅ Voice Assistant started!")

        # ==================== Greeting Message ====================
        # Send greeting message
        await assistant.say(greeting_message, allow_interruptions=True)
        logger.info(f"💬 Greeting sent: {greeting_message}")

        logger.info("✅ Agent fully initialized and ready!")
        
    except Exception as e:
        logger.error(f"❌ Error in agent session: {e}")
    finally:
        # Update call log on exit
        if call_log_id:
            try:
                end_time = datetime.utcnow()
                duration = (end_time - start_time).total_seconds()

                # Calculate estimated cost (very rough estimate)
                # Azure TTS: $4/1M chars. Assume 10 chars/sec avg speech?
                # STT: $1/hour (Deepgram) or similar.
                # Let's estimate $0.10 per hour for now as a placeholder
                cost = (duration / 3600) * 0.10

                update_data = {
                    "end_time": end_time.isoformat(),
                    "duration_seconds": int(duration),
                    "status": "completed",
                    "cost": round(cost, 4)
                }

                # ==================== Save Transcript ====================
                # Use the messages collected by event listeners during the session
                try:
                    logger.info(f"📊 Collected {len(transcript_messages)} transcript messages")

                    if transcript_messages:
                        # Build transcript as text
                        transcript_lines = []

                        for msg in transcript_messages:
                            role = msg.get("role", "unknown")
                            text = msg.get("text", "")

                            # Format for text transcript
                            transcript_lines.append(f"{role.upper()}: {text}")

                        # Add to update data
                        update_data["transcript"] = "\n".join(transcript_lines)
                        update_data["transcript_json"] = transcript_messages

                        logger.info(f"✅ Transcript saved: {len(transcript_messages)} messages")

                        # ==================== AI Summary (On-Demand Only) ====================
                        # Summary is NOT generated automatically anymore.
                        # User can request summary via "Generate AI Summary" button in UI
                        # which calls POST /api/calls/{call_id}/generate-summary
                        logger.info("ℹ️ AI Summary disabled for automatic generation - user can request via UI")

                    else:
                        logger.info("ℹ️ No transcript messages collected during session")

                except Exception as e:
                    logger.error(f"❌ Failed to save transcript: {e}")
                    import traceback
                    logger.error(f"❌ Traceback: {traceback.format_exc()}")
                    # Don't fail the whole update if transcript fails

                # Update database with all data (metadata + transcript + summary)
                supabase.table("call_logs").update(update_data).eq("id", call_log_id).execute()
                logger.info(f"✅ Call log updated: {call_log_id} (Duration: {int(duration)}s)")
            except Exception as e:
                logger.error(f"❌ Failed to update call log: {e}")


# ==================== Azure Voice Options ====================
"""
Top Azure Neural Voices (High Quality, Natural):

ENGLISH:
- en-US-JennyNeural (Female, friendly, warm) ⭐ RECOMMENDED
- en-US-GuyNeural (Male, professional, clear)
- en-US-AriaNeural (Female, natural, conversational)
- en-US-DavisNeural (Male, calm, mature)
- en-US-JaneNeural (Female, energetic, young)
- en-GB-SoniaNeural (British Female, elegant)
- en-GB-RyanNeural (British Male, professional)

FARSI (Persian):
- fa-IR-DilaraNeural (Female, natural)
- fa-IR-FaridNeural (Male, clear)

ARABIC:
- ar-SA-ZariyahNeural (Female, natural)
- ar-SA-HamedNeural (Male, clear)

GERMAN (Deutsch): ⭐
- de-DE-KatjaNeural (Female, friendly, warm) ⭐ RECOMMENDED
- de-DE-ConradNeural (Male, professional, clear)
- de-DE-AmalaNeural (Female, young, energetic)
- de-DE-KillianNeural (Male, calm, mature)
- de-AT-IngridNeural (Austrian Female, natural)
- de-AT-JonasNeural (Austrian Male, professional)
- de-CH-LeniNeural (Swiss Female, clear)
- de-CH-JanNeural (Swiss Male, friendly)

SPANISH:
- es-ES-ElviraNeural (Female, warm)
- es-MX-DaliaNeural (Mexican Female, friendly)

Full list: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support
"""


# ==================== Run Worker ====================
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🎙️  AIOOS Voice Agent Worker")
    logger.info("=" * 60)
    logger.info("💰 Using Azure TTS - 5x cheaper than ElevenLabs!")
    logger.info("🎯 Quality: Comparable or better than ElevenLabs")
    logger.info("=" * 60)

    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm
        )
    )
