"""
AI Summary Generation - Generate call summaries using GPT-4o-mini
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from openai import AsyncOpenAI

logger = logging.getLogger("aioos-ai-summary")

# OpenAI client - initialized on demand
_client = None

def get_openai_client():
    """Get or create OpenAI client"""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. AI summary feature requires OpenAI API key.")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def generate_call_summary(
    transcript_messages: List[Dict[str, Any]],
    language: str = "de"
) -> Dict[str, Any]:
    """
    Generate AI summary from call transcript

    Args:
        transcript_messages: List of {role, text, timestamp} messages
        language: Language code (de, en, etc.)

    Returns:
        {
            "summary": str,  # Main summary text
            "key_points": List[str],  # Key discussion points
            "sentiment": str,  # overall, positive, negative, neutral
            "action_items": List[str],  # Action items identified
            "topics": List[str],  # Main topics discussed
            "duration_analysis": str  # Analysis of call efficiency
        }
    """

    if not transcript_messages or len(transcript_messages) == 0:
        return {
            "summary": "No transcript available",
            "key_points": [],
            "sentiment": "neutral",
            "action_items": [],
            "topics": [],
            "duration_analysis": "Call too short to analyze"
        }

    # Build transcript text
    transcript_text = "\n".join([
        f"{msg.get('role', 'unknown').upper()}: {msg.get('text', '')}"
        for msg in transcript_messages
    ])

    # System prompt based on language
    system_prompts = {
        "de": """Du bist ein professioneller Call-Analyse-Assistent.
Analysiere das folgende Telefonat und erstelle eine strukturierte Zusammenfassung auf Deutsch.

Gib deine Antwort als JSON zurück mit folgenden Feldern:
- summary: Eine prägnante Zusammenfassung (2-3 Sätze)
- key_points: Liste der wichtigsten besprochenen Punkte
- sentiment: Gesamtstimmung (positive, negative, neutral)
- action_items: Liste identifizierter Handlungsschritte
- topics: Liste der Hauptthemen
- duration_analysis: Einschätzung der Gesprächseffizienz""",

        "en": """You are a professional call analysis assistant.
Analyze the following call transcript and create a structured summary in English.

Return your answer as JSON with these fields:
- summary: A concise summary (2-3 sentences)
- key_points: List of main discussion points
- sentiment: Overall sentiment (positive, negative, neutral)
- action_items: List of identified action items
- topics: List of main topics
- duration_analysis: Assessment of call efficiency"""
    }

    system_prompt = system_prompts.get(language, system_prompts["en"])

    try:
        # Get OpenAI client
        client = get_openai_client()

        # Call GPT-4o-mini for analysis
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transcript:\n\n{transcript_text}"}
            ],
            temperature=0.3,  # Low temperature for consistent analysis
            response_format={"type": "json_object"}
        )

        # Parse JSON response
        summary_data = json.loads(response.choices[0].message.content)

        logger.info(f"✅ AI Summary generated: {len(summary_data.get('summary', ''))} chars")

        return summary_data

    except Exception as e:
        logger.error(f"❌ Failed to generate AI summary: {e}")

        # Fallback: basic summary
        user_messages = [m for m in transcript_messages if m.get('role') == 'user']
        agent_messages = [m for m in transcript_messages if m.get('role') == 'assistant']

        return {
            "summary": f"Gespräch mit {len(user_messages)} Benutzer-Nachrichten und {len(agent_messages)} Agent-Antworten.",
            "key_points": ["Automatische Analyse fehlgeschlagen"],
            "sentiment": "neutral",
            "action_items": [],
            "topics": [],
            "duration_analysis": "Analyse nicht verfügbar",
            "error": str(e)
        }


async def generate_sentiment_analysis(text: str) -> str:
    """
    Quick sentiment analysis for a single message

    Returns: positive, negative, or neutral
    """
    try:
        client = get_openai_client()
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze sentiment. Reply with only one word: positive, negative, or neutral"
                },
                {"role": "user", "content": text}
            ],
            temperature=0.1,
            max_tokens=10
        )

        sentiment = response.choices[0].message.content.strip().lower()

        if sentiment in ["positive", "negative", "neutral"]:
            return sentiment

        return "neutral"

    except Exception as e:
        logger.error(f"❌ Sentiment analysis failed: {e}")
        return "neutral"
