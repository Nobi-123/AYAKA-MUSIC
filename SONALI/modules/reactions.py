# SONALI/modules/reactions.py
from pyrogram.types import Message
import random
from .stickers import STICKERS, STICKER_REPLY_MAP

# --- Text triggers for bot replies ---
TEXT_REACTIONS = {
    "hello": "👋 Hey there!",
    "hi": "🙌 Hi!",
    "thanks": "😊 You’re welcome!",
    "good morning": "🌞 Good morning! Have a nice day!",
    "good night": "🌙 Good night! Sweet dreams!",
    "miss you": "Awww 😘 main bhi tumhe miss kar rahi hoon!"
}

# --- Text triggers for sticker replies ---
STICKER_REACTIONS = {
    "good night": "CAACAgIAAxkBAAEBQj9gkqQkN5jB7x5G3-xyz1234"  # Replace with your sticker file_id
}

# --- Emoji reactions based on keywords ---
EMOJI_REACTIONS = {
    "love": ["❤️", "😍", "😘"],
    "happy": ["😄", "😁", "😊"],
    "sad": ["😢", "😭", "😔"],
    "angry": ["😡", "😠", "🤬"],
    "wow": ["😲", "😳", "🤯"]
}

async def react_to_message(message: Message):
    """
    Automatically reacts to human messages or stickers.
    """
    # --- Text reactions ---
    if message.text:
        text_lower = message.text.lower()
        for keyword, reply in TEXT_REACTIONS.items():
            if keyword in text_lower:
                await message.reply_text(reply)
                break

        for keyword, sticker_id in STICKER_REACTIONS.items():
            if keyword in text_lower:
                await message.reply_sticker(sticker_id)
                break

        # --- Emoji reactions ---
        for keyword, emojis in EMOJI_REACTIONS.items():
            if keyword in text_lower:
                emoji = random.choice(emojis)
                await message.reply_text(emoji)
                break

    # --- Sticker-to-sticker replies ---
    if message.sticker:
        received_sticker_id = message.sticker.file_id
        reply_sticker_id = STICKER_REPLY_MAP.get(received_sticker_id)
        if reply_sticker_id:
            await message.reply_sticker(reply_sticker_id)
            return
        # Random sticker reaction (20% chance)
        if random.random() < 0.2:
            await message.reply_sticker(random.choice(STICKERS))