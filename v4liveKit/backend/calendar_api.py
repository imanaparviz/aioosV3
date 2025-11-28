"""
AIOOS Platform - Calendar & Appointment API Endpoints
FastAPI endpoints for calendar management and appointment booking
"""

import logging
from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict
from pydantic import BaseModel, Field, validator
from fastapi import HTTPException

logger = logging.getLogger("aioos-calendar-api")


# ==================== Pydantic Models ====================

class CalendarEventCreate(BaseModel):
    """Model for creating a calendar event"""
    agent_id: str
    title: str
    description: Optional[str] = None
    event_type: str = "appointment"
    event_date: date
    event_time: time
    duration_minutes: int = Field(default=30, gt=0, le=480)
    participant_name: Optional[str] = None
    participant_email: Optional[str] = None
    participant_phone: Optional[str] = None
    status: str = "pending"
    notes: Optional[str] = None
    created_via: str = "voice"

    @validator('status')
    def validate_status(cls, v):
        allowed = ['pending', 'confirmed', 'cancelled', 'completed']
        if v not in allowed:
            raise ValueError(f'Status must be one of {allowed}')
        return v

    @validator('event_type')
    def validate_event_type(cls, v):
        allowed = ['appointment', 'meeting', 'call', 'consultation']
        if v not in allowed:
            raise ValueError(f'Event type must be one of {allowed}')
        return v


class CalendarEventUpdate(BaseModel):
    """Model for updating a calendar event"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None
    event_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(default=None, gt=0, le=480)
    status: Optional[str] = None
    notes: Optional[str] = None


class BusinessHoursConfig(BaseModel):
    """Model for business hours configuration"""
    working_hours: Dict  # {"monday": [{"start": "09:00", "end": "17:00"}], ...}
    break_times: List[Dict] = Field(default_factory=list)
    default_appointment_duration: int = Field(default=45, gt=0, le=480)
    buffer_time_minutes: int = Field(default=0, ge=0, le=60)
    min_advance_booking_hours: int = Field(default=2, ge=0)
    max_advance_booking_days: int = Field(default=90, gt=0)
    timezone: str = "UTC"


class AvailableSlotRequest(BaseModel):
    """Request model for checking available time slots"""
    agent_id: str
    date: date
    duration_minutes: int = Field(default=30, gt=0, le=480)


class BookAppointmentRequest(BaseModel):
    """Request model for booking appointment via voice agent"""
    agent_id: str
    participant_name: str
    date: date
    start_time: time
    duration_minutes: int = Field(default=30, gt=0, le=480)
    description: Optional[str] = None
    participant_phone: Optional[str] = None
    participant_email: Optional[str] = None


# ==================== API Endpoint Functions ====================
# These functions should be added to main.py

def add_calendar_routes(app, supabase):
    """
    Add calendar routes to FastAPI app
    Call this from main.py: add_calendar_routes(app, supabase)
    """

    @app.get("/api/calendar/events")
    async def get_calendar_events(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        agent_id: Optional[str] = None
    ):
        """
        Get calendar events filtered by date range and agent
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            query = supabase.table("calendar_events").select("*")

            # Apply filters
            if agent_id:
                query = query.eq("agent_id", agent_id)
            if start_date:
                query = query.gte("event_date", start_date.isoformat())
            if end_date:
                query = query.lte("event_date", end_date.isoformat())

            # Order by date
            query = query.order("event_date", desc=False).order("event_time", desc=False)

            response = query.execute()
            events = response.data

            logger.info(f"✅ Fetched {len(events)} calendar events")
            return events

        except Exception as e:
            logger.error(f"❌ Failed to fetch calendar events: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.post("/api/calendar/events")
    async def create_calendar_event(event: CalendarEventCreate):
        """
        Create a new calendar event
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            # Check if time slot is available
            is_available = await check_slot_availability(
                supabase,
                event.agent_id,
                event.event_date,
                event.event_time,
                event.duration_minutes
            )

            if not is_available:
                raise HTTPException(
                    status_code=409,
                    detail="Time slot is not available. Please choose a different time."
                )

            # Create event data
            event_data = event.dict()

            # Insert into database
            response = supabase.table("calendar_events").insert(event_data).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=500, detail="Failed to create calendar event")

            created_event = response.data[0]
            logger.info(f"✅ Created calendar event: {created_event['title']} on {created_event['event_date']}")

            return created_event

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to create calendar event: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.get("/api/calendar/events/{event_id}")
    async def get_calendar_event(event_id: str):
        """
        Get a specific calendar event by ID
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            response = supabase.table("calendar_events").select("*").eq("id", event_id).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

            return response.data[0]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to fetch event {event_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.put("/api/calendar/events/{event_id}")
    async def update_calendar_event(event_id: str, event: CalendarEventUpdate):
        """
        Update an existing calendar event
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            # Get existing event
            existing = supabase.table("calendar_events").select("*").eq("id", event_id).execute()
            if not existing.data or len(existing.data) == 0:
                raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

            # Update only provided fields
            update_data = event.dict(exclude_unset=True)

            # If time/date changed, check availability
            if 'event_date' in update_data or 'event_time' in update_data or 'duration_minutes' in update_data:
                existing_event = existing.data[0]
                check_date = update_data.get('event_date', existing_event['event_date'])
                check_time = update_data.get('event_time', existing_event['event_time'])
                check_duration = update_data.get('duration_minutes', existing_event['duration_minutes'])

                is_available = await check_slot_availability(
                    supabase,
                    existing_event['agent_id'],
                    check_date,
                    check_time,
                    check_duration,
                    exclude_event_id=event_id
                )

                if not is_available:
                    raise HTTPException(
                        status_code=409,
                        detail="New time slot is not available"
                    )

            # Update in database
            response = supabase.table("calendar_events").update(update_data).eq("id", event_id).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=500, detail="Failed to update event")

            logger.info(f"✅ Updated event {event_id}")
            return response.data[0]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to update event {event_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.delete("/api/calendar/events/{event_id}")
    async def delete_calendar_event(event_id: str):
        """
        Delete a calendar event
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            response = supabase.table("calendar_events").delete().eq("id", event_id).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=404, detail=f"Event {event_id} not found")

            logger.info(f"✅ Deleted event {event_id}")
            return {"status": "success", "message": "Event deleted"}

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to delete event {event_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.get("/api/business-hours/{agent_id}")
    async def get_business_hours(agent_id: str):
        """
        Get business hours configuration for an agent
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            response = supabase.table("business_hours").select("*").eq("agent_id", agent_id).execute()

            if not response.data or len(response.data) == 0:
                # Return default business hours if none exist
                return {
                    "agent_id": agent_id,
                    "working_hours": {
                        "monday": [{"start": "09:00", "end": "17:00"}],
                        "tuesday": [{"start": "09:00", "end": "17:00"}],
                        "wednesday": [{"start": "09:00", "end": "17:00"}],
                        "thursday": [{"start": "09:00", "end": "17:00"}],
                        "friday": [{"start": "09:00", "end": "17:00"}]
                    },
                    "break_times": [
                        {
                            "name": "Lunch Break",
                            "start": "12:30",
                            "end": "13:30",
                            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                        }
                    ],
                    "default_appointment_duration": 45,
                    "buffer_time_minutes": 0
                }

            return response.data[0]

        except Exception as e:
            logger.error(f"❌ Failed to fetch business hours for agent {agent_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.post("/api/business-hours/{agent_id}")
    async def update_business_hours(agent_id: str, config: BusinessHoursConfig):
        """
        Update business hours configuration for an agent
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            # Check if business hours exist
            existing = supabase.table("business_hours").select("*").eq("agent_id", agent_id).execute()

            config_data = config.dict()
            config_data["agent_id"] = agent_id

            if existing.data and len(existing.data) > 0:
                # Update existing
                response = supabase.table("business_hours").update(config_data).eq("agent_id", agent_id).execute()
            else:
                # Insert new
                response = supabase.table("business_hours").insert(config_data).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=500, detail="Failed to update business hours")

            logger.info(f"✅ Updated business hours for agent {agent_id}")
            return response.data[0]

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to update business hours for agent {agent_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.post("/api/calendar/available-slots")
    async def get_available_slots(request: AvailableSlotRequest):
        """
        Get available time slots for a specific agent on a specific date
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            # Call the PostgreSQL function
            response = supabase.rpc(
                "get_available_slots",
                {
                    "p_agent_id": request.agent_id,
                    "p_date": request.date.isoformat(),
                    "p_slot_duration": request.duration_minutes
                }
            ).execute()

            slots = response.data or []

            logger.info(f"✅ Found {len(slots)} time slots for agent {request.agent_id} on {request.date}")
            return {
                "date": request.date.isoformat(),
                "agent_id": request.agent_id,
                "slots": slots
            }

        except Exception as e:
            logger.error(f"❌ Failed to get available slots: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    @app.post("/api/calendar/book")
    async def book_appointment(request: BookAppointmentRequest):
        """
        Book an appointment (used by voice agent tool)
        This is a convenience endpoint that combines availability check + event creation
        """
        if not supabase:
            raise HTTPException(status_code=503, detail="Database not configured")

        try:
            # Check availability
            is_available = await check_slot_availability(
                supabase,
                request.agent_id,
                request.date,
                request.start_time,
                request.duration_minutes
            )

            if not is_available:
                raise HTTPException(
                    status_code=409,
                    detail=f"Time slot {request.start_time} on {request.date} is not available"
                )

            # Create event
            event_data = {
                "agent_id": request.agent_id,
                "title": f"Appointment with {request.participant_name}",
                "description": request.description,
                "event_type": "appointment",
                "event_date": request.date.isoformat(),
                "event_time": request.start_time.isoformat(),
                "duration_minutes": request.duration_minutes,
                "participant_name": request.participant_name,
                "participant_email": request.participant_email,
                "participant_phone": request.participant_phone,
                "status": "confirmed",
                "created_via": "voice"
            }

            response = supabase.table("calendar_events").insert(event_data).execute()

            if not response.data or len(response.data) == 0:
                raise HTTPException(status_code=500, detail="Failed to book appointment")

            created_event = response.data[0]
            logger.info(f"✅ Booked appointment for {request.participant_name} on {request.date} at {request.start_time}")

            return {
                "status": "success",
                "message": f"Appointment booked successfully for {request.date} at {request.start_time}",
                "event": created_event
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Failed to book appointment: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ==================== Helper Functions ====================

async def check_slot_availability(
    supabase,
    agent_id: str,
    event_date: date,
    start_time: time,
    duration_minutes: int,
    exclude_event_id: Optional[str] = None
) -> bool:
    """
    Check if a time slot is available for booking
    Returns True if available, False if conflict exists
    """
    try:
        # Calculate end time
        start_datetime = datetime.combine(event_date, start_time)
        end_datetime = start_datetime + timedelta(minutes=duration_minutes)
        end_time = end_datetime.time()

        # Query for conflicting appointments
        query = supabase.table("calendar_events") \
            .select("*") \
            .eq("agent_id", agent_id) \
            .eq("event_date", event_date.isoformat()) \
            .in_("status", ["pending", "confirmed"])

        # Exclude current event if updating
        if exclude_event_id:
            query = query.neq("id", exclude_event_id)

        response = query.execute()
        existing_events = response.data

        # Check for time conflicts
        for event in existing_events:
            event_start = datetime.strptime(event['event_time'], '%H:%M:%S').time()
            event_end_datetime = datetime.combine(
                event_date,
                event_start
            ) + timedelta(minutes=event['duration_minutes'])
            event_end = event_end_datetime.time()

            # Check for overlap
            if (
                (start_time >= event_start and start_time < event_end) or  # Starts during existing
                (end_time > event_start and end_time <= event_end) or  # Ends during existing
                (start_time <= event_start and end_time >= event_end)  # Encompasses existing
            ):
                logger.info(f"⚠️  Time conflict found with event: {event['title']}")
                return False

        return True

    except Exception as e:
        logger.error(f"❌ Error checking availability: {e}")
        return False
