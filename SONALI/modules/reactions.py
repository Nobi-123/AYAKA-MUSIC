# SONALI/modules/reactions.py
"""
Automatic reactions module for SONALI.
- Reacts to user messages intelligently
- Sends emojis based on sentiment, keywords, or message type
- Works with stickers too
"""

import random
from pyrogram.types import Message

# --------------------------
# Predefined sticker reactions
# --------------------------
STICKERS = [
    "CAACAgEAAxkBAAEBH4FgxP7JbJ2f7y-3h1O1ikG6RvDsvwACXAADwZxgD7hYxkPY3fLFiQE",
    "CAACAgEAAxkBAAEBH4NgxP7JXmvkb36xV5aRGn7wUgrctwACXQADwZxgD9Y2ztvHJuBvIiQE",
    "CAACAgEAAxkBAAEBH4RgxP7JZxTzUcrrL07v5OZay8lPLwACXgADwZxgD8rrd4Lf7OtUFiQE"
]

# --------------------------
# Emoji reactions based on message content
# --------------------------
EMOJI_REACTIONS = {
    "love": ["❤️", "😍", "😘"],
    "haha": ["😂", "🤣", "😆"],
    "sad": ["😢", "😭", "💔"],
    "hello": ["👋", "🙋‍♀️", "😊"],
    "thanks": ["🙏", "😊", "🤗"],
    "wow": ["😮", "😲", "🤩"],
    "angry": ["😡", "🤬", "😠"], 
    "baby" : ["♥️", "😒"], 
    "sex" : ["🍒", "😘", "🥵"]
}

# Generic filler emojis
GENERIC_REACTIONS = ["😎", "😉", "😅", "😇", "🤔", "👍", "🎶"]

# --------------------------
# React to message function
# --------------------------
async def react_to_message(message: Message):
    """
    Reacts to a message with emojis intelligently.
    """
    text = (message.text or "").lower() if message.text else ""

    # Match emojis based on keywords
    for keyword, emojis in EMOJI_REACTIONS.items():
        if keyword in text:
            await message.reply(random.choice(emojis))
            return

    # 10% chance to react with a generic emoji
    if random.random() < 0.1:
        await message.reply(random.choice(GENERIC_REACTIONS))