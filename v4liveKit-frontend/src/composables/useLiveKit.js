import { ref, onUnmounted } from 'vue'
import { Room, RoomEvent, createLocalAudioTrack } from 'livekit-client'

export function useLiveKit() {
    const room = ref(null)
    const isConnected = ref(false)
    const isConnecting = ref(false)
    const error = ref(null)
    const remoteAudioTracks = ref([])
    const localAudioTrack = ref(null)

    const connect = async (url, token, options = {}) => {
        isConnecting.value = true
        error.value = null

        try {
            // Initialize room
            room.value = new Room(options)

            // Set up event listeners
            setupRoomListeners()

            // Connect
            await room.value.connect(url, token)

            // Handle local microphone
            await enableMicrophone()

        } catch (err) {
            console.error('Failed to connect to LiveKit:', err)
            error.value = err.message || 'Failed to connect'
            isConnecting.value = false
            isConnected.value = false
        }
    }

    const disconnect = async () => {
        if (room.value) {
            await room.value.disconnect()
        }
        room.value = null
        isConnected.value = false
        isConnecting.value = false
        remoteAudioTracks.value = []
        localAudioTrack.value = null
    }

    const enableMicrophone = async () => {
        try {
            // Create local audio track
            const track = await createLocalAudioTrack({
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true,
            })

            if (room.value) {
                await room.value.localParticipant.publishTrack(track)
                localAudioTrack.value = track
            }
        } catch (err) {
            console.error('Failed to enable microphone:', err)
            error.value = `Microphone error: ${err.message}`
            // We don't disconnect here, just report error
        }
    }

    const setupRoomListeners = () => {
        if (!room.value) return

        room.value.on(RoomEvent.Connected, () => {
            console.log('✅ Connected to LiveKit room')
            isConnected.value = true
            isConnecting.value = false
        })

        room.value.on(RoomEvent.Disconnected, (reason) => {
            console.log('❌ Disconnected from LiveKit room:', reason)
            isConnected.value = false
            isConnecting.value = false
            remoteAudioTracks.value = []
        })

        room.value.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
            if (track.kind === 'audio') {
                console.log('🔊 Audio track subscribed:', participant.identity)
                remoteAudioTracks.value.push({
                    sid: track.sid,
                    track: track,
                    participantIdentity: participant.identity
                })
            }
        })

        room.value.on(RoomEvent.TrackUnsubscribed, (track) => {
            if (track.kind === 'audio') {
                remoteAudioTracks.value = remoteAudioTracks.value.filter(t => t.sid !== track.sid)
            }
        })

        room.value.on(RoomEvent.MediaDevicesError, (err) => {
            console.error('Media Device Error', err)
            error.value = 'Media Device Error: ' + err.message
        })
    }

    // Cleanup on unmount
    onUnmounted(() => {
        disconnect()
    })

    return {
        room,
        isConnected,
        isConnecting,
        error,
        remoteAudioTracks,
        connect,
        disconnect
    }
}
