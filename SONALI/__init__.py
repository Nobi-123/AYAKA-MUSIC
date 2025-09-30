# SONALI/__init__.py

# --------------------------
# Core modules
# --------------------------
from .core.bot import RAUSHAN
from .core.dir import dirr
from .core.git import git
from .core.userbot import Userbot

# Misc / utilities
from .misc import dbb, heroku

# --------------------------
# Modules
# --------------------------
# Import modules here carefully, AFTER core imports
from .modules.stickers import STICKERS, get_context_sticker
from .modules.chatbot import chat_and_respond, last_bot_message, OWNER_USERNAME
from .modules.voice_manager import text_to_voice
from .modules.reactions import react_to_message
from .modules.chat_control import is_chat_enabled, enable_chat, disable_chat

# --------------------------
# APIs (placeholders)
# --------------------------
from .platforms import AppleAPI, CarbonAPI, SoundAPI, SpotifyAPI, RessoAPI, TeleAPI, YouTubeAPI

# --------------------------
# Initialize core functions (do not call heavy code here if possible)
# --------------------------
dirr()
git()
dbb()
heroku()

# --------------------------
# Initialize bot objects
# --------------------------
# Create bot instances only after all imports
app = RAUSHAN()
userbot = Userbot()

# --------------------------
# Initialize API objects
# --------------------------
Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()