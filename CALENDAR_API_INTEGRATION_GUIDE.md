# 🤝 Calendar API Integration Guide

**Complete Handshake Protocol for AIOOS Calendar System**

Version: 1.0
Last Updated: 2025-11-30
Status: Draft

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Server A (AIOOS Calendar Provider)](#server-a-aioos-calendar-provider)
4. [Server B (External Booking Client)](#server-b-external-booking-client)
5. [Connection Point #1: Query Free Slots](#connection-point-1-query-free-slots)
6. [Connection Point #2: Book Appointment](#connection-point-2-book-appointment)
7. [Authentication](#authentication)
8. [Data Types & Validation](#data-types--validation)
9. [Error Handling](#error-handling)
10. [Testing Guide](#testing-guide)
11. [Implementation Examples](#implementation-examples)
12. [Troubleshooting](#troubleshooting)

---

## Overview

This document describes the integration protocol between two systems:

- **Server A (AIOOS)**: Calendar provider that exposes available time slots
- **Server B (External System)**: Booking client that wants to query and book appointments

### Integration Goals

✅ Server B can query available time slots from Server A
✅ Server B can book specific time slots on Server A
✅ Both systems agree on data formats and validation rules
✅ Proper error handling and conflict resolution
✅ Secure API key authentication

---

## Architecture

```
┌─────────────────────────────┐         ┌──────────────────────────────┐
│   SERVER A (AIOOS)          │  ←───→  │   SERVER B (External System) │
│   "Calendar Provider"       │         │   "Booking Client"           │
│                             │         │                              │
│   • Supabase PostgreSQL     │         │   • Your Database            │
│   • FastAPI Backend         │         │   • Your Backend             │
│   • Business Hours Config   │         │   • Booking Logic            │
│   • Availability Rules      │         │                              │
│                             │         │                              │
│   Exposes:                  │         │   Consumes:                  │
│   • GET /free-slots         │         │   • Calls GET /free-slots    │
│   • POST /external-booking  │         │   • Calls POST /booking      │
│                             │         │                              │
│   Location:                 │         │   Location:                  │
│   localhost:8000            │         │   api.example.com            │
└─────────────────────────────┘         └──────────────────────────────┘
```

### Communication Flow

```
Server B                           Server A
   │                                  │
   │  1. Query available slots        │
   ├─────────────────────────────────>│
   │     GET /free-slots              │
   │                                  │
   │  2. Receive slot list            │
   │<─────────────────────────────────┤
   │     {available_slots: [...]}     │
   │                                  │
   │  3. User picks a slot            │
   │                                  │
   │  4. Book selected slot           │
   ├─────────────────────────────────>│
   │     POST /external-booking       │
   │                                  │
   │  5. Receive confirmation         │
   │<─────────────────────────────────┤
   │     {booking_id, status}         │
   │                                  │
```

---

## Server A (AIOOS Calendar Provider)

### Role & Responsibilities

Server A is the **calendar owner** that:
- ✅ Maintains agent schedules and business hours
- ✅ Tracks all booked appointments in database
- ✅ Exposes available time slots via API
- ✅ Validates booking requests before confirming
- ✅ Prevents double-booking conflicts
- ✅ Enforces business rules (min/max booking windows)

### Database Structure

```sql
-- Main events table
CREATE TABLE calendar_events (
    id UUID PRIMARY KEY,
    agent_id UUID NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL,
    participant_name VARCHAR(255),
    participant_email VARCHAR(255),
    participant_phone VARCHAR(50),
    status VARCHAR(50),  -- pending, confirmed, cancelled, completed
    created_via VARCHAR(50) DEFAULT 'api',
    metadata JSONB DEFAULT '{}'
);

-- Business hours configuration
CREATE TABLE business_hours (
    agent_id UUID UNIQUE NOT NULL,
    working_hours JSONB,  -- {"monday": [{"start": "09:00", "end": "17:00"}], ...}
    default_appointment_duration INTEGER DEFAULT 45,
    buffer_time_minutes INTEGER DEFAULT 0,
    min_advance_booking_hours INTEGER DEFAULT 2,
    max_advance_booking_days INTEGER DEFAULT 90,
    timezone VARCHAR(100) DEFAULT 'UTC'
);
```

### Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase PostgreSQL
- **Location**: `http://localhost:8000` (dev) or production URL

### Configuration

Server A requires these environment variables:

```bash
# .env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
CALENDAR_API_KEY=secret-key-abc123  # For authenticating Server B
```

---

## Server B (External Booking Client)

### Role & Responsibilities

Server B is the **booking consumer** that:
- ✅ Queries Server A for available time slots
- ✅ Displays available slots to end users
- ✅ Sends booking requests to Server A
- ✅ Handles booking confirmations and errors
- ✅ Stores booking references from Server A
- ✅ Manages its own user/customer data

### Required Information

Before integration, Server B needs:

| Item | Format | Example | Source |
|------|--------|---------|--------|
| **API Key** | String | `secret-key-abc123` | Provided by Server A admin |
| **Agent ID** | UUID | `47addfec-f4cd-41e2-b6ec-6a5e949fe754` | Provided by Server A admin |
| **Base URL** | URL | `http://localhost:8000` | Provided by Server A admin |
| **Timezone** | IANA | `UTC` or `America/New_York` | Agreed upon |

### Technology Stack

Server B can use any technology that supports:
- ✅ HTTP requests (GET, POST)
- ✅ JSON serialization/deserialization
- ✅ Date/time handling
- ✅ Header management for API keys

Examples: Python, Node.js, PHP, Java, C#, etc.

---

## Connection Point #1: Query Free Slots

### Purpose

Server B queries Server A to get all available time slots for a specific agent within a date range.

### Endpoint Details

**Method**: `GET`
**Path**: `/api/calendar/free-slots/{agent_id}`
**Authorization**: API Key (header)

### Request Specification

#### URL Parameters

| Parameter | Type | Required | Format | Example |
|-----------|------|----------|--------|---------|
| `agent_id` | string | ✅ YES | UUID v4 | `47addfec-f4cd-41e2-b6ec-6a5e949fe754` |

#### Query Parameters

| Parameter | Type | Required | Format | Validation | Example |
|-----------|------|----------|--------|------------|---------|
| `start_date` | string | ✅ YES | `YYYY-MM-DD` | Must be valid date | `2025-12-01` |
| `end_date` | string | ✅ YES | `YYYY-MM-DD` | Must be >= start_date | `2025-12-07` |
| `duration_minutes` | integer | ❌ NO | Number | 1-480, default: 30 | `45` |

#### Headers

```http
X-API-Key: secret-key-abc123
Accept: application/json
```

#### Full Request Example

```http
GET /api/calendar/free-slots/47addfec-f4cd-41e2-b6ec-6a5e949fe754?start_date=2025-12-01&end_date=2025-12-07&duration_minutes=30 HTTP/1.1
Host: localhost:8000
X-API-Key: secret-key-abc123
Accept: application/json
```

### Response Specification

#### Success Response (200 OK)

```json
{
  "agent_id": "47addfec-f4cd-41e2-b6ec-6a5e949fe754",
  "start_date": "2025-12-01",
  "end_date": "2025-12-07",
  "timezone": "UTC",
  "slot_duration_minutes": 30,
  "total_days_with_availability": 5,
  "available_slots": [
    {
      "date": "2025-12-01",
      "day_of_week": "Monday",
      "total_slots": 12,
      "slots": [
        {
          "start": "09:00",
          "end": "09:30",
          "duration_minutes": 30
        },
        {
          "start": "09:30",
          "end": "10:00",
          "duration_minutes": 30
        },
        {
          "start": "10:00",
          "end": "10:30",
          "duration_minutes": 30
        }
      ]
    },
    {
      "date": "2025-12-02",
      "day_of_week": "Tuesday",
      "total_slots": 10,
      "slots": [
        {
          "start": "14:00",
          "end": "14:30",
          "duration_minutes": 30
        },
        {
          "start": "14:30",
          "end": "15:00",
          "duration_minutes": 30
        }
      ]
    }
  ]
}
```

#### Response Schema

```typescript
interface FreeSlotResponse {
  agent_id: string;                      // UUID format
  start_date: string;                    // ISO date "YYYY-MM-DD"
  end_date: string;                      // ISO date "YYYY-MM-DD"
  timezone: string;                      // IANA timezone
  slot_duration_minutes: number;
  total_days_with_availability: number;
  available_slots: DaySlots[];
}

interface DaySlots {
  date: string;                          // ISO date "YYYY-MM-DD"
  day_of_week: string;                   // "Monday", "Tuesday", etc.
  total_slots: number;
  slots: TimeSlot[];
}

interface TimeSlot {
  start: string;                         // 24-hour time "HH:MM"
  end: string;                           // 24-hour time "HH:MM"
  duration_minutes: number;
}
```

#### Error Responses

| Status Code | Scenario | Response Body |
|-------------|----------|---------------|
| `401` | Invalid API key | `{"detail": "Invalid API key"}` |
| `404` | Agent not found | `{"detail": "Business hours not found for agent {id}"}` |
| `400` | Invalid date range | `{"detail": "end_date must be after start_date"}` |
| `400` | Range too large | `{"detail": "Date range cannot exceed 90 days"}` |

### Server A Implementation

```python
# calendar_api.py (Server A)

@app.get("/api/calendar/free-slots/{agent_id}")
async def get_free_time_slots(
    agent_id: str,
    start_date: date,
    end_date: date,
    duration_minutes: int = 30,
    x_api_key: str = Header(None)
):
    """
    Get all available free time slots for an agent in a date range
    """
    # 1. Validate API key
    if x_api_key != os.getenv("CALENDAR_API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2. Validate date range
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="end_date must be after start_date")

    if (end_date - start_date).days > 90:
        raise HTTPException(status_code=400, detail="Date range cannot exceed 90 days")

    # 3. Get business hours
    bh_response = supabase.table("business_hours").select("*").eq("agent_id", agent_id).execute()
    if not bh_response.data:
        raise HTTPException(status_code=404, detail=f"Business hours not found")

    business_hours = bh_response.data[0]
    timezone = business_hours.get("timezone", "UTC")

    # 4. Collect slots for each day
    available_slots = []
    current_date = start_date

    while current_date <= end_date:
        # Call PostgreSQL function
        slots_response = supabase.rpc(
            "get_available_slots",
            {
                "p_agent_id": agent_id,
                "p_date": current_date.isoformat(),
                "p_slot_duration": duration_minutes
            }
        ).execute()

        day_slots = []
        for slot in (slots_response.data or []):
            if slot.get("is_available"):
                day_slots.append({
                    "start": slot["start_time"],
                    "end": slot["end_time"],
                    "duration_minutes": duration_minutes
                })

        if day_slots:
            available_slots.append({
                "date": current_date.isoformat(),
                "day_of_week": current_date.strftime("%A"),
                "slots": day_slots,
                "total_slots": len(day_slots)
            })

        current_date += timedelta(days=1)

    return {
        "agent_id": agent_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "timezone": timezone,
        "slot_duration_minutes": duration_minutes,
        "total_days_with_availability": len(available_slots),
        "available_slots": available_slots
    }
```

### Server B Implementation

```python
# booking_client.py (Server B)

import requests
from typing import Dict, List

class CalendarClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_free_slots(
        self,
        agent_id: str,
        start_date: str,
        end_date: str,
        duration_minutes: int = 30
    ) -> Dict:
        """
        Query Server A for available time slots

        Args:
            agent_id: UUID of the agent
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            duration_minutes: Desired slot duration (default: 30)

        Returns:
            Dict containing available_slots

        Raises:
            requests.HTTPError: If API returns error
        """
        url = f"{self.base_url}/api/calendar/free-slots/{agent_id}"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "duration_minutes": duration_minutes
        }
        headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises exception for 4xx/5xx

        return response.json()

# Usage example
client = CalendarClient("http://localhost:8000", "secret-key-abc123")
slots = client.get_free_slots(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    start_date="2025-12-01",
    end_date="2025-12-07"
)

print(f"Found {len(slots['available_slots'])} days with availability")
```

---

## Connection Point #2: Book Appointment

### Purpose

Server B sends a booking request to reserve a specific time slot on Server A.

### Endpoint Details

**Method**: `POST`
**Path**: `/api/calendar/external-booking`
**Authorization**: API Key (header or body)
**Content-Type**: `application/json`

### Request Specification

#### Headers

```http
X-API-Key: secret-key-abc123
Content-Type: application/json
Accept: application/json
```

#### Request Body

```json
{
  "agent_id": "47addfec-f4cd-41e2-b6ec-6a5e949fe754",
  "participant_name": "John Doe",
  "participant_email": "john@example.com",
  "participant_phone": "+1-555-0123",
  "booking_date": "2025-12-05",
  "booking_time": "14:30",
  "duration_minutes": 45,
  "description": "Initial consultation call",
  "external_reference_id": "EXT-BOOKING-12345",
  "api_key": "secret-key-abc123"
}
```

#### Field Specifications

| Field | Type | Required | Format | Max Length | Validation | Example |
|-------|------|----------|--------|------------|------------|---------|
| `agent_id` | string | ✅ YES | UUID v4 | - | Valid UUID | `47addfec-...` |
| `participant_name` | string | ✅ YES | Text | 255 | Not empty | `"John Doe"` |
| `participant_email` | string | ❌ NO | Email | 255 | Valid email or null | `"john@example.com"` |
| `participant_phone` | string | ❌ NO | Phone | 50 | Any format | `"+1-555-0123"` |
| `booking_date` | string | ✅ YES | `YYYY-MM-DD` | - | Future date | `"2025-12-05"` |
| `booking_time` | string | ✅ YES | `HH:MM` | - | 24-hour format | `"14:30"` |
| `duration_minutes` | integer | ❌ NO | Number | - | 1-480, default: 30 | `45` |
| `description` | string | ❌ NO | Text | - | Any text | `"Consultation"` |
| `external_reference_id` | string | ❌ NO | Text | 255 | Your tracking ID | `"EXT-12345"` |
| `api_key` | string | ✅ YES* | Text | - | Valid API key | `"secret-key-abc123"` |

*Required if not provided in header

#### Full Request Example

```http
POST /api/calendar/external-booking HTTP/1.1
Host: localhost:8000
X-API-Key: secret-key-abc123
Content-Type: application/json
Accept: application/json

{
  "agent_id": "47addfec-f4cd-41e2-b6ec-6a5e949fe754",
  "participant_name": "John Doe",
  "participant_email": "john@example.com",
  "booking_date": "2025-12-05",
  "booking_time": "14:30",
  "duration_minutes": 45,
  "external_reference_id": "EXT-12345",
  "api_key": "secret-key-abc123"
}
```

### Response Specification

#### Success Response (201 Created)

```json
{
  "status": "success",
  "booking_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Booking confirmed for 2025-12-05 at 14:30",
  "details": {
    "event_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "agent_id": "47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    "participant_name": "John Doe",
    "booking_date": "2025-12-05",
    "booking_time": "14:30",
    "duration_minutes": 45,
    "external_reference_id": "EXT-BOOKING-12345"
  }
}
```

#### Response Schema

```typescript
interface BookingResponse {
  status: "success" | "error";
  booking_id: string;                    // UUID of created event
  message: string;                       // Human-readable confirmation
  details: {
    event_id: string;                    // Same as booking_id
    agent_id: string;
    participant_name: string;
    booking_date: string;                // ISO date
    booking_time: string;                // 24h time
    duration_minutes: number;
    external_reference_id: string | null;
  };
}
```

#### Error Responses

| Status Code | Scenario | Response Body |
|-------------|----------|---------------|
| `401` | Invalid API key | `{"detail": "Invalid API key"}` |
| `400` | Date in past | `{"detail": "Cannot book in the past"}` |
| `400` | Too soon | `{"detail": "Bookings must be made at least 2 hours in advance"}` |
| `400` | Too far ahead | `{"detail": "Cannot book more than 90 days in advance"}` |
| `409` | Slot already booked | `{"detail": "Time slot 14:30 on 2025-12-05 is not available"}` |
| `422` | Invalid format | `{"detail": [{"loc": ["body", "booking_time"], "msg": "Invalid time format"}]}` |
| `500` | Server error | `{"detail": "Booking error: Database connection failed"}` |

### Validation Rules

Server A will validate:

1. **API Key**: Must match configured key
2. **Past Date**: `booking_date` >= today
3. **Advance Booking Window**:
   - Minimum: 2 hours from now (configurable)
   - Maximum: 90 days from now (configurable)
4. **Availability**: Slot must be free (no overlapping bookings)
5. **Business Hours**: Time must fall within working hours
6. **Data Formats**: All fields must match specified formats

### Server A Implementation

```python
# calendar_api.py (Server A)

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime, timedelta

class ExternalBookingRequest(BaseModel):
    agent_id: str
    participant_name: str
    participant_email: Optional[str] = None
    participant_phone: Optional[str] = None
    booking_date: date
    booking_time: time
    duration_minutes: int = Field(default=30, gt=0, le=480)
    description: Optional[str] = None
    external_reference_id: Optional[str] = None
    api_key: str

@app.post("/api/calendar/external-booking", status_code=201)
async def create_external_booking(
    request: ExternalBookingRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Accept booking requests from external APIs
    """
    # 1. Validate API key
    api_key = x_api_key or request.api_key
    expected_key = os.getenv("CALENDAR_API_KEY")

    if not expected_key or api_key != expected_key:
        logger.warning("Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 2. Validate date is not in past
    today = date.today()
    if request.booking_date < today:
        raise HTTPException(status_code=400, detail="Cannot book in the past")

    # 3. Check business hours constraints
    bh_response = supabase.table("business_hours").select("*").eq("agent_id", request.agent_id).execute()
    if bh_response.data:
        business_hours = bh_response.data[0]

        # Check minimum advance booking
        min_hours = business_hours.get("min_advance_booking_hours", 2)
        booking_datetime = datetime.combine(request.booking_date, request.booking_time)
        now = datetime.now()
        hours_until = (booking_datetime - now).total_seconds() / 3600

        if hours_until < min_hours:
            raise HTTPException(
                status_code=400,
                detail=f"Bookings must be made at least {min_hours} hours in advance"
            )

        # Check maximum advance booking
        max_days = business_hours.get("max_advance_booking_days", 90)
        days_until = (request.booking_date - today).days

        if days_until > max_days:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot book more than {max_days} days in advance"
            )

    # 4. Check availability
    is_available = await check_slot_availability(
        supabase,
        request.agent_id,
        request.booking_date,
        request.booking_time,
        request.duration_minutes
    )

    if not is_available:
        raise HTTPException(
            status_code=409,
            detail=f"Time slot {request.booking_time} on {request.booking_date} is not available"
        )

    # 5. Create booking
    event_data = {
        "agent_id": request.agent_id,
        "title": f"External Booking - {request.participant_name}",
        "description": request.description or "Booked via external API",
        "event_type": "appointment",
        "event_date": request.booking_date.isoformat(),
        "event_time": request.booking_time.isoformat(),
        "duration_minutes": request.duration_minutes,
        "participant_name": request.participant_name,
        "participant_email": request.participant_email,
        "participant_phone": request.participant_phone,
        "status": "confirmed",
        "created_via": "api",
        "metadata": {
            "external_reference_id": request.external_reference_id,
            "booking_source": "external_api"
        }
    }

    response = supabase.table("calendar_events").insert(event_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create booking")

    created_event = response.data[0]

    logger.info(
        f"External booking created: {request.participant_name} on "
        f"{request.booking_date} at {request.booking_time}"
    )

    return {
        "status": "success",
        "booking_id": created_event["id"],
        "message": f"Booking confirmed for {request.booking_date} at {request.booking_time}",
        "details": {
            "event_id": created_event["id"],
            "agent_id": request.agent_id,
            "participant_name": request.participant_name,
            "booking_date": str(request.booking_date),
            "booking_time": str(request.booking_time),
            "duration_minutes": request.duration_minutes,
            "external_reference_id": request.external_reference_id
        }
    }
```

### Server B Implementation

```python
# booking_client.py (Server B)

class CalendarClient:
    # ... (previous code) ...

    def book_appointment(
        self,
        agent_id: str,
        participant_name: str,
        booking_date: str,
        booking_time: str,
        duration_minutes: int = 30,
        **kwargs
    ) -> Dict:
        """
        Book a specific time slot on Server A

        Args:
            agent_id: UUID of the agent
            participant_name: Name of person booking
            booking_date: Date in YYYY-MM-DD format
            booking_time: Time in HH:MM format (24-hour)
            duration_minutes: Duration (default: 30)
            **kwargs: Optional fields (email, phone, description, etc.)

        Returns:
            Dict containing booking_id and confirmation

        Raises:
            requests.HTTPError: If booking fails
        """
        url = f"{self.base_url}/api/calendar/external-booking"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "agent_id": agent_id,
            "participant_name": participant_name,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "duration_minutes": duration_minutes,
            "api_key": self.api_key,
            **kwargs
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        return response.json()

# Usage example
client = CalendarClient("http://localhost:8000", "secret-key-abc123")

# First, get available slots
slots = client.get_free_slots(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    start_date="2025-12-01",
    end_date="2025-12-07"
)

# Pick first available slot
first_day = slots['available_slots'][0]
first_slot = first_day['slots'][0]

# Book it
booking = client.book_appointment(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    participant_name="John Doe",
    booking_date=first_day['date'],
    booking_time=first_slot['start'],
    duration_minutes=30,
    participant_email="john@example.com",
    external_reference_id="MY-SYSTEM-REF-123"
)

print(f"Booking confirmed! ID: {booking['booking_id']}")
```

---

## Authentication

### API Key Authentication

Both endpoints require API key authentication for security.

#### Method 1: Header-based (Recommended)

```http
X-API-Key: secret-key-abc123
```

#### Method 2: Body-based (POST only)

```json
{
  "api_key": "secret-key-abc123",
  ...
}
```

### Configuration

**Server A** must set in `.env`:

```bash
CALENDAR_API_KEY=secret-key-abc123
```

**Server B** must store securely:

```python
# Use environment variables, not hardcoded!
API_KEY = os.getenv("AIOOS_API_KEY")
```

### Security Best Practices

✅ **DO**:
- Use HTTPS in production
- Store API keys in environment variables
- Rotate API keys periodically
- Use different keys for dev/staging/production
- Log failed authentication attempts

❌ **DON'T**:
- Hardcode API keys in source code
- Commit API keys to version control
- Share API keys via email/chat
- Use same key across multiple clients

---

## Data Types & Validation

### Date Formats

| Field | Format | Example | Regex |
|-------|--------|---------|-------|
| Date | `YYYY-MM-DD` | `2025-12-05` | `^\d{4}-\d{2}-\d{2}$` |
| Time | `HH:MM` | `14:30` | `^\d{2}:\d{2}$` |
| DateTime | ISO 8601 | `2025-12-05T14:30:00Z` | - |

### Type Mapping

**Python (Server A)**:
```python
from datetime import date, time, datetime

booking_date: date         # date(2025, 12, 5)
booking_time: time         # time(14, 30)
duration_minutes: int      # 45
```

**JavaScript/TypeScript (Server B)**:
```typescript
booking_date: string       // "2025-12-05"
booking_time: string       // "14:30"
duration_minutes: number   // 45
```

**JSON**:
```json
{
  "booking_date": "2025-12-05",
  "booking_time": "14:30",
  "duration_minutes": 45
}
```

### Common Mistakes

❌ **Wrong**:
```json
{
  "booking_date": "12/05/2025",          // American format
  "booking_time": "2:30 PM",             // 12-hour format
  "duration_minutes": "45",              // String instead of number
  "duration_minutes": 45.5               // Decimal not allowed
}
```

✅ **Correct**:
```json
{
  "booking_date": "2025-12-05",          // ISO format
  "booking_time": "14:30",               // 24-hour format
  "duration_minutes": 45                 // Integer
}
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Human-readable error message"
}
```

For validation errors (422):

```json
{
  "detail": [
    {
      "loc": ["body", "booking_time"],
      "msg": "Invalid time format",
      "type": "value_error"
    }
  ]
}
```

### HTTP Status Codes

| Code | Meaning | When to Retry |
|------|---------|---------------|
| `200` | Success (GET) | - |
| `201` | Created (POST) | - |
| `400` | Bad Request | ❌ Fix request and retry |
| `401` | Unauthorized | ❌ Check API key |
| `404` | Not Found | ❌ Check agent_id |
| `409` | Conflict | ❌ Slot taken, choose different time |
| `422` | Validation Error | ❌ Fix data format |
| `500` | Server Error | ✅ Retry with backoff |
| `503` | Service Unavailable | ✅ Retry with backoff |

### Error Handling Best Practices

**Server B should**:

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    """Create session with automatic retries for 5xx errors"""
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Usage
session = create_session_with_retries()

try:
    response = session.post(url, json=data, headers=headers)
    response.raise_for_status()
    booking = response.json()

except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key - check credentials")
    elif e.response.status_code == 409:
        print("Slot already booked - choose different time")
    elif e.response.status_code >= 500:
        print("Server error - will retry automatically")
    else:
        print(f"Error: {e.response.json()['detail']}")

except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

---

## Testing Guide

### Pre-Integration Testing

Before connecting to Server A, Server B should verify:

#### 1. Date/Time Formatting

```python
from datetime import date, time

# Test date format
test_date = date(2025, 12, 5)
assert test_date.isoformat() == "2025-12-05"

# Test time format
test_time = time(14, 30)
assert test_time.strftime("%H:%M") == "14:30"
```

#### 2. JSON Serialization

```python
import json

payload = {
    "booking_date": "2025-12-05",
    "booking_time": "14:30",
    "duration_minutes": 45
}

# Should not throw error
json_string = json.dumps(payload)
parsed = json.loads(json_string)
assert parsed["duration_minutes"] == 45  # Number, not string
```

### Integration Testing Scenarios

#### Test 1: Valid Free Slots Query ✅

```python
# Expected: 200 OK
response = client.get_free_slots(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    start_date="2025-12-01",
    end_date="2025-12-07"
)
assert response["agent_id"] == "47addfec-f4cd-41e2-b6ec-6a5e949fe754"
assert len(response["available_slots"]) >= 0
```

#### Test 2: Invalid API Key ❌

```python
# Expected: 401 Unauthorized
try:
    client_bad = CalendarClient(BASE_URL, "wrong-api-key")
    client_bad.get_free_slots(...)
    assert False, "Should have raised error"
except requests.HTTPError as e:
    assert e.response.status_code == 401
```

#### Test 3: Valid Booking ✅

```python
# Expected: 201 Created
booking = client.book_appointment(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    participant_name="Test User",
    booking_date="2025-12-15",  # Future date
    booking_time="10:00",
    duration_minutes=30
)
assert booking["status"] == "success"
assert "booking_id" in booking
```

#### Test 4: Past Date Booking ❌

```python
# Expected: 400 Bad Request
try:
    client.book_appointment(
        agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
        participant_name="Test User",
        booking_date="2020-01-01",  # Past date
        booking_time="10:00"
    )
    assert False, "Should have raised error"
except requests.HTTPError as e:
    assert e.response.status_code == 400
    assert "past" in e.response.json()["detail"].lower()
```

#### Test 5: Duplicate Booking ❌

```python
# Expected: 409 Conflict on second attempt
booking1 = client.book_appointment(
    agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
    participant_name="User 1",
    booking_date="2025-12-20",
    booking_time="15:00"
)
assert booking1["status"] == "success"

# Try to book same slot again
try:
    booking2 = client.book_appointment(
        agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
        participant_name="User 2",
        booking_date="2025-12-20",
        booking_time="15:00"
    )
    assert False, "Should have raised conflict error"
except requests.HTTPError as e:
    assert e.response.status_code == 409
```

#### Test 6: Invalid Time Format ❌

```python
# Expected: 422 Validation Error
try:
    client.book_appointment(
        agent_id="47addfec-f4cd-41e2-b6ec-6a5e949fe754",
        participant_name="Test User",
        booking_date="2025-12-15",
        booking_time="2:30 PM"  # Wrong format!
    )
    assert False, "Should have raised validation error"
except requests.HTTPError as e:
    assert e.response.status_code == 422
```

### Test Checklist

Server B should verify all these before going live:

- [ ] ✅ Can query free slots successfully
- [ ] ✅ Can book available slot successfully
- [ ] ❌ Gets 401 with invalid API key
- [ ] ❌ Gets 400 for past dates
- [ ] ❌ Gets 409 for duplicate bookings
- [ ] ❌ Gets 422 for invalid formats
- [ ] ✅ Handles 500 errors with retry
- [ ] ✅ Stores booking_id from Server A
- [ ] ✅ Logs all API calls for debugging

---

## Implementation Examples

### Complete Python Client (Server B)

```python
# calendar_integration.py

import os
import requests
from typing import Dict, List, Optional
from datetime import date, time
import logging

logger = logging.getLogger(__name__)

class CalendarAPIError(Exception):
    """Base exception for calendar API errors"""
    pass

class AuthenticationError(CalendarAPIError):
    """API key is invalid"""
    pass

class BookingConflictError(CalendarAPIError):
    """Time slot is already booked"""
    pass

class ValidationError(CalendarAPIError):
    """Request data is invalid"""
    pass

class CalendarClient:
    """
    Client for AIOOS Calendar API

    Usage:
        client = CalendarClient(
            base_url="http://localhost:8000",
            api_key="secret-key-abc123"
        )

        slots = client.get_free_slots(
            agent_id="47addfec-...",
            start_date="2025-12-01",
            end_date="2025-12-07"
        )

        booking = client.book_appointment(
            agent_id="47addfec-...",
            participant_name="John Doe",
            booking_date="2025-12-05",
            booking_time="14:30"
        )
    """

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and raise appropriate errors"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            status = e.response.status_code

            try:
                error_detail = e.response.json().get('detail', 'Unknown error')
            except:
                error_detail = e.response.text

            if status == 401:
                raise AuthenticationError(f"Invalid API key: {error_detail}")
            elif status == 409:
                raise BookingConflictError(f"Booking conflict: {error_detail}")
            elif status == 422:
                raise ValidationError(f"Validation error: {error_detail}")
            else:
                raise CalendarAPIError(f"API error ({status}): {error_detail}")

    def get_free_slots(
        self,
        agent_id: str,
        start_date: str,
        end_date: str,
        duration_minutes: int = 30
    ) -> Dict:
        """
        Get available time slots for an agent

        Args:
            agent_id: UUID of the agent
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            duration_minutes: Slot duration (default: 30)

        Returns:
            {
                "agent_id": "...",
                "available_slots": [...]
            }

        Raises:
            AuthenticationError: Invalid API key
            CalendarAPIError: Other API errors
        """
        url = f"{self.base_url}/api/calendar/free-slots/{agent_id}"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "duration_minutes": duration_minutes
        }

        logger.info(f"Querying free slots for agent {agent_id}")
        response = self.session.get(url, params=params)

        data = self._handle_response(response)
        logger.info(f"Found {data['total_days_with_availability']} days with availability")

        return data

    def book_appointment(
        self,
        agent_id: str,
        participant_name: str,
        booking_date: str,
        booking_time: str,
        duration_minutes: int = 30,
        participant_email: Optional[str] = None,
        participant_phone: Optional[str] = None,
        description: Optional[str] = None,
        external_reference_id: Optional[str] = None
    ) -> Dict:
        """
        Book an appointment

        Args:
            agent_id: UUID of the agent
            participant_name: Name of person booking
            booking_date: Date (YYYY-MM-DD)
            booking_time: Time (HH:MM, 24-hour)
            duration_minutes: Duration (default: 30)
            participant_email: Optional email
            participant_phone: Optional phone
            description: Optional description
            external_reference_id: Your system's reference ID

        Returns:
            {
                "status": "success",
                "booking_id": "...",
                "message": "..."
            }

        Raises:
            AuthenticationError: Invalid API key
            BookingConflictError: Slot already booked
            ValidationError: Invalid data format
            CalendarAPIError: Other API errors
        """
        url = f"{self.base_url}/api/calendar/external-booking"
        payload = {
            "agent_id": agent_id,
            "participant_name": participant_name,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "duration_minutes": duration_minutes,
            "api_key": self.api_key
        }

        # Add optional fields
        if participant_email:
            payload["participant_email"] = participant_email
        if participant_phone:
            payload["participant_phone"] = participant_phone
        if description:
            payload["description"] = description
        if external_reference_id:
            payload["external_reference_id"] = external_reference_id

        logger.info(f"Booking appointment for {participant_name} on {booking_date} at {booking_time}")
        response = self.session.post(url, json=payload)

        data = self._handle_response(response)
        logger.info(f"Booking successful: {data['booking_id']}")

        return data


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize client
    client = CalendarClient(
        base_url=os.getenv("AIOOS_BASE_URL", "http://localhost:8000"),
        api_key=os.getenv("AIOOS_API_KEY", "secret-key-abc123")
    )

    agent_id = "47addfec-f4cd-41e2-b6ec-6a5e949fe754"

    try:
        # Get free slots
        print("🔍 Fetching available slots...")
        slots = client.get_free_slots(
            agent_id=agent_id,
            start_date="2025-12-01",
            end_date="2025-12-07",
            duration_minutes=30
        )

        print(f"\n✅ Found {len(slots['available_slots'])} days with availability")

        # Show first day's slots
        if slots['available_slots']:
            first_day = slots['available_slots'][0]
            print(f"\n📅 {first_day['date']} ({first_day['day_of_week']}):")
            for slot in first_day['slots'][:5]:  # Show first 5 slots
                print(f"   • {slot['start']} - {slot['end']}")

            # Book first slot
            print(f"\n📝 Booking first slot...")
            first_slot = first_day['slots'][0]

            booking = client.book_appointment(
                agent_id=agent_id,
                participant_name="John Doe",
                booking_date=first_day['date'],
                booking_time=first_slot['start'],
                duration_minutes=30,
                participant_email="john@example.com",
                participant_phone="+1-555-0123",
                description="Test booking from Python client",
                external_reference_id="PYTHON-TEST-001"
            )

            print(f"\n✅ Booking confirmed!")
            print(f"   Booking ID: {booking['booking_id']}")
            print(f"   Message: {booking['message']}")

    except AuthenticationError:
        print("❌ Authentication failed - check your API key")
    except BookingConflictError as e:
        print(f"❌ Booking conflict: {e}")
    except ValidationError as e:
        print(f"❌ Invalid data: {e}")
    except CalendarAPIError as e:
        print(f"❌ API error: {e}")
```

### Node.js/TypeScript Client (Server B)

```typescript
// calendar-client.ts

import axios, { AxiosInstance, AxiosError } from 'axios';

interface TimeSlot {
  start: string;
  end: string;
  duration_minutes: number;
}

interface DaySlots {
  date: string;
  day_of_week: string;
  total_slots: number;
  slots: TimeSlot[];
}

interface FreeSlotResponse {
  agent_id: string;
  start_date: string;
  end_date: string;
  timezone: string;
  slot_duration_minutes: number;
  total_days_with_availability: number;
  available_slots: DaySlots[];
}

interface BookingRequest {
  agent_id: string;
  participant_name: string;
  booking_date: string;
  booking_time: string;
  duration_minutes?: number;
  participant_email?: string;
  participant_phone?: string;
  description?: string;
  external_reference_id?: string;
  api_key: string;
}

interface BookingResponse {
  status: 'success' | 'error';
  booking_id: string;
  message: string;
  details: {
    event_id: string;
    agent_id: string;
    participant_name: string;
    booking_date: string;
    booking_time: string;
    duration_minutes: number;
    external_reference_id: string | null;
  };
}

class CalendarAPIError extends Error {
  constructor(message: string, public statusCode?: number) {
    super(message);
    this.name = 'CalendarAPIError';
  }
}

export class CalendarClient {
  private client: AxiosInstance;

  constructor(baseURL: string, apiKey: string) {
    this.client = axios.create({
      baseURL,
      headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });
  }

  async getFreeSlots(
    agentId: string,
    startDate: string,
    endDate: string,
    durationMinutes: number = 30
  ): Promise<FreeSlotResponse> {
    try {
      const response = await this.client.get<FreeSlotResponse>(
        `/api/calendar/free-slots/${agentId}`,
        {
          params: {
            start_date: startDate,
            end_date: endDate,
            duration_minutes: durationMinutes
          }
        }
      );

      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  async bookAppointment(request: Omit<BookingRequest, 'api_key'>): Promise<BookingResponse> {
    try {
      const response = await this.client.post<BookingResponse>(
        '/api/calendar/external-booking',
        {
          ...request,
          api_key: this.client.defaults.headers['X-API-Key']
        }
      );

      return response.data;
    } catch (error) {
      this.handleError(error);
    }
  }

  private handleError(error: unknown): never {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError<{ detail: string }>;
      const status = axiosError.response?.status;
      const detail = axiosError.response?.data?.detail || 'Unknown error';

      if (status === 401) {
        throw new CalendarAPIError(`Authentication failed: ${detail}`, status);
      } else if (status === 409) {
        throw new CalendarAPIError(`Booking conflict: ${detail}`, status);
      } else if (status === 422) {
        throw new CalendarAPIError(`Validation error: ${detail}`, status);
      } else {
        throw new CalendarAPIError(`API error (${status}): ${detail}`, status);
      }
    }

    throw new CalendarAPIError('Network error');
  }
}

// Example usage
async function main() {
  const client = new CalendarClient(
    process.env.AIOOS_BASE_URL || 'http://localhost:8000',
    process.env.AIOOS_API_KEY || 'secret-key-abc123'
  );

  const agentId = '47addfec-f4cd-41e2-b6ec-6a5e949fe754';

  try {
    // Get free slots
    console.log('🔍 Fetching available slots...');
    const slots = await client.getFreeSlots(
      agentId,
      '2025-12-01',
      '2025-12-07',
      30
    );

    console.log(`✅ Found ${slots.available_slots.length} days with availability`);

    if (slots.available_slots.length > 0) {
      const firstDay = slots.available_slots[0];
      const firstSlot = firstDay.slots[0];

      // Book first slot
      console.log(`📝 Booking ${firstDay.date} at ${firstSlot.start}...`);

      const booking = await client.bookAppointment({
        agent_id: agentId,
        participant_name: 'John Doe',
        booking_date: firstDay.date,
        booking_time: firstSlot.start,
        duration_minutes: 30,
        participant_email: 'john@example.com',
        external_reference_id: 'NODE-TEST-001'
      });

      console.log(`✅ Booking confirmed!`);
      console.log(`   Booking ID: ${booking.booking_id}`);
    }
  } catch (error) {
    if (error instanceof CalendarAPIError) {
      console.error(`❌ ${error.message}`);
    } else {
      console.error('❌ Unexpected error:', error);
    }
  }
}

if (require.main === module) {
  main();
}
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "Invalid API key" (401)

**Symptoms**: All requests return 401

**Causes**:
- API key mismatch between Server A and Server B
- API key not set in Server A's `.env`
- Wrong header name or format

**Solutions**:
1. Verify Server A has `CALENDAR_API_KEY` in `.env`
2. Verify Server B uses exact same key
3. Check header is `X-API-Key` (case-sensitive)
4. Restart Server A after changing `.env`

```bash
# Server A - Check .env
cat v4liveKit/backend/.env | grep CALENDAR_API_KEY

# Should output:
# CALENDAR_API_KEY=secret-key-abc123
```

#### Issue 2: "Time slot not available" (409)

**Symptoms**: Booking fails with conflict error

**Causes**:
- Slot already booked by someone else
- Time between query and booking changed status
- Database has existing conflicting event

**Solutions**:
1. Query free slots again before booking
2. Implement retry with different slot
3. Check Server A database for conflicts

```python
# Retry logic
for attempt in range(3):
    slots = client.get_free_slots(...)
    if not slots['available_slots']:
        break

    try:
        booking = client.book_appointment(...)
        break  # Success!
    except BookingConflictError:
        continue  # Try next slot
```

#### Issue 3: "Cannot book in the past" (400)

**Symptoms**: Booking fails for past dates

**Causes**:
- Timezone mismatch (Server A in UTC, Server B in local time)
- Date calculation error
- System clock difference

**Solutions**:
1. Ensure both servers use same timezone
2. Always use future dates
3. Sync system clocks (NTP)

```python
from datetime import date, timedelta

# Always book at least 1 day ahead
tomorrow = (date.today() + timedelta(days=1)).isoformat()
booking = client.book_appointment(
    booking_date=tomorrow,
    ...
)
```

#### Issue 4: Validation errors (422)

**Symptoms**: Request rejected with field errors

**Causes**:
- Wrong date/time format
- Duration as string instead of number
- Missing required fields

**Solutions**:
1. Use `YYYY-MM-DD` for dates
2. Use `HH:MM` (24-hour) for times
3. Send duration as number, not string

```python
# ❌ Wrong
{
    "booking_date": "12/05/2025",      # Wrong format
    "booking_time": "2:30 PM",         # Wrong format
    "duration_minutes": "45"           # Wrong type
}

# ✅ Correct
{
    "booking_date": "2025-12-05",      # ISO format
    "booking_time": "14:30",           # 24-hour
    "duration_minutes": 45             # Number
}
```

### Debug Checklist

When integration fails, check:

**Server A (AIOOS)**:
- [ ] Backend running (`http://localhost:8000`)
- [ ] Database connected (Supabase credentials valid)
- [ ] `CALENDAR_API_KEY` set in `.env`
- [ ] Calendar routes registered (`add_calendar_routes()`)
- [ ] Agent exists in `agents` table
- [ ] Business hours configured for agent

**Server B (External)**:
- [ ] Correct base URL
- [ ] Correct API key
- [ ] Valid agent ID (UUID format)
- [ ] Proper date/time formats
- [ ] Network connectivity to Server A
- [ ] Error handling implemented

### Logging

**Server A should log**:
```python
logger.info(f"External booking request from {x_api_key[:8]}...")
logger.info(f"Booking created: {booking_id}")
logger.warning(f"Invalid API key attempt")
logger.error(f"Failed to create booking: {error}")
```

**Server B should log**:
```python
logger.info(f"Querying slots for agent {agent_id}")
logger.info(f"Booking successful: {booking_id}")
logger.error(f"Booking failed: {status_code} - {detail}")
```

---

## Appendix

### Complete Integration Checklist

#### Server A (AIOOS) Setup

- [ ] Database tables created (`calendar_events`, `business_hours`)
- [ ] PostgreSQL functions created (`get_available_slots`, `check_time_slot_available`)
- [ ] Calendar API code added to `calendar_api.py`
- [ ] Routes registered in `main.py` (`add_calendar_routes(app, supabase)`)
- [ ] API key configured in `.env` (`CALENDAR_API_KEY`)
- [ ] Agent created with valid UUID
- [ ] Business hours configured for agent
- [ ] Backend tested locally
- [ ] Endpoints tested with curl/Postman

#### Server B (External) Setup

- [ ] API key received from Server A
- [ ] Agent ID received from Server A
- [ ] Base URL confirmed
- [ ] Client library implemented
- [ ] Date/time formatting correct
- [ ] Error handling implemented
- [ ] Logging implemented
- [ ] Test scenarios passed
- [ ] Production credentials secured

### Quick Start Commands

**Server A**:
```bash
# Setup database
cd v4liveKit/backend
python setup_calendar_table.py

# Start backend
python main.py

# Test endpoint
curl "http://localhost:8000/api/calendar/free-slots/AGENT_ID?start_date=2025-12-01&end_date=2025-12-07" \
  -H "X-API-Key: secret-key-abc123"
```

**Server B**:
```bash
# Install dependencies
pip install requests  # Python
npm install axios     # Node.js

# Test connection
python calendar_client.py
node calendar-client.js
```

### Contact & Support

For integration support:

- **Server A Team**: AIOOS Platform maintainers
- **Documentation**: This file
- **API Version**: 1.0
- **Last Updated**: 2025-11-30

---

**End of Integration Guide**
