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
import random
from typing import Union
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SIMPLE_MUSIC import app
import config

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

def _get_close_icon():
    if getattr(config, "BUTTON_ICON", False):
        return {"icon_custom_emoji_id": "5424756476117807727"}
    return {}

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    r1, r2 = random.choices(STYLES, k=2)
    not_dur = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                **_get_style(r1)
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                **_get_style(r1),
                **_get_close_icon()
            ),
        ]
    ]
    dur_list = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
                **_get_style(r1)
            )
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
                **_get_style(r2)
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
                **_get_style(r2),
                **_get_close_icon()
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur_list)
    return upl


def queue_back_markup(_, CPLAY):
    r1 = random.choice(STYLES)
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                    **_get_style(r1)
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                    **_get_style(r1),
                    **_get_close_icon()
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    r1, r2, r3, r4 = random.choices(STYLES, k=4)
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", **_get_style(r2)),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", **_get_style(r2)),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", **_get_style(r4), **_get_close_icon())],
    ]
    return buttons
