# SONALI/modules/stickers.py
import random

HAPPY_STICKERS = [
    "CAACAgEAAxkBAAEBH4FgxP7JbJ2f7y-3h1O1ikG6RvDsvwACXAADwZxgD7hYxkPY3fLFiQE",
]

SAD_STICKERS = [
    "CAACAgEAAxkBAAEBH4RgxP7JZxTzUcrrL07v5OZay8lPLwACXgADwZxgD8rrd4Lf7OtUFiQE",
]

LOVE_STICKERS = [
    "CAACAgEAAxkBAAEBH4ZgxP7Jj_6pO4hJ-F4uU7v0bZ_tLgACYAADwZxgD2r7uFjTEm6qFiQE",
]

SURPRISE_STICKERS = [
    "CAACAgEAAxkBAAEBH4fgxP7JeHfI5OXp2lQhAGfDRcJGRQACXQADwZxgD3qq3GJ_w2RWiQE",
]

# Combine all
STICKERS = HAPPY_STICKERS + SAD_STICKERS + LOVE_STICKERS + SURPRISE_STICKERS

def get_context_sticker(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["love", "cute"]):
        return random.choice(LOVE_STICKERS)
    elif any(word in text for word in ["happy", "yay"]):
        return random.choice(HAPPY_STICKERS)
    elif any(word in text for word in ["sad", "cry"]):
        return random.choice(SAD_STICKERS)
    elif any(word in text for word in ["wow", "surprise"]):
        return random.choice(SURPRISE_STICKERS)
    else:
        return random.choice(STICKERS)