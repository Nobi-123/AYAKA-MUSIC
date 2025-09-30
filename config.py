import os
import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# --------------------------
# Telegram / Pyrogram Config
# --------------------------
API_ID = int(getenv("API_ID", "29481920"))
API_HASH = getenv("API_HASH", "f700ddb0930acfab095b00911a2e6f3a")
BOT_TOKEN = getenv("BOT_TOKEN", "8477795771:AAGFz4p7pmJaw5wp7L1U_KkeqdIJGJ56rZk")

OWNER_USERNAME = getenv("OWNER_USERNAME", "x9Ahad")
OWNER_ID = int(getenv("OWNER_ID", "8195241636"))

BOT_USERNAME = getenv("BOT_USERNAME", "AyakaXMusicBot")
BOT_NAME = getenv("BOT_NAME", "˹ Ａʏᴀᴋᴀ ꭗ‌ Ｍᴜsɪᴄ  ˼")

# --------------------------
# MongoDB
# --------------------------
MONGO_DB_URI = getenv(
    "MONGO_DB_URI",
    "mongodb+srv://ahad0181888:ahad0181888@cluster0.f9casz0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# --------------------------
# Limits
# --------------------------
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))
DURATION_LIMIT = DURATION_LIMIT_MIN * 60  # convert minutes to seconds

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))  # 100 MB
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))  # 1 GB

# --------------------------
# Logging & Support
# --------------------------
LOGGER_ID = int(getenv("LOGGER_ID", "-1002847095020"))
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/TechNodeCoders")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/TNCmeetup")

# --------------------------
# Heroku Config
# --------------------------
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# --------------------------
# APIs
# --------------------------
API_URL = getenv("API_URL", "https://api.thequickearn.xyz")
VIDEO_API_URL = getenv("VIDEO_API_URL", "https://api.video.thequickearn.xyz")
API_KEY = getenv("API_KEY", "30DxNexGenBots121b50")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")

# --------------------------
# ElevenLabs Voice Config
# --------------------------
ELEVENLABS_API_KEYS = [getenv("ELEVENLABS_API_KEY", "sk_79ce62df7f5c28cf7c65f297d531c41b33429708ec0c6b72")]
ELEVENLABS_VOICE_ID = getenv("ELEVENLABS_VOICE_ID", "E7bpJOpaUwdzBn3Wd6Lr")

# --------------------------
# Chatbot / SambaNova API
# --------------------------
CHATBOT_API_KEY = getenv("SAMBANOVA_API_KEY", "41c87b5d-4a4d-4a8f-9544-48d9bfc9b06a")
CHATBOT_API_URL = getenv("SAMBANOVA_API_URL", "https://api.sambanova.ai/v1/chat")

# --------------------------
# Pyrogram Sessions
# --------------------------
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# --------------------------
# Bot Behaviour
# --------------------------
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))

# --------------------------
# Assets / Images
# --------------------------
START_IMG_URL = "https://files.catbox.moe/we2hw5.jpg"
PING_IMG_URL = "https://files.catbox.moe/zywku1.jpg"
PLAYLIST_IMG_URL = "https://files.catbox.moe/tj7a58.jpg"
STATS_IMG_URL = "https://files.catbox.moe/jdwd10.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/lwm506.jpg"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/a80x63.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/a80x63.jpg"

# --------------------------
# Bot States
# --------------------------
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
GREET = ["💌", "❣️", "❤️"]

# --------------------------
# Utility Functions
# --------------------------
def time_to_seconds(time: str) -> int:
    parts = str(time).split(":")
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(parts)))