# SONALI/modules/voice_manager.py
import logging
import asyncio
import random
from elevenlabs.client import AsyncElevenLabs
import config

logger = logging.getLogger(__name__)

# Your voice ID (rename as you like)
VOICE_ID = config.ELEVENLABS_VOICE_ID

async def text_to_voice(text: str) -> bytes | None:
    """
    Converts text to voice using ElevenLabs API, adding human-like pauses.
    Returns audio bytes.
    """
    if not config.ELEVENLABS_API_KEYS:
        logger.warning("ELEVENLABS_API_KEYS not configured. Skipping voice generation.")
        return None

    # Introduce small random human-like pauses in text
    def add_pauses(text):
        # Split sentences and insert short pauses
        sentences = text.split(".")
        new_text = ""
        for s in sentences:
            s = s.strip()
            if not s:
                continue
            new_text += s
            # Randomly add comma pause
            if random.random() < 0.5:
                new_text += ","
            new_text += ". "
        return new_text.strip()

    processed_text = add_pauses(text)

    for attempt in range(len(config.ELEVENLABS_API_KEYS)):
        try:
            current_key = config.ELEVENLABS_API_KEYS[config.current_eleven_key_index]
            logger.info(f"Attempting ElevenLabs call with key index: {config.current_eleven_key_index}")

            eleven_client = AsyncElevenLabs(api_key=current_key)
            audio_stream = eleven_client.text_to_speech.convert(
                voice_id=VOICE_ID,
                model_id="eleven_v3",
                text=processed_text,
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
                f"ElevenLabs API Key at index {config.current_eleven_key_index} failed ({type(e).__name__}: {e}). Rotating to the next key."
            )
            config.current_eleven_key_index = (config.current_eleven_key_index + 1) % len(config.ELEVENLABS_API_KEYS)

    logger.critical("All ElevenLabs API keys have been exhausted or are failing.")
    return None