# -----------------------------------------------
# Dynamic Settings — lets the owner change bot media / behaviour
# from the /admin panel instead of editing config.py or plugin
# files by hand. Overrides are stored in MongoDB and applied on
# top of config.py at startup + live the moment they're changed.
# -----------------------------------------------
import config
from SIMPLE_MUSIC.core.mongo import mongodb

settingsdb = mongodb.bot_admin_settings

# ── Media that can be changed from the panel ──────────────────
# key            -> (label shown in panel, media type, default value)
MEDIA_SETTINGS = {
    "START_IMG_URL":            ("Sᴛᴀʀᴛ ᴘʜᴏᴛᴏ (/start)",            "photo",   None),
    "HELP_IMG_URL":              ("Hᴇʟᴘ ᴘʜᴏᴛᴏ (/help)",              "photo",   None),
    "PLAYLIST_IMG_URL":          ("Pʟᴀʏʟɪsᴛ ᴘʜᴏᴛᴏ",                  "photo",   None),
    "SPOTIFY_PLAYLIST_IMG_URL":  ("Sᴘᴏᴛɪғʏ ᴘʟᴀʏʟɪsᴛ ᴘʜᴏᴛᴏ",          "photo",   None),
    "SPOTIFY_ALBUM_IMG_URL":     ("Sᴘᴏᴛɪғʏ ᴀʟʙᴜᴍ ᴘʜᴏᴛᴏ",             "photo",   None),
    "SPOTIFY_ARTIST_IMG_URL":    ("Sᴘᴏᴛɪғʏ ᴀʀᴛɪsᴛ ᴘʜᴏᴛᴏ",            "photo",   None),
    "STATS_IMG_URL":             ("Sᴛᴀᴛs ᴘʜᴏᴛᴏ (/stats)",            "photo",   None),
    "PING_IMG_URL":              ("Pɪɴɢ ᴘʜᴏᴛᴏ (/ping)",              "photo",   None),
    "STREAM_IMG_URL":            ("Nᴏᴡ ᴘʟᴀʏɪɴɢ ᴘʜᴏᴛᴏ (ᴀᴜᴅɪᴏ)",       "photo",   None),
    "SOUNCLOUD_IMG_URL":         ("Nᴏᴡ ᴘʟᴀʏɪɴɢ ᴘʜᴏᴛᴏ (SᴏᴜɴᴅCʟᴏᴜᴅ)",  "photo",   None),
    "YOUTUBE_IMG_URL":           ("Fᴀʟʟʙᴀᴄᴋ YᴏᴜTᴜʙᴇ ᴛʜᴜᴍʙɴᴀɪʟ",       "photo",   None),
    "TELEGRAM_VIDEO_URL":        ("Nᴏᴡ ᴘʟᴀʏɪɴɢ ᴠɪᴅᴇᴏ ᴛʜᴜᴍʙ",         "photo",   None),
    "TELEGRAM_AUDIO_URL":        ("Nᴏᴡ ᴘʟᴀʏɪɴɢ ᴀᴜᴅɪᴏ ᴛʜᴜᴍʙ",         "photo",   None),
    "WELCOME_VIDEO_URL":         ("Wᴇʟᴄᴏᴍᴇ ᴠɪᴅᴇᴏ (ɴᴇᴡ ᴍᴇᴍʙᴇʀ)",      "video",   "https://files.catbox.moe/9iom66.mp4"),
    "LOADING_STICKER_ID":        ("Sᴏɴɢ sᴇᴀʀᴄʜ ʟᴏᴀᴅɪɴɢ sᴛɪᴄᴋᴇʀ",      "sticker", "CAACAgUAAxkBAAEh4PxqiaBLfDX8oIaBrlN0mHSJ7Td0RAAC0CMAAkEtGVWBmO4GOjbcQj0E"),
}

# ── Simple on/off toggles that live in config.py ──────────────
TOGGLE_SETTINGS = {
    "BUTTON_COLOUR": "Cᴏʟᴏᴜʀᴇᴅ ʙᴜᴛᴛᴏɴs",
    "BUTTON_ICON":   "Pʀᴇᴍɪᴜᴍ ᴇᴍᴏᴊɪ ᴏɴ ʙᴜᴛᴛᴏɴs",
}


def get_media(key: str):
    """Current value for a media key — live override if set, else config.py/default."""
    default = MEDIA_SETTINGS.get(key, (None, None, None))[2]
    return getattr(config, key, default)


def get_toggle(key: str) -> bool:
    return bool(getattr(config, key, False))


async def set_setting(key: str, value):
    """Persist an override to Mongo and apply it immediately (no restart needed)."""
    await settingsdb.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)
    setattr(config, key, value)


async def load_overrides():
    """Called once at startup — pulls saved overrides from Mongo onto config.py."""
    try:
        async for doc in settingsdb.find({}):
            setattr(config, doc["_id"], doc["value"])
    except Exception:
        pass
