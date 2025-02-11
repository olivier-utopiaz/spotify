from dotenv import load_dotenv
import os
from loguru import logger

# Load environment variables
load_dotenv()

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Meta/Threads configuration
META_APP_ID = os.getenv('META_APP_ID')
META_APP_SECRET = os.getenv('META_APP_SECRET')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_USER_ID = os.getenv('INSTAGRAM_USER_ID')

# Music genres configuration
MUSIC_GENRES = {
    'hip-hop': ['hip-hop', 'rap'],
    'soul': ['soul', 'r-n-b'],
    'funk': ['funk'],
    'reggae': ['reggae'],
    'salsa': ['salsa', 'latin'],
    'classical': ['classical'],
    'rock': ['rock'],
    'metal': ['metal'],
    'jazz': ['jazz']
}

# Messages configuration
GREETINGS = [
    "Bonjour @threads 👋",
    "Hello la communauté @threads 👋",
    "Salut tout le monde 👋",
    "Hello evertone 👋",
    "Hi there 👋",
]

MORNING_MESSAGES = [
    "Comment ça va en ce {} matin ?",
    "Bien réveillé en ce {} ?",
    "Prêt pour cette belle journée de {} ?",
    "How are you this beautiful morning?"
]

# Posting time configuration
POSTING_TIME = os.getenv('POSTING_TIME', '07:30')
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# Logger configuration
logger.add("logs/threads_bot.log", rotation="1 day", retention="1 month")