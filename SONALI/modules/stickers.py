
# SONALI/modules/stickers.py
"""
Contains sticker IDs to be used by the bot for automatic replies.
"""

import random

# List of Telegram sticker file_ids
STICKERS = [
    "CAACAgUAAxkBAAEEj2Ng6nObGqDFN9Q_hvYfU2N2ZCw7cAACcQADVp29Cm2WjGg1Xb6DJAQ",
    "CAACAgUAAxkBAAEEj2Rg6nQ2a8l6y7F_8_YqOVc7gYdJ4wACVQADVp29CmaNObo9mT3EjAQ",
    "CAACAgUAAxkBAAEEj2Ng6nQF9_t9OCc3sKxMciEjF9t8IwACVgADVp29Cn9wrBfr59kQJAQ",
    "CAACAgUAAxkBAAEEj2Ng6nQF8a8y7F_8_YqOVc7gYdJ4wACVgADVp29Cn9wrBfr59kQJAQ",
    # Add as many as you want
]

def get_random_sticker():
    """Return a random sticker file_id."""
    return random.choice(STICKERS)