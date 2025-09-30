# SONALI/modules/voice_manager.py
"""
Manages ElevenLabs Text-to-Speech API calls with API key rotation.
"""

import logging
from elevenlabs.client import AsyncElevenLabs
from . import config

logger = logging.getLogger(__name__)

# --------------------------
# Replace this with your preferred voice ID
# You can set it in config or directly here
# --------------------------
BOT_VOICE_ID = config.ELEVENLABS_VOICE_ID or "YourDefaultVoiceID"

async def text_to_voice(text: str) -> bytes | None:
    """
    Converts text to voice using ElevenLabs with API key rotation.

    Args:
        text (str): Text to convert.

    Returns:
        bytes | None: Audio bytes if successful, otherwise None.
    """
    if not config.ELEVENLABS_API_KEYS:
        logger.warning("ELEVENLABS_API_KEYS not configured. Skipping voice generation.")
        return None

    for attempt in range(len(config.ELEVENLABS_API_KEYS)):
        try:
            current_key = config.ELEVENLABS_API_KEYS[config.current_eleven_key_index]
            logger.info(f"Attempting ElevenLabs call with key index: {config.current_eleven_key_index}")

            eleven_client = AsyncElevenLabs(api_key=current_key)
            audio_stream = eleven_client.text_to_speech.convert(
                voice_id=BOT_VOICE_ID,
                model_id="eleven_v3",
                text=text,
                output_format="mp3_44100_128",
            )

            audio_bytes = b""
            async for chunk in audio_stream:
                audio_bytes += chunk

            if not audio_bytes:
                raise ValueError("Received empty audio stream from ElevenLabs.")

            logger.info(f"Successfully generated voice for text: '{text[:30]}...'")
            return audio_bytes

        except Exception as e:
            logger.warning(
                f"ElevenLabs API Key at index {config.current_eleven_key_index} failed "
                f"({type(e).__name__}: {e}). Rotating to the next key."
            )
            config.current_eleven_key_index = (config.current_eleven_key_index + 1) % len(config.ELEVENLABS_API_KEYS)

    logger.critical("All ElevenLabs API keys have been exhausted or are failing.")
    return None