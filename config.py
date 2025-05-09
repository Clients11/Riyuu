import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)
# Play duration limit in seconds
DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60*60*2)) # 2 hours

# DURATION_LIMIT_MIN

# Video play duration limit in seconds
VIDEO_DURATION_LIMIT = int(getenv("VIDEO_DURATION_LIMIT", 60*20)) # 20 minutes

# Vars For API End Pont.
YTPROXY_URL = getenv("YTPROXY_URL", 'http://tubed1.okflix.top/') ## E.G https://yt.okflix.
YT_API_KEY = "freekey15052025"

# Chat id of a group for logging bot's activities

LOGGER_ID = int(getenv("LOGGER_ID", -1002389335496))

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 5111294407))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/Clients11/Riyuu",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/+JCeJ-DJMQ6U4Yjc9")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/+Y6HCWX0ZYis1MTA0")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", True))
ASSISTANT_LEAVE_TIME = int(getenv("ASSISTANT_LEAVE_TIME",  5400))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 52428800))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 20971520))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes

PRIVATE_BOT_MODE_MEM = int(getenv("PRIVATE_BOT_MODE_MEM", 1))

TUBED_API = getenv("TUBED_API" , None)
CACHE_DURATION = int(getenv("CACHE_DURATION" , "3600"))  #60*60*24
CACHE_SLEEP = int(getenv("CACHE_SLEEP" , "1800"))   #60*60


# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
file_cache: dict[str, float] = {}

START_IMG_URL = ["https://imgur.com/a/QlMC0gh",
                 "https://imgur.com/a/QlMC0gh"]
    
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://imgur.com/a/QlMC0gh"
)
PLAYLIST_IMG_URL = "https://imgur.com/a/QlMC0gh"
STATS_IMG_URL = "https://imgur.com/a/QlMC0gh"
TELEGRAM_AUDIO_URL = "https://imgur.com/a/QlMC0gh"
TELEGRAM_VIDEO_URL = "https://imgur.com/a/QlMC0gh"
STREAM_IMG_URL = "https://imgur.com/a/QlMC0gh"
SOUNCLOUD_IMG_URL = "https://imgur.com/a/QlMC0gh"
YOUTUBE_IMG_URL = "https://imgur.com/a/QlMC0gh"
SPOTIFY_ARTIST_IMG_URL = "https://imgur.com/a/QlMC0gh"
SPOTIFY_ALBUM_IMG_URL = "https://imgur.com/a/QlMC0gh"
SPOTIFY_PLAYLIST_IMG_URL = "https://imgur.com/a/QlMC0gh"





if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
