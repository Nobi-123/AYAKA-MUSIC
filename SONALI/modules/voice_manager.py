# SONALI/modules/voice_manager.py
import logging
from elevenlabs.client import AsyncElevenLabs
import config

logger = logging.getLogger(__name__)

async def text_to_voice(text: str) -> bytes | None:
    """
    Converts text to voice using ElevenLabs with API key rotation.
    Returns audio bytes if successful, else None.
    """
    if not config.ELEVENLABS_API_KEYS:
        logger.warning("ELEVENLABS_API_KEYS not configured. Skipping voice generation.")
        return None

    for attempt in range(len(config.ELEVENLABS_API_KEYS)):
        try:
            current_key = config.ELEVENLABS_API_KEYS[config.current_eleven_key_index]
            logger.info(f"Attempting ElevenLabs call with key index: {config.current_eleven_key_index}")

            client = AsyncElevenLabs(api_key=current_key)
            audio_stream = client.text_to_speech.convert(
                voice_id=config.ELEVENLABS_VOICE_ID,
                model_id="eleven_v3",
                text=text,
                output_format="mp3_44100_128",
            )

            audio_bytes = b""
            async for chunk in audio_stream:
                audio_bytes += chunk

            if not audio_bytes:
                raise ValueError("Received empty audio stream from ElevenLabs.")

            logger.info(f"Voice generated successfully for text: '{text[:30]}...'")
            return audio_bytes

        except Exception as e:
            logger.warning(f"API key index {config.current_eleven_key_index} failed ({type(e).__name__}: {e}). Rotating key.")
            config.current_eleven_key_index = (config.current_eleven_key_index + 1) % len(config.ELEVENLABS_API_KEYS)

    logger.critical("All ElevenLabs API keys exhausted or failing.")
    return None