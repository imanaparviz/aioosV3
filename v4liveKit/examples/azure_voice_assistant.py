"""
Voice Assistant ba Azure TTS/STT - Arzoon va High Quality!
Azure TTS ~$4 per 1M characters vs ElevenLabs ~$22 per 1M characters
"""
import asyncio
import logging

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
from livekit.agents.pipeline import VoiceAssistant
from livekit.plugins import azure, openai, silero

load_dotenv()
logger = logging.getLogger("azure-voice-assistant")


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful voice assistant powered by Azure Speech. "
            "You provide short and concise responses. "
            "You sound natural and friendly."
        ),
    )

    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant
    participant = await ctx.wait_for_participant()
    logger.info(f"starting Azure voice assistant for {participant.identity}")

    # Azure STT options
    # Supported languages: en-US, ar-SA, de-DE, es-ES, fr-FR, hi-IN, it-IT,
    # ja-JP, ko-KR, pt-BR, ru-RU, zh-CN, zh-HK, zh-TW and many more!
    stt_language = "en-US"  # Change to your language

    # Azure TTS options - Neural Voices (high quality)
    # Popular voices:
    # English: en-US-JennyNeural, en-US-GuyNeural, en-US-AriaNeural
    # Farsi: fa-IR-DilaraNeural, fa-IR-FaridNeural
    # Arabic: ar-SA-ZariyahNeural, ar-SA-HamedNeural
    tts_voice = "en-US-JennyNeural"  # Very natural female voice

    assistant = VoiceAssistant(
        vad=ctx.proc.userdata["vad"],
        stt=azure.STT(
            language=stt_language,
            # Optional: for better accuracy
            # speech_recognition_language=stt_language,
        ),
        llm=openai.LLM(model="gpt-4o-mini"),  # or use Claude with anthropic.LLM()
        tts=azure.TTS(
            voice=tts_voice,
            # Optional settings:
            # speech_synthesis_voice_name=tts_voice,
            # speaking_rate=1.0,  # 0.5 to 2.0 (1.0 is normal)
            # speaking_pitch=1.0,  # 0.5 to 2.0 (1.0 is normal)
        ),
        chat_ctx=initial_ctx,
    )

    assistant.start(ctx.room, participant)

    # Handle text chat messages
    chat = rtc.ChatManager(ctx.room)

    async def answer_from_text(txt: str):
        chat_ctx = assistant.chat_ctx.copy()
        chat_ctx.append(role="user", text=txt)
        stream = assistant.llm.chat(chat_ctx=chat_ctx)
        await assistant.say(stream)

    @chat.on("message_received")
    def on_chat_received(msg: rtc.ChatMessage):
        if msg.message:
            asyncio.create_task(answer_from_text(msg.message))

    await assistant.say("Hello! I'm your Azure-powered voice assistant. How can I help you today?", allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
