# SONALI/modules/chatbot.py
"""
Human-like SambaNova chatbot for SONALI.
Features:
- Casual Hinglish replies
- Emojis, filler words, slang
- Voice replies via ElevenLabs
- Owner / developer tagging
"""

import logging
import aiohttp
import random
from modules.voice_manager import text_to_voice
import config

logger = logging.getLogger(__name__)

# --------------------------
# Owner / Developer Keywords
# --------------------------
OWNER_KEYWORDS = [
    "owner", "developer", "father", "papa",
    "tere owner ka naam kya hai", "tera owner kaun hai",
    "owner ka naam kya hai", "apka owner kaun hai",
    "developer ka naam kya hai", "apka developer kaun hai",
    "papa ka naam kya hai", "father ka naam kya hai",
    "who is your owner", "who is your developer",
    "who is your papa", "who is your father"
]

# --------------------------
# Voice request keywords
# --------------------------
VOICE_REQUEST_KEYWORDS = [
    "ye msg mujhe voice msg mai bhejo",
    "send this in voice",
    "voice me bhejo"
    "Voice"
    "bolo"
    "baby"
    "listen"
    "baby suno"
]

# --------------------------
# Track last bot message per chat
# --------------------------
last_bot_message = {}

# --------------------------
# SambaNova API call
# --------------------------
async def samba_chat_reply(user_text: str, chat_id: int) -> str:
    """
    Sends user message to SambaNova API and returns a casual Hinglish reply.
    """
    url = config.CHATBOT_API_URL
    headers = {
        "Authorization": f"Bearer {config.CHATBOT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"input": user_text, "chat_id": str(chat_id)}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=30) as resp:
                data = await resp.json()
                reply = data.get("output") or "Hmm, mujhe samajh nahi aaya 😅"

                # --------------------------
                # Add casual Hinglish flair
                # --------------------------
                fillers = ["😂", "😅", "hmm…", "accha…", "sahi hai…", "arey waah…", "lol", "yeh toh sahi hai 😎"]
                slangs = ["bhai", "yaar", "arre", "hai na", "kya bolti public 😜"]

                # Randomly add fillers
                if random.random() < 0.5:
                    reply += " " + random.choice(fillers)

                # Randomly add slangs
                if random.random() < 0.3:
                    reply = random.choice(slangs) + ", " + reply

                # Add human hesitation
                if random.random() < 0.2:
                    reply = "Hmm… " + reply

                return reply
    except Exception as e:
        logger.error(f"SambaNova API failed: {e}")
        return "Sorry yaar, abhi main reply nahi kar sakti 😢"

# --------------------------
# Main chatbot handler
# --------------------------
async def chat_and_respond(chat_id: int, user_text: str, user_id: int):
    """
    Generate chatbot reply, voice, and store last message.
    """
    # Owner keywords
    if any(keyword in user_text.lower() for keyword in OWNER_KEYWORDS):
        reply_text = f"Mera owner hai {config.OWNER_USERNAME} ❤️"
        audio_bytes = await text_to_voice(reply_text)
        last_bot_message[chat_id] = reply_text
        return reply_text, audio_bytes

    # Chatbot reply
    bot_text = await samba_chat_reply(user_text, chat_id)
    audio_bytes = await text_to_voice(bot_text)

    # Save last bot message
    last_bot_message[chat_id] = bot_text
    return bot_text, audio_bytes

# --------------------------
# Voice request handler
# --------------------------
async def handle_voice_request(chat_id: int, user_text: str):
    """
    Return audio for last bot message if user asks for voice.
    """
    if any(k.lower() in user_text.lower() for k in VOICE_REQUEST_KEYWORDS):
        last_text = last_bot_message.get(chat_id)
        if last_text:
            audio_bytes = await text_to_voice(last_text)
            return audio_bytes
    return None