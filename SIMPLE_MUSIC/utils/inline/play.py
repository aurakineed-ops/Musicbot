# -----------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 Developed & Maintained by: Yoru Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Yoru Music Bot
# -----------------------------------------------
import math
import random
import config
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.utils.database import is_autoplay
from SIMPLE_MUSIC.utils.formatters import time_to_seconds

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _group_add_url():
    return f"https://t.me/{app.username}?startgroup=true"


def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}


def _get_icon(emoji_id: str):
    # icon_custom_emoji_id only renders if the bot owner has Telegram Premium
    # (or the bot purchased a Fragment username) — gate it behind a config flag
    # so bots without Premium don't get a BUTTON_ICON_INVALID error on send.
    if getattr(config, "BUTTON_ICON", False):
        return {"icon_custom_emoji_id": emoji_id}
    return {}

def stream_caption(title, duration, requester):
    return (
        "<blockquote><b><emoji id='5388992682875958399'>🎬</emoji> sᴛʀᴇᴀᴍ ʜᴀs sᴛᴀʀᴛᴇᴅ. ᴇɴᴊᴏʏ ᴛʜᴇ ᴍᴜsɪᴄ |</b>\n"
        f"<b><emoji id='5989830505615331276'>🎵</emoji> ᴛɪᴛʟᴇ :</b> {title}\n"
        f"<b><emoji id='5258419835922030550'>🕔</emoji> ʟᴇɴɢᴛʜ :</b> {duration} ᴍɪɴs\n"
        f"<b><emoji id='5256143829672672750'>👤</emoji>ʀᴇǫᴜᴇsᴛᴇʀ :</b> {requester}</blockquote>"
    )


def track_markup(_, videoid, user_id, channel, fplay):
    r1 = random.choice(STYLES)
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                **_get_style(r1)
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                **_get_style(r1)
            ),
        ],
    ]
    return buttons


async def _autoplay_button_data(chat_id):
    """Returns (label_text, icon_emoji_id). Telegram buttons only support ONE
    custom-emoji icon slot, so the icon itself swaps between the ✔️/❌ premium
    emoji depending on state — that's the part that actually needs to look
    'premium', the text stays plain since button labels can't render
    per-character custom emoji."""
    if await is_autoplay(chat_id):
        return "Aᴜᴛᴏᴩʟᴀʏ : ᴏɴ", "6219844953711844584"
    return "Aᴜᴛᴏᴩʟᴀʏ : ᴏꜰꜰ", "6237830550170640402"


async def stream_markup_timer(_, chat_id, played, dur):
    autoplay_label, autoplay_icon = await _autoplay_button_data(chat_id)
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)

    remaining_sec = duration_sec - played_sec
    if remaining_sec < 0:
        remaining_sec = 0

    rem_min = remaining_sec // 60
    rem_sec = remaining_sec % 60
    remaining = f"{rem_min:02d}:{rem_sec:02d}"

    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
    umm = math.floor(percentage)

    if 0 < umm <= 10:
        bar = "|♬—————————|-"
    elif 10 < umm < 20:
        bar = "|—♬————————|-"
    elif 20 <= umm < 30:
        bar = "|——♬———————|-"
    elif 30 <= umm < 40:
        bar = "|———♬——————|-"
    elif 40 <= umm < 50:
        bar = "|————♬—————|-"
    elif 50 <= umm < 60:
        bar = "|—————♬————|-"
    elif 60 <= umm < 70:
        bar = "|——————♬———|-"
    elif 70 <= umm < 80:
        bar = "|———————♬——|-"
    elif 80 <= umm < 95:
        bar = "|指標———————♬—|-"
    else:
        bar = "|—————————♬|-"

    r1, r2, r3 = random.choices(STYLES, k=3)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {remaining}",
                url=_group_add_url(),
                **_get_style(r1)
            )
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", **_get_style(r2)),
        ],
        [
            InlineKeyboardButton(
                text=autoplay_label,
                callback_data=f"autoplay_toggle {chat_id}",
                **_get_style(r2),
                **_get_icon(autoplay_icon),
            ),
        ],
        [
            InlineKeyboardButton(text="10s", callback_data=f"ADMIN Back10|{chat_id}", **_get_style(r2), **_get_icon("5456187398977247949")),
            InlineKeyboardButton(text="10s", callback_data=f"ADMIN Fwd10|{chat_id}", **_get_style(r2), **_get_icon("5456327792868220208")),
        ],
        [
            InlineKeyboardButton(text="Close", callback_data=f"STREAM_CLOSE|{chat_id}", **_get_style(r3), **_get_icon("6026256492619895014"))
        ],
    ]
    return buttons


async def stream_markup(_, chat_id):
    r1, r2, r3 = random.choices(STYLES, k=3)
    autoplay_label, autoplay_icon = await _autoplay_button_data(chat_id)
    buttons = [
        [
            InlineKeyboardButton(text="ʟᴏᴀᴅɪɴɢ…", url=_group_add_url(), **_get_style(r1)),
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", **_get_style(r1)),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", **_get_style(r1)),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", **_get_style(r1)),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", **_get_style(r1)),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", **_get_style(r1)),
        ],
        [
            InlineKeyboardButton(
                text=autoplay_label,
                callback_data=f"autoplay_toggle {chat_id}",
                **_get_style(r2),
                **_get_icon(autoplay_icon),
            ),
        ],
        [
            InlineKeyboardButton(text="10s", callback_data=f"ADMIN Back10|{chat_id}", **_get_style(r1), **_get_icon("5456187398977247949")),
            InlineKeyboardButton(text="10s", callback_data=f"ADMIN Fwd10|{chat_id}", **_get_style(r1), **_get_icon("5456327792868220208")),
        ],
        [
            InlineKeyboardButton(text="Close", callback_data=f"STREAM_CLOSE|{chat_id}", **_get_style(r3), **_get_icon("6026256492619895014"))
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    r1 = random.choice(STYLES)
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"SIMPLEPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                **_get_style(r1)
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"SIMPLEPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                **_get_style(r1)
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    r1 = random.choice(STYLES)
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                **_get_style(r1)
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    r1, r2 = random.choices(STYLES, k=2)
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                **_get_style(r1)
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                **_get_style(r1)
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                **_get_style(r2)
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                **_get_style(r2)
            ),
        ],
    ]
    return buttons
