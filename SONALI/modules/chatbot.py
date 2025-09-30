# SONALI/modules/chatbot.py
import logging
from typing import Optional, Tuple
from . import config
from .voice_manager import text_to_voice
import httpx

logger = logging.getLogger(__name__)

SAMBA_API_URL = "https://api.sambanova.ai/v1/chat"

OWNER_USERNAME = "@OfcAlwaysOg"
OWNER_KEYWORDS = [
    "owner", "developer", "father", "papa",
    "who is your owner", "who is your developer",
    "who is your papa", "who is your father"
]

VOICE_REQUEST_KEYWORDS = [
    "ye msg mujhe voice msg mai bhejo",
    "send this in voice",
    "voice me bhejo"
]

chatbot_enabled = {}
last_bot_message = {}

FLIRTY_REPLIES = [
    "Awww 😘 tumne mujhe miss kiya?",
    "Hahaha 😄 tumhare jokes mujhe pasand aaye!",
    "Oh really? 😏 batao aur...",
    "Mujhe tumhari baatein sunke accha lagta hai 😍",
    "Tum itne cute kaise ho? 😋",
    "Hahaha, tum toh naughty ho 😜",
    "Main hamesha tumhare sath hoon 😇",
    "Hmm… interesting 😏 aur batao",
    "Awww 😘 dil khush kar diya tumne",
]

def playful_reply(text: str) -> str:
    lower = text.lower()
    if any(greet in lower for greet in ["hello", "hi", "hey", "hii"]):
        return "Heyy 😘 kaise ho?"
    if "good morning" in lower:
        return "Good morning sunshine ☀️😍"
    if "good night" in lower:
        return "Good night 😴 sweet dreams ❤️"
    if "miss you" in lower:
        return "Awww 😘 main bhi tumhe miss kar rahi hoon!"
    if "love" in lower:
        return "Awww 😍 tum toh mujhe bahut pasand ho!"
    return FLIRTY_REPLIES[int.from_bytes(text.encode(), "little") % len(FLIRTY_REPLIES)]

async def get_sambanova_response(prompt: str, user_id: int, language="hinglish") -> str:
    if any(keyword in prompt.lower() for keyword in OWNER_KEYWORDS):
        return f"My owner is {OWNER_USERNAME}"

    headers = {
        "Authorization": f"Bearer {config.SAMBANOVA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "input_text": prompt,
        "user_id": str(user_id),
        "language": language
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(SAMBA_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "output_text" in data:
                return data["output_text"]
    except Exception as e:
        logger.error(f"SambaNova API error: {e}")

    return playful_reply(prompt)

async def chat_and_respond(chat_id: int, user_text: str, user_id: int, send_voice=True) -> Tuple[str, Optional[bytes]]:
    if chatbot_enabled.get(chat_id) is False:
        return "Chatbot is disabled in this chat.", None

    if any(k in user_text.lower() for k in VOICE_REQUEST_KEYWORDS):
        last_text = last_bot_message.get(chat_id)
        if last_text:
            audio_bytes = await text_to_voice(last_text)
            return "Here's your message in voice 😘", audio_bytes
        else:
            return "No previous message to convert to voice 😅", None

    bot_text = await get_sambanova_response(user_text, user_id, language="hinglish")
    last_bot_message[chat_id] = bot_text
    audio_bytes = None
    if send_voice and OWNER_USERNAME not in bot_text:
        audio_bytes = await text_to_voice(bot_text)

    return bot_text, audio_bytes