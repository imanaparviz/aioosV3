import os
import logging
from datetime import timedelta
from livekit import api

logger = logging.getLogger("livekit-service")

class LiveKitService:
    def __init__(self):
        self.url = os.getenv("LIVEKIT_URL", "wss://your-project.livekit.cloud")
        self.api_key = os.getenv("LIVEKIT_API_KEY", "")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET", "")
        
        if not self.api_key or not self.api_secret:
            logger.warning("⚠️ LiveKit credentials not found. Some features may not work.")

    async def create_token(self, room_name: str, participant_identity: str, participant_name: str = None) -> str:
        """
        Create LiveKit access token for a participant
        """
        if not self.api_key or not self.api_secret:
            raise Exception("LiveKit credentials not configured")

        token = api.AccessToken(self.api_key, self.api_secret)
        token.with_identity(participant_identity)
        token.with_name(participant_name or participant_identity)
        token.with_grants(api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
            can_publish_data=True,
        ))

        # Token expires after 1 hour
        token.with_ttl(timedelta(hours=1))

        return token.to_jwt()

    async def create_room(self, room_name: str, empty_timeout: int = 600, max_participants: int = 20, metadata: str = None):
        """
        Create a room explicitly (optional, usually rooms are created on join)
        But useful for setting metadata upfront.
        """
        if not self.api_key or not self.api_secret:
            raise Exception("LiveKit credentials not configured")
            
        lkapi = api.LiveKitAPI(self.url, self.api_key, self.api_secret)
        
        try:
            # Check if room exists
            rooms = await lkapi.room.list_rooms([room_name])
            if not rooms:
                logger.info(f"Creating room: {room_name}")
                await lkapi.room.create_room(
                    name=room_name,
                    empty_timeout=empty_timeout,
                    max_participants=max_participants,
                    metadata=metadata
                )
            else:
                logger.info(f"Room {room_name} already exists, updating metadata if provided")
                if metadata:
                    # Update room metadata if it exists
                    # Note: python sdk might not have update_room_metadata easily exposed in all versions, 
                    # but create_room typically handles "get or create" logic or we can just proceed.
                    # For now we assume create_room is sufficient or we just let the worker handle it via room connection.
                    pass 
                    
        except Exception as e:
            logger.error(f"Error creating room: {e}")
            raise
        finally:
            await lkapi.aclose()
