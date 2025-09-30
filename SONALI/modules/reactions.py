# SONALI/modules/reactions.py
"""
Handles automatic reactions and sticker replies based on message content or stickers.
Compatible with RAUSHAN bot.
"""
from pyrogram.types import Message
import random
from .stickers import STICKERS

# Example text triggers: keyword -> reaction text
TEXT_REACTIONS = {
    "hello": "👋 Hey there!",
    "hi": "🙌 Hi!",
    "thanks": "😊 You’re welcome!",
    "good morning": "🌞 Good morning! Have a nice day!",
    "good night": "🌙 Good night! Sweet dreams!",
    "miss you": "Awww 😘 main bhi tumhe miss kar rahi hoon!"
}

# Text -> sticker triggers: keyword -> sticker file_id
STICKER_REACTIONS = {
    "good night": "CAACAgIAAxkBAAEBQj9gkqQkN5jB7x5G3-xyz1234"  # replace with your sticker file_id
}

# Sticker-to-sticker replies: received_sticker_file_id -> reply_sticker_file_id
STICKER_REPLY_MAP = {
    "CAACAgIAAxkBAAEBQkZgkqRR3sB5p2xyzabc": "CAACAgIAAxkBAAEBQl1gkqU0mD5rxyz123"  # Example mapping
}

async def react_to_message(message: Message):
    """
    Automatically reacts to text or stickers.
    """
    # --- Text reactions ---
    if message.text:
        text_lower = message.text.lower()
        for keyword, reply in TEXT_REACTIONS.items():
            if keyword in text_lower:
                await message.reply_text(reply)
                return

        for keyword, sticker_id in STICKER_REACTIONS.items():
            if keyword in text_lower:
                await message.reply_sticker(sticker_id)
                return

    # --- Sticker-to-sticker replies ---
    if message.sticker:
        received_sticker_id = message.sticker.file_id
        reply_sticker_id = STICKER_REPLY_MAP.get(received_sticker_id)
        if reply_sticker_id:
            await message.reply_sticker(reply_sticker_id)
            return

    # --- Random sticker reply (optional fun) ---
    if message.sticker and random.random() < 0.2:  # 20% chance
        await message.reply_sticker(random.choice(STICKERS))
