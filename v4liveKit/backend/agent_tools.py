"""
AIOOS Platform - Agent Tools
Custom tools for LiveKit voice agents
"""

import os
import logging
import requests
import json
from datetime import datetime, timedelta, time, date
from typing import Optional, List
from livekit.agents import llm

logger = logging.getLogger("aioos-agent-tools")

# Backend API URL
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


# ==================== Appointment Booking Tool ====================

class BookAppointmentTool(llm.FunctionTool):
    """
    Tool for booking appointments via voice conversation

    This tool allows the agent to book appointments when users request them.
    Example user requests:
    - "Book me an appointment tomorrow at 2pm"
    - "I need to schedule a meeting for Friday at 10am"
    - "Can you reserve a time slot for me between 3-4pm on Monday?"
    """

    def __init__(self, agent_id: str):
        super().__init__(
            name="book_appointment",
            description=(
                "Books an appointment for the user. Use this when the user wants to "
                "schedule, book, or reserve an appointment or meeting. "
                "You must collect: participant name, date, and time before booking. "
                "Ask clarifying questions if information is missing."
            ),
            parameters=[
                llm.FunctionParameter(
                    name="participant_name",
                    type="string",
                    description="The name of the person booking the appointment",
                    required=True
                ),
                llm.FunctionParameter(
                    name="date",
                    type="string",
                    description="The date of the appointment in YYYY-MM-DD format",
                    required=True
                ),
                llm.FunctionParameter(
                    name="time",
                    type="string",
                    description="The start time of the appointment in HH:MM format (24-hour)",
                    required=True
                ),
                llm.FunctionParameter(
                    name="duration_minutes",
                    type="integer",
                    description="Duration of the appointment in minutes (default: 30)",
                    required=False
                ),
                llm.FunctionParameter(
                    name="description",
                    type="string",
                    description="Optional description or notes about the appointment",
                    required=False
                ),
                llm.FunctionParameter(
                    name="phone",
                    type="string",
                    description="Optional phone number of the participant",
                    required=False
                ),
                llm.FunctionParameter(
                    name="email",
                    type="string",
                    description="Optional email address of the participant",
                    required=False
                ),
            ]
        )
        self.agent_id = agent_id

    async def run(
        self,
        participant_name: str,
        date: str,
        time: str,
        duration_minutes: int = 30,
        description: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> str:
        """
        Execute the appointment booking
        Returns a human-readable message about the booking status
        """
        try:
            # Validate and parse date
            try:
                appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return f"Invalid date format '{date}'. Please provide date in YYYY-MM-DD format (e.g., 2025-01-15)."

            # Validate and parse time
            try:
                appointment_time = datetime.strptime(time, "%H:%M").time()
            except ValueError:
                return f"Invalid time format '{time}'. Please provide time in HH:MM format (e.g., 14:30)."

            # Check if date is in the past
            if appointment_date < datetime.now().date():
                return "Cannot book appointments in the past. Please choose a future date."

            # Check if it's too far in the future (90 days default)
            if appointment_date > datetime.now().date() + timedelta(days=90):
                return "Cannot book appointments more than 90 days in advance. Please choose a closer date."

            # Prepare booking request
            booking_data = {
                "agent_id": self.agent_id,
                "participant_name": participant_name,
                "date": date,
                "start_time": time,
                "duration_minutes": duration_minutes,
                "description": description,
                "participant_phone": phone,
                "participant_email": email
            }

            logger.info(f"📅 Attempting to book appointment: {json.dumps(booking_data, indent=2)}")

            # Call backend API to book appointment
            response = requests.post(
                f"{BACKEND_API_URL}/api/calendar/book",
                json=booking_data,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                event = result.get("event", {})

                # Format success message
                formatted_date = appointment_date.strftime("%A, %B %d, %Y")
                formatted_time = appointment_time.strftime("%I:%M %p")

                success_message = (
                    f"Perfect! I've successfully booked your appointment for "
                    f"{formatted_date} at {formatted_time}. "
                    f"The appointment will last {duration_minutes} minutes."
                )

                if description:
                    success_message += f" Purpose: {description}."

                logger.info(f"✅ Appointment booked successfully: {event.get('id')}")
                return success_message

            elif response.status_code == 409:
                # Time slot not available
                error_detail = response.json().get("detail", "Time slot is not available")
                logger.warning(f"⚠️  Booking conflict: {error_detail}")

                return (
                    f"I'm sorry, but that time slot is not available. "
                    f"Would you like me to suggest some alternative times?"
                )

            else:
                # Other error
                error_detail = response.json().get("detail", "Unknown error")
                logger.error(f"❌ Booking failed: {error_detail}")

                return (
                    f"I encountered an error while trying to book your appointment. "
                    f"Please try again or contact support if the problem persists."
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error during booking: {e}")
            return (
                "I'm having trouble connecting to the booking system. "
                "Please try again in a moment."
            )

        except Exception as e:
            logger.error(f"❌ Unexpected error during booking: {e}")
            return (
                "An unexpected error occurred. Please try again or contact support."
            )


# ==================== Check Available Slots Tool ====================

class CheckAvailabilityTool(llm.FunctionTool):
    """
    Tool for checking available appointment slots

    This tool allows the agent to check what time slots are available
    on a specific date before booking.
    """

    def __init__(self, agent_id: str):
        super().__init__(
            name="check_availability",
            description=(
                "Checks available appointment time slots for a specific date. "
                "Use this when the user asks about availability or wants to see "
                "what times are free on a particular day."
            ),
            parameters=[
                llm.FunctionParameter(
                    name="date",
                    type="string",
                    description="The date to check availability for in YYYY-MM-DD format",
                    required=True
                ),
                llm.FunctionParameter(
                    name="duration_minutes",
                    type="integer",
                    description="Desired appointment duration in minutes (default: 30)",
                    required=False
                ),
            ]
        )
        self.agent_id = agent_id

    async def run(self, date: str, duration_minutes: int = 30) -> str:
        """
        Check available slots for a date
        Returns a human-readable message with available times
        """
        try:
            # Validate date
            try:
                check_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return f"Invalid date format '{date}'. Please provide date in YYYY-MM-DD format."

            # Call backend API
            response = requests.post(
                f"{BACKEND_API_URL}/api/calendar/available-slots",
                json={
                    "agent_id": self.agent_id,
                    "date": date,
                    "duration_minutes": duration_minutes
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                slots = result.get("slots", [])

                if not slots:
                    formatted_date = check_date.strftime("%A, %B %d, %Y")
                    return f"I don't have any available time slots on {formatted_date}. Would you like to try a different day?"

                # Filter only available slots
                available_slots = [slot for slot in slots if slot.get("is_available")]

                if not available_slots:
                    formatted_date = check_date.strftime("%A, %B %d, %Y")
                    return f"All time slots are booked on {formatted_date}. Would you like to try a different day?"

                # Format available times
                formatted_date = check_date.strftime("%A, %B %d, %Y")
                times_list = []

                for slot in available_slots[:10]:  # Show max 10 slots
                    slot_time = datetime.strptime(slot["start_time"], "%H:%M:%S").time()
                    formatted_time = slot_time.strftime("%I:%M %p")
                    times_list.append(formatted_time)

                times_str = ", ".join(times_list)

                message = f"I have the following time slots available on {formatted_date}: {times_str}. "
                message += "Which time works best for you?"

                logger.info(f"✅ Found {len(available_slots)} available slots for {date}")
                return message

            else:
                error_detail = response.json().get("detail", "Unknown error")
                logger.error(f"❌ Failed to check availability: {error_detail}")
                return "I'm having trouble checking availability. Please try again."

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Network error checking availability: {e}")
            return "I'm having trouble connecting to the scheduling system. Please try again."

        except Exception as e:
            logger.error(f"❌ Unexpected error checking availability: {e}")
            return "An unexpected error occurred. Please try again."


# ==================== Cancel Appointment Tool ====================

class CancelAppointmentTool(llm.FunctionTool):
    """
    Tool for canceling appointments
    """

    def __init__(self, agent_id: str):
        super().__init__(
            name="cancel_appointment",
            description=(
                "Cancels an existing appointment. Use this when the user wants to "
                "cancel or remove a scheduled appointment. You need to know the "
                "date and time of the appointment to cancel."
            ),
            parameters=[
                llm.FunctionParameter(
                    name="date",
                    type="string",
                    description="The date of the appointment to cancel in YYYY-MM-DD format",
                    required=True
                ),
                llm.FunctionParameter(
                    name="time",
                    type="string",
                    description="The start time of the appointment in HH:MM format",
                    required=True
                ),
            ]
        )
        self.agent_id = agent_id

    async def run(self, date: str, time: str) -> str:
        """
        Cancel an appointment
        """
        try:
            # Find the appointment
            response = requests.get(
                f"{BACKEND_API_URL}/api/calendar/events",
                params={
                    "agent_id": self.agent_id,
                    "start_date": date,
                    "end_date": date
                },
                timeout=10
            )

            if response.status_code != 200:
                return "I'm having trouble accessing the appointment system. Please try again."

            events = response.json()

            # Find matching appointment
            target_event = None
            for event in events:
                if event["event_time"].startswith(time):
                    target_event = event
                    break

            if not target_event:
                return f"I couldn't find an appointment on {date} at {time}. Please double-check the date and time."

            # Cancel the appointment (update status to cancelled)
            response = requests.put(
                f"{BACKEND_API_URL}/api/calendar/events/{target_event['id']}",
                json={"status": "cancelled"},
                timeout=10
            )

            if response.status_code == 200:
                formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%A, %B %d, %Y")
                formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")

                logger.info(f"✅ Cancelled appointment: {target_event['id']}")
                return f"I've successfully cancelled your appointment on {formatted_date} at {formatted_time}."
            else:
                return "I encountered an error while cancelling the appointment. Please try again."

        except Exception as e:
            logger.error(f"❌ Error cancelling appointment: {e}")
            return "An unexpected error occurred while cancelling. Please try again."


# ==================== Helper: Get All Tools ====================

def get_agent_tools(agent_id: str) -> List[llm.FunctionTool]:
    """
    Get all available tools for an agent
    Call this from agent_worker.py to register tools
    """
    return [
        BookAppointmentTool(agent_id),
        CheckAvailabilityTool(agent_id),
        CancelAppointmentTool(agent_id),
    ]
