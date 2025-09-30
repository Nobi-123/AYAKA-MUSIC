# SONALI/modules/voice_manager.py
import logging
from elevenlabs.client import AsyncElevenLabs
from .. import config  # ✅ correct import

logger = logging.getLogger(__name__)
MY_VOICE_ID = "YourVoiceIDHere"

async def text_to_voice(text: str) -> bytes | None:
    if not config.ELEVENLABS_API_KEYS:
        logger.warning("ELEVENLABS_API_KEYS not configured.")
        return None

    for attempt in range(len(config.ELEVENLABS_API_KEYS)):
        try:
            key = config.ELEVENLABS_API_KEYS[config.current_eleven_key_index]
            client = AsyncElevenLabs(api_key=key)
            audio_stream = client.text_to_speech.convert(
                voice_id=MY_VOICE_ID,
                model_id="eleven_v3",
                text=text,
                output_format="mp3_44100_128",
            )
            audio_bytes = b""
            async for chunk in audio_stream:
                audio_bytes += chunk
            if audio_bytes:
                return audio_bytes
        except Exception as e:
            config.current_eleven_key_index = (config.current_eleven_key_index + 1) % len(config.ELEVENLABS_API_KEYS)
            continue
    return None