# SONALI/__init__.py

# Core modules
from .core.bot import RAUSHAN
from .core.dir import dirr
from .core.git import git
from .core.userbot import Userbot

# Misc and utils
from .misc import dbb, heroku

# SONALI/modules/__init__.py
from .stickers import STICKERS, get_context_sticker
from .chatbot import chat_and_respond, last_bot_message, OWNER_USERNAME
from .voice_manager import text_to_voice
from .reactions import react_to_message
from .chat_control import is_chat_enabled, enable_chat, disable_chat

# APIs (placeholder, update if you have these classes)
from .platforms import AppleAPI, CarbonAPI, SoundAPI, SpotifyAPI, RessoAPI, TeleAPI, YouTubeAPI

# Initialize core objects
dirr()
git()
dbb()
heroku()

app = RAUSHAN()
userbot = Userbot()

# Example API objects (update with your actual API classes)
Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()