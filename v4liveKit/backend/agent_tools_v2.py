"""
AIOOS Platform - Agent Tools v2 (API 1.2.18)
Custom tools for LiveKit voice agents using new @function_tool decorator
"""

import os
import logging
import requests
import json
from datetime import datetime, timedelta
from typing import Optional
from livekit.agents import function_tool, RunContext

logger = logging.getLogger("aioos-agent-tools-v2")

# Backend API URL
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


# ==================== Get Appointments Tool ====================

@function_tool()
async def get_appointments(
    context: RunContext,
    agent_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> str:
    """
    Get list of appointments for an agent.
    Use this when the user asks about their schedule, appointments, or termins.

    Args:
        agent_id: The ID of the agent to fetch appointments for
        start_date: Optional start date in YYYY-MM-DD format (defaults to today)
        end_date: Optional end date in YYYY-MM-DD format (defaults to 7 days from start)

    Returns:
        A human-readable message with the list of appointments
    """
    try:
        # Default dates if not provided
        if not start_date:
            start_date = datetime.now().date().isoformat()
        if not end_date:
            end_date = (datetime.now().date() + timedelta(days=7)).isoformat()

        logger.info(f"📅 Fetching appointments for agent {agent_id} from {start_date} to {end_date}")

        # Call backend API
        response = requests.get(
            f"{BACKEND_API_URL}/api/calendar/events",
            params={
                "agent_id": agent_id,
                "start_date": start_date,
                "end_date": end_date
            },
            timeout=10
        )

        if response.status_code == 200:
            events = response.json()

            if not events:
                return "Sie haben keine Termine in diesem Zeitraum."  # You have no appointments in this period

            # Filter only pending and confirmed appointments
            active_events = [e for e in events if e.get("status") in ["pending", "confirmed"]]

            if not active_events:
                return "Sie haben keine aktiven Termine in diesem Zeitraum."

            # Format appointments message
            message = f"Sie haben {len(active_events)} Termine:\n\n"

            for idx, event in enumerate(active_events[:10], 1):  # Max 10
                event_date = datetime.fromisoformat(event["event_date"]).strftime("%A, %d. %B %Y")
                event_time = event["event_time"][:5]  # HH:MM
                title = event.get("title", "Termin")
                participant = event.get("participant_name", "")
                duration = event.get("duration_minutes", 30)

                message += f"{idx}. {event_date} um {event_time} Uhr - {title}"
                if participant:
                    message += f" mit {participant}"
                message += f" ({duration} Minuten)\n"

            logger.info(f"✅ Returned {len(active_events)} appointments")
            return message

        else:
            error_detail = response.json().get("detail", "Unknown error")
            logger.error(f"❌ Failed to fetch appointments: {error_detail}")
            return "Ich konnte Ihre Termine leider nicht abrufen. Bitte versuchen Sie es später erneut."

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error fetching appointments: {e}")
        return "Ich habe Probleme, auf den Kalender zuzugreifen. Bitte versuchen Sie es in einem Moment erneut."

    except Exception as e:
        logger.error(f"❌ Unexpected error fetching appointments: {e}")
        return "Ein unerwarteter Fehler ist aufgetreten."


# ==================== Check Available Slots Tool ====================

@function_tool()
async def check_availability(
    context: RunContext,
    agent_id: str,
    date: str,
    duration_minutes: int = 30
) -> str:
    """
    Check available appointment time slots for a specific date.
    Use this when the user asks about availability or wants to see what times are free.

    Args:
        agent_id: The ID of the agent
        date: The date to check in YYYY-MM-DD format
        duration_minutes: Duration needed in minutes (default 30)

    Returns:
        A human-readable message with available time slots
    """
    try:
        # Validate date
        try:
            check_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return f"Ungültiges Datumsformat '{date}'. Bitte verwenden Sie YYYY-MM-DD."

        logger.info(f"🕐 Checking availability for {agent_id} on {date}")

        # Call backend API
        response = requests.post(
            f"{BACKEND_API_URL}/api/calendar/available-slots",
            json={
                "agent_id": agent_id,
                "date": date,
                "duration_minutes": duration_minutes
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            slots = result.get("slots", [])

            if not slots:
                formatted_date = check_date.strftime("%A, %d. %B %Y")
                return f"Ich habe leider keine verfügbaren Zeiten am {formatted_date}. Möchten Sie einen anderen Tag probieren?"

            # Filter available slots
            available_slots = [slot for slot in slots if slot.get("is_available")]

            if not available_slots:
                formatted_date = check_date.strftime("%A, %d. %B %Y")
                return f"Alle Zeiten sind am {formatted_date} belegt. Möchten Sie einen anderen Tag probieren?"

            # Format available times
            formatted_date = check_date.strftime("%A, %d. %B %Y")
            times_list = []

            for slot in available_slots[:10]:  # Max 10 slots
                slot_time = datetime.strptime(slot["start_time"], "%H:%M:%S").time()
                formatted_time = slot_time.strftime("%H:%M")
                times_list.append(formatted_time)

            times_str = ", ".join(times_list)
            message = f"Am {formatted_date} habe ich folgende Zeiten frei: {times_str} Uhr. Welche Zeit passt Ihnen am besten?"

            logger.info(f"✅ Found {len(available_slots)} available slots")
            return message

        else:
            error_detail = response.json().get("detail", "Unknown error")
            logger.error(f"❌ Failed to check availability: {error_detail}")
            return "Ich konnte die Verfügbarkeit leider nicht prüfen. Bitte versuchen Sie es später erneut."

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error checking availability: {e}")
        return "Ich habe Probleme mit der Verbindung zum Buchungssystem."

    except Exception as e:
        logger.error(f"❌ Unexpected error checking availability: {e}")
        return "Ein unerwarteter Fehler ist aufgetreten."


# ==================== Book Appointment Tool ====================

@function_tool()
async def book_appointment(
    context: RunContext,
    agent_id: str,
    participant_name: str,
    date: str,
    time: str,
    duration_minutes: int = 30,
    description: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None
) -> str:
    """
    Book an appointment for the user.
    Use this when the user wants to schedule, book, or reserve an appointment or meeting.

    Args:
        agent_id: The ID of the agent
        participant_name: The name of the person booking
        date: The appointment date in YYYY-MM-DD format
        time: The start time in HH:MM format (24-hour)
        duration_minutes: Duration in minutes (default 30)
        description: Optional description
        phone: Optional phone number
        email: Optional email address

    Returns:
        A human-readable confirmation or error message
    """
    try:
        # Validate date
        try:
            appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return f"Ungültiges Datumsformat '{date}'. Bitte verwenden Sie YYYY-MM-DD."

        # Validate time
        try:
            appointment_time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return f"Ungültiges Zeitformat '{time}'. Bitte verwenden Sie HH:MM."

        # Check if date is in past
        if appointment_date < datetime.now().date():
            return "Ich kann keine Termine in der Vergangenheit buchen. Bitte wählen Sie ein zukünftiges Datum."

        # Prepare booking data
        booking_data = {
            "agent_id": agent_id,
            "participant_name": participant_name,
            "date": date,
            "start_time": time,
            "duration_minutes": duration_minutes,
            "description": description,
            "participant_phone": phone,
            "participant_email": email
        }

        logger.info(f"📅 Booking appointment: {json.dumps(booking_data, indent=2)}")

        # Call backend API
        response = requests.post(
            f"{BACKEND_API_URL}/api/calendar/book",
            json=booking_data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            # Format success message in German
            formatted_date = appointment_date.strftime("%A, %d. %B %Y")
            formatted_time = appointment_time.strftime("%H:%M")

            message = (
                f"Perfekt! Ich habe Ihren Termin erfolgreich gebucht für "
                f"{formatted_date} um {formatted_time} Uhr. "
                f"Der Termin dauert {duration_minutes} Minuten."
            )

            if description:
                message += f" Zweck: {description}."

            logger.info(f"✅ Appointment booked successfully")
            return message

        elif response.status_code == 409:
            # Time slot not available
            error_detail = response.json().get("detail", "")
            logger.warning(f"⚠️ Booking conflict: {error_detail}")

            return (
                f"Es tut mir leid, aber diese Zeit ist nicht verfügbar. "
                f"Möchten Sie, dass ich Ihnen alternative Zeiten vorschlage?"
            )

        else:
            error_detail = response.json().get("detail", "Unknown error")
            logger.error(f"❌ Booking failed: {error_detail}")

            return (
                f"Beim Buchen des Termins ist ein Fehler aufgetreten. "
                f"Bitte versuchen Sie es erneut."
            )

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error during booking: {e}")
        return "Ich habe Probleme mit der Verbindung zum Buchungssystem."

    except Exception as e:
        logger.error(f"❌ Unexpected error during booking: {e}")
        return "Ein unerwarteter Fehler ist aufgetreten."


# ==================== Cancel Appointment Tool ====================

@function_tool()
async def cancel_appointment(
    context: RunContext,
    agent_id: str,
    date: str,
    time: str
) -> str:
    """
    Cancel an existing appointment.
    Use this when the user wants to cancel or remove a scheduled appointment.

    Args:
        agent_id: The ID of the agent
        date: The date of the appointment in YYYY-MM-DD format
        time: The start time in HH:MM format

    Returns:
        A human-readable confirmation or error message
    """
    try:
        # Find the appointment
        response = requests.get(
            f"{BACKEND_API_URL}/api/calendar/events",
            params={
                "agent_id": agent_id,
                "start_date": date,
                "end_date": date
            },
            timeout=10
        )

        if response.status_code != 200:
            return "Ich kann leider nicht auf den Kalender zugreifen. Bitte versuchen Sie es später erneut."

        events = response.json()

        # Find matching appointment
        target_event = None
        for event in events:
            if event["event_time"].startswith(time):
                target_event = event
                break

        if not target_event:
            return f"Ich konnte keinen Termin am {date} um {time} Uhr finden. Bitte überprüfen Sie Datum und Uhrzeit."

        # Cancel the appointment
        response = requests.put(
            f"{BACKEND_API_URL}/api/calendar/events/{target_event['id']}",
            json={"status": "cancelled"},
            timeout=10
        )

        if response.status_code == 200:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %d. %B %Y")
            formatted_time = datetime.strptime(time, "%H:%M").strftime("%H:%M")

            logger.info(f"✅ Cancelled appointment: {target_event['id']}")
            return f"Ich habe Ihren Termin am {formatted_date} um {formatted_time} Uhr erfolgreich storniert."
        else:
            return "Beim Stornieren des Termins ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut."

    except Exception as e:
        logger.error(f"❌ Error cancelling appointment: {e}")
        return "Ein unerwarteter Fehler ist beim Stornieren aufgetreten."


# ==================== Search Knowledge Base Tool ====================

@function_tool()
async def search_knowledge(
    context: RunContext,
    agent_id: str,
    query: str,
    limit: int = 5
) -> str:
    """
    Durchsucht die Wissensdatenbank des Agenten nach relevanten Informationen.
    WICHTIG: Verwenden Sie dieses Tool IMMER wenn der Benutzer eine Frage stellt!
    Die Wissensdatenbank enthält hochgeladene Dokumente mit wichtigen Informationen.

    Args:
        agent_id: Die ID des Agenten
        query: Die Suchanfrage oder Frage des Benutzers
        limit: Maximale Anzahl der Ergebnisse (Standard: 5)

    Returns:
        Relevante Informationen aus der Wissensdatenbank oder eine Meldung falls nichts gefunden wurde
    """
    try:
        logger.info(f"🔍 Searching knowledge base for: {query}")

        # Call backend API
        response = requests.post(
            f"{BACKEND_API_URL}/api/knowledge/search",
            data={
                "agent_id": agent_id,
                "query": query,
                "limit": limit
            },
            timeout=15
        )

        if response.status_code == 200:
            result = response.json()
            search_results = result.get("results", [])

            if not search_results or len(search_results) == 0:
                return "KEINE ERGEBNISSE: Ich konnte keine relevanten Informationen in meiner Wissensdatenbank finden zu dieser Frage."

            # Format results - simple and clear, no source attribution
            message = f"WISSENSDATENBANK ERGEBNISSE ({len(search_results)} gefunden):\n\n"

            for idx, item in enumerate(search_results, 1):
                content = item.get("content", "").strip()
                similarity = item.get("similarity", 0)

                # Add just the content, no file name
                message += f"{content}\n\n"

            message += "WICHTIG: Nutze diese Informationen für deine Antwort. Erwähne NICHT woher die Information kommt."

            logger.info(f"✅ Found {len(search_results)} relevant results")
            return message

        else:
            error_detail = response.json().get("detail", "Unknown error")
            logger.error(f"❌ Knowledge search failed: {error_detail}")
            return "Ich konnte die Wissensdatenbank leider nicht durchsuchen."

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error during knowledge search: {e}")
        return "Ich habe Probleme mit der Verbindung zur Wissensdatenbank."

    except Exception as e:
        logger.error(f"❌ Unexpected error during knowledge search: {e}")
        return "Ein unerwarteter Fehler ist aufgetreten."


# ==================== Helper: Get All Tools ====================

def get_all_tools():
    """
    Get all tools as a list
    Use this to register tools with an Agent
    """
    return [
        get_appointments,
        check_availability,
        book_appointment,
        cancel_appointment,
        search_knowledge,
    ]
