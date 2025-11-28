"""
AIOOS Platform - FastAPI Backend Server
High-quality voice AI platform ba LiveKit + Azure/OpenAI/Deepgram
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from livekit import api
from supabase import create_client, Client
from supabase.lib.client_options import SyncClientOptions
from calendar_api import add_calendar_routes
from knowledge_api import add_knowledge_routes
from ai_summary import generate_call_summary
from livekit_service import LiveKitService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aioos-backend")

# Initialize FastAPI
app = FastAPI(
    title="AIOOS Voice AI Platform",
    description="Professional voice AI platform powered by LiveKit, Azure, OpenAI, and Deepgram",
    version="1.0.0"
)

# CORS configuration - bara Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LiveKit Service
livekit_service = LiveKitService()

# Supabase configuration
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL") or os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("VITE_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY", "")

# Initialize Supabase client
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized")
        logger.info(f"📍 Supabase URL: {SUPABASE_URL}")
    except Exception as e:
        logger.error(f"❌ Supabase initialization failed: {e}")
        supabase = None
else:
    logger.warning("⚠️  Supabase credentials not found. Database features disabled.")

# Register calendar API routes
if supabase:
    add_calendar_routes(app, supabase)
    logger.info("✅ Calendar API routes registered")
else:
    logger.warning("⚠️  Calendar API routes not registered (Supabase not available)")

# Register knowledge base API routes
if supabase:
    add_knowledge_routes(app, supabase)
    logger.info("✅ Knowledge Base API routes registered")
else:
    logger.warning("⚠️  Knowledge Base API routes not registered (Supabase not available)")


# ==================== Pydantic Models ====================

class AgentConfig(BaseModel):
    """Agent configuration model"""
    name: str
    description: Optional[str] = None
    language: str = "en-US"
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    system_instructions: Optional[str] = None

    # TTS/STT provider - ba default Azure (cheap and quality!)
    tts_provider: str = "azure"  # azure, openai, deepgram
    tts_voice: str = "en-US-JennyNeural"  # Azure voice
    stt_provider: str = "azure"  # azure, deepgram

    # Business logic
    status: str = "active"  # active, inactive
    tags: Optional[List[str]] = None


class AgentTestRequest(BaseModel):
    """Request model bara test kardane agent"""
    user_identity: str = "test-user"
    metadata: Optional[Dict] = None


class CreateRoomRequest(BaseModel):
    """Request model bara sakhtane room"""
    room_name: Optional[str] = None
    participant_identity: str
    agent_id: Optional[str] = None
    metadata: Optional[Dict] = None


# ==================== Helper Functions ====================

def get_authenticated_supabase_client(authorization: Optional[str] = None) -> Client:
    """
    Get Supabase client authenticated with user JWT token
    Age authorization header nadare, ba ANON_KEY kar mikone
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(status_code=503, detail="Supabase not configured")

    # Age JWT token darim, authenticated client besaz
    if authorization and authorization.startswith("Bearer "):
        access_token = authorization.replace("Bearer ", "")
        # Create authenticated Supabase client ba user JWT
        options = SyncClientOptions(
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        return create_client(SUPABASE_URL, SUPABASE_KEY, options=options)

    # Default: ba ANON_KEY (bara public endpoints)
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# Helper functions moved to livekit_service.py and utils.py


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "AIOOS Voice AI Platform",
        "version": "1.0.0",
        "status": "running",
        "message": "Salam! Backend server successfully running ✅"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "livekit": "configured" if livekit_service.api_key else "not_configured",
            "supabase": "connected" if supabase else "not_configured"
        }
    }


@app.get("/api/agents")
async def get_agents(authorization: Optional[str] = Header(None)):
    """
    Get list of agents for authenticated user
    RLS policy automatically filters by user_id from JWT
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        # Get authenticated Supabase client ba user JWT
        # RLS policies will automatically filter agents by user_id
        auth_supabase = get_authenticated_supabase_client(authorization)

        response = auth_supabase.table("agents").select("*").order("created_at", desc=True).execute()
        agents = response.data

        logger.info(f"✅ Fetched {len(agents)} agents from database")
        return agents

    except Exception as e:
        logger.error(f"❌ Failed to fetch agents: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/agents/{agent_id}")
async def get_agent_by_id(agent_id: str, authorization: Optional[str] = Header(None)):
    """
    Get agent by ID from Supabase
    RLS policy ensures user can only see their own agents
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        # Get authenticated Supabase client ba user JWT
        # RLS policies will automatically filter agents by user_id
        auth_supabase = get_authenticated_supabase_client(authorization)

        response = auth_supabase.table("agents").select("*").eq("id", agent_id).execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

        agent = response.data[0]
        logger.info(f"✅ Fetched agent: {agent['name']}")
        return agent

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to fetch agent {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/agents")
async def create_agent(agent: AgentConfig, authorization: Optional[str] = Header(None)):
    """
    Create new agent and save to Supabase
    User must be authenticated - JWT token auto-sets user_id via database trigger
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        # Get authenticated Supabase client ba user JWT
        # This allows database trigger to auto-set user_id from auth.uid()
        auth_supabase = get_authenticated_supabase_client(authorization)

        # Prepare agent data (WITHOUT user_id - trigger will set it automatically)
        agent_data = {
            "name": agent.name,
            "description": agent.description,
            "language": agent.language,
            "tts_provider": agent.tts_provider,
            "tts_voice": agent.tts_voice,
            "stt_provider": agent.stt_provider,
            "stt_language": agent.language,  # Use same as agent language
            "llm_model": agent.llm_model,
            "llm_temperature": agent.temperature,
            "system_instructions": agent.system_instructions,
            "status": agent.status,
            "tags": agent.tags or []
        }

        # Insert into Supabase ba authenticated client
        # Database trigger will automatically set user_id from JWT (auth.uid())
        response = auth_supabase.table("agents").insert(agent_data).execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=500, detail="Failed to create agent")

        created_agent = response.data[0]
        logger.info(f"✅ Created agent: {created_agent['name']} (ID: {created_agent['id']})")

        return created_agent

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to create agent: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/agents/{agent_id}/test")
async def test_agent(agent_id: str, request: AgentTestRequest):
    """
    Create test session bara agent
    This creates a LiveKit room with agent_id in metadata
    The persistent worker will pick this up automatically
    """
    try:
        # Generate unique room name
        room_name = f"test-{agent_id}-{datetime.utcnow().timestamp()}"

        logger.info(f"🎤 Creating test session for agent {agent_id}")
        logger.info(f"📍 Room name: {room_name}")

        # Create room with metadata so worker knows which agent to use
        import json
        metadata = json.dumps({
            "agent_id": agent_id,
            "type": "test_session"
        })
        
        await livekit_service.create_room(room_name, metadata=metadata)

        # Create LiveKit access token bara user
        token = await livekit_service.create_token(room_name, request.user_identity)

        logger.info(f"✅ Test session created successfully")

        return {
            "status": "success",
            "room_name": room_name,
            "agent_id": agent_id,
            "livekit_url": livekit_service.url,
            "token": token,
            "participant_identity": request.user_identity,
            "message": "Test session ready! Connect to LiveKit room."
        }

    except Exception as e:
        logger.error(f"❌ Failed to create test session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rooms/create")
async def create_room(request: CreateRoomRequest):
    """
    Create LiveKit room with agent
    """
    try:
        room_name = request.room_name or f"room-{datetime.utcnow().timestamp()}"
        
        # Prepare metadata if agent_id is provided
        metadata = None
        if request.agent_id:
            import json
            metadata = json.dumps({
                "agent_id": request.agent_id,
                "type": "standard_room"
            })
            
        # Create room explicitly to set metadata
        await livekit_service.create_room(room_name, metadata=metadata)

        # Create token bara participant
        token = await livekit_service.create_token(room_name, request.participant_identity)

        return {
            "status": "success",
            "room_name": room_name,
            "livekit_url": livekit_service.url,
            "token": token,
            "participant_identity": request.participant_identity
        }

    except Exception as e:
        logger.error(f"❌ Failed to create room: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_platform_stats():
    """
    Get platform statistics from Supabase
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        # Call the stored function to get platform stats
        response = supabase.rpc("get_platform_stats").execute()

        if response.data and len(response.data) > 0:
            stats = response.data[0]
            logger.info("✅ Fetched platform statistics")
            return stats
        else:
            # Return defaults if no data
            return {
                "total_agents": 0,
                "active_agents": 0,
                "total_calls_today": 0,
                "total_calls_all_time": 0,
                "total_minutes_today": 0,
                "avg_call_duration_seconds": 0,
                "active_calls": 0
            }

    except Exception as e:
        logger.error(f"❌ Failed to fetch platform stats: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/analytics/summary")
async def get_analytics_summary(
    range: str = "30d", 
    authorization: Optional[str] = Header(None)
):
    """
    Get analytics summary (calls, duration, cost, etc.)
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)
        
        # Calculate start date based on range
        now = datetime.utcnow()
        if range == "7d":
            start_date = now - timedelta(days=7)
        elif range == "90d":
            start_date = now - timedelta(days=90)
        else: # Default 30d
            start_date = now - timedelta(days=30)
            
        response = auth_supabase.rpc("get_analytics_summary", {
            "p_start_date": start_date.isoformat(),
            "p_end_date": now.isoformat()
        }).execute()
        
        if response.data:
            return response.data
        return {}
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch analytics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/chart")
async def get_analytics_chart(
    period: str = "daily",
    authorization: Optional[str] = Header(None)
):
    """
    Get chart data for analytics
    - daily: Hourly data for last 24 hours (intraday)
    - weekly: Daily data for last 7 days
    - monthly: Daily data for last 30 days
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)

        # Daily = Hourly (24h), Weekly = 7 days, Monthly = 30 days
        if period == "daily":
            # Hourly data for intraday chart
            response = auth_supabase.rpc("get_hourly_call_volume", {
                "p_hours": 24
            }).execute()
        elif period == "weekly":
            # Daily data for 7 days
            response = auth_supabase.rpc("get_daily_call_volume", {
                "p_days": 7
            }).execute()
        else:  # monthly
            # Daily data for 30 days
            response = auth_supabase.rpc("get_daily_call_volume", {
                "p_days": 30
            }).execute()

        return response.data or []

    except Exception as e:
        logger.error(f"❌ Failed to fetch analytics chart: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/top-agents")
async def get_top_agents(authorization: Optional[str] = Header(None)):
    """
    Get top agents by call volume
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)
        
        response = auth_supabase.rpc("get_top_agents_analytics", {
            "p_limit": 5
        }).execute()
        
        return response.data or []
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch top agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Call Logs Endpoints ====================

@app.get("/api/calls")
async def get_calls(
    agent_id: Optional[str] = None,
    department: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    duration_filter: Optional[str] = None,  # short, medium, long
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    authorization: Optional[str] = Header(None)
):
    """
    Get call logs with filters and pagination
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)

        # Start query
        query = auth_supabase.table("call_logs").select("*")

        # Apply filters
        if agent_id:
            query = query.eq("agent_id", agent_id)

        if department:
            # Department filter - need to join with agents table or use RLS
            pass  # Will implement after adding department field

        if date_from:
            query = query.gte("start_time", date_from)

        if date_to:
            query = query.lte("start_time", date_to)

        if status:
            # Map frontend status to database status
            status_map = {
                "completed": "completed",
                "transferred": "completed",  # Can add transfer field later
                "hung_up": "completed",
                "error": "failed"
            }
            db_status = status_map.get(status.lower(), status)
            query = query.eq("status", db_status)

        if duration_filter:
            # Duration filters
            if duration_filter == "short":
                query = query.lt("duration_seconds", 60)
            elif duration_filter == "medium":
                query = query.gte("duration_seconds", 60).lte("duration_seconds", 300)
            elif duration_filter == "long":
                query = query.gt("duration_seconds", 300)

        if search:
            # Search in room_name
            query = query.ilike("room_name", f"%{search}%")

        # Order by start_time descending (newest first)
        query = query.order("start_time", desc=True)

        # Get total count for pagination
        count_query = auth_supabase.table("call_logs").select("id", count="exact")
        if agent_id:
            count_query = count_query.eq("agent_id", agent_id)
        count_response = count_query.execute()
        total_count = count_response.count or 0

        # Apply pagination
        query = query.range(offset, offset + limit - 1)

        response = query.execute()

        # Format response
        calls = []
        for call in response.data:
            # Format duration as MM:SS
            duration_seconds = call.get("duration_seconds", 0) or 0
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            duration_formatted = f"{minutes:02d}:{seconds:02d}"

            # Format start time
            start_time = call.get("start_time", "")
            if start_time:
                from datetime import datetime
                dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                start_time_formatted = dt.strftime("%b %d, %Y, %I:%M %p")
            else:
                start_time_formatted = ""

            # Get agent name (will need to join in future)
            agent_name = "Unknown"
            if call.get("agent_id"):
                try:
                    agent_response = auth_supabase.table("agents").select("name").eq("id", call["agent_id"]).execute()
                    if agent_response.data:
                        agent_name = agent_response.data[0]["name"]
                except:
                    pass

            calls.append({
                "id": call["id"],
                "callerId": call.get("room_name", "Unknown"),
                "agent": agent_name,
                "department": "Support",  # TODO: Add department field
                "startTime": start_time_formatted,
                "duration": duration_formatted,
                "outcome": call.get("status", "unknown").title(),
                "raw": call  # Include raw data for debugging
            })

        return {
            "calls": calls,
            "total": total_count,
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        logger.error(f"❌ Failed to fetch calls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calls/{call_id}")
async def get_call_by_id(
    call_id: str,
    authorization: Optional[str] = Header(None)
):
    """
    Get individual call details
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)

        response = auth_supabase.table("call_logs").select("*").eq("id", call_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Call not found")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to fetch call {call_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/calls/{call_id}/generate-summary")
async def generate_summary_for_call(
    call_id: str,
    authorization: Optional[str] = Header(None)
):
    """
    Generate or regenerate AI summary for a call
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)

        # Get call data
        response = auth_supabase.table("call_logs").select("*").eq("id", call_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Call not found")

        call_data = response.data[0]

        # Check if transcript exists
        transcript_json = call_data.get("transcript_json")
        if not transcript_json or not isinstance(transcript_json, list):
            raise HTTPException(status_code=400, detail="No transcript available for this call")

        # Detect language (default: German)
        language = "de"  # Could be detected from agent settings

        # Generate summary
        logger.info(f"🤖 Generating AI summary for call {call_id}...")
        summary_data = await generate_call_summary(transcript_json, language=language)

        # Update database
        update_response = auth_supabase.table("call_logs").update({
            "summary": summary_data.get("summary", ""),
            "summary_json": summary_data
        }).eq("id", call_id).execute()

        logger.info(f"✅ AI Summary generated for call {call_id}")

        return {
            "success": True,
            "call_id": call_id,
            "summary": summary_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to generate summary for call {call_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calls/export")
async def export_calls(
    agent_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    """
    Export call logs as CSV
    """
    if not supabase:
        raise HTTPException(status_code=503, detail="Database not configured")

    try:
        auth_supabase = get_authenticated_supabase_client(authorization)

        # Get all calls with filters (no pagination)
        query = auth_supabase.table("call_logs").select("*")

        if agent_id:
            query = query.eq("agent_id", agent_id)
        if date_from:
            query = query.gte("start_time", date_from)
        if date_to:
            query = query.lte("start_time", date_to)

        query = query.order("start_time", desc=True)
        response = query.execute()

        # Generate CSV
        import io
        import csv

        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["Call ID", "Room Name", "Agent ID", "Start Time", "End Time", "Duration (seconds)", "Status", "Cost"])

        # Write data
        for call in response.data:
            writer.writerow([
                call.get("id", ""),
                call.get("room_name", ""),
                call.get("agent_id", ""),
                call.get("start_time", ""),
                call.get("end_time", ""),
                call.get("duration_seconds", 0),
                call.get("status", ""),
                call.get("cost", 0)
            ])

        csv_content = output.getvalue()
        output.close()

        from fastapi.responses import Response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=call_logs_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )

    except Exception as e:
        logger.error(f"❌ Failed to export calls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Run Server ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
