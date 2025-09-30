# SONALI/modules/stickers.py
"""
Context-aware sticker replies for SONALI.
- Sends stickers based on message content or mood
- Works with text messages and automatic reactions
"""

import random

# --------------------------
# Sticker Pools
# --------------------------
HAPPY_STICKERS = [
    "CAACAgEAAxkBAAEBH4FgxP7JbJ2f7y-3h1O1ikG6RvDsvwACXAADwZxgD7hYxkPY3fLFiQE",
    "CAACAgEAAxkBAAEBH4NgxP7JXmvkb36xV5aRGn7wUgrctwACXQADwZxgD9Y2ztvHJuBvIiQE",
]

SAD_STICKERS = [
    "CAACAgEAAxkBAAEBH4RgxP7JZxTzUcrrL07v5OZay8lPLwACXgADwZxgD8rrd4Lf7OtUFiQE",
    "CAACAgEAAxkBAAEBH4VgxP7JeBfcGf1yxCtqP87nnHsz9QACXwADwZxgD9pQOyHzR7N5FiQE",
]

LOVE_STICKERS = [
    "CAACAgEAAxkBAAEBH4ZgxP7Jj_6pO4hJ-F4uU7v0bZ_tLgACYAADwZxgD2r7uFjTEm6qFiQE",
    "CAACAgEAAxkBAAEBH4dgxP7Jd-RV1lItpCFjkK8wYuU7HwACXAADwZxgD8-9vJ_sF4OFIiQE",
]

SURPRISE_STICKERS = [
    "CAACAgEAAxkBAAEBH4fgxP7JeHfI5OXp2lQhAGfDRcJGRQACXQADwZxgD3qq3GJ_w2RWiQE",
]

GENERIC_STICKERS = HAPPY_STICKERS + SAD_STICKERS + LOVE_STICKERS + SURPRISE_STICKERS

# --------------------------
# Sticker reply function
# --------------------------
def get_context_sticker(message_text: str) -> str:
    """
    Returns a sticker ID based on message content.
    """
    text = message_text.lower()

    if any(word in text for word in ["love", "like", "pyaar", "cute"]):
        return random.choice(LOVE_STICKERS)
    elif any(word in text for word in ["happy", "yay", "awesome", "fun"]):
        return random.choice(HAPPY_STICKERS)
    elif any(word in text for word in ["sad", "cry", "miss", "alone"]):
        return random.choice(SAD_STICKERS)
    elif any(word in text for word in ["wow", "surprise", "shock", "oh"]):
        return random.choice(SURPRISE_STICKERS)
    else:
        # Random generic sticker
        return random.choice(GENERIC_STICKERS)