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

import config
import random
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
from SIMPLE_MUSIC import app

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def start_panel(_):
    s1 = random.choice(STYLES)
    
    def get_style():
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": s1}
        return {}

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true",
                icon_custom_emoji_id="6106976571837389806",
                **get_style()
            ),
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id="6107010613748177541",
                **get_style()
            ),
        ],
    ]
    return buttons


def private_panel(_):
    s1, s2, s3 = random.sample(STYLES, 3)
    s4 = random.choice(STYLES)
    row_styles = [s1, s2, s3, s4]

    def get_style(index):
        if getattr(config, "BUTTON_COLOUR", False):
            return {"style": row_styles[index]}
        return {}

    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                icon_custom_emoji_id="6106976571837389806",
                **get_style(0)
            )
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"tg://openmessage?user_id={config.OWNER_ID}",
                icon_custom_emoji_id="6104953285758689029",
                **get_style(1)
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_2"], 
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id="6107010613748177541",
                **get_style(2)
            ),
            InlineKeyboardButton(
                text=_["S_B_6"], 
                url=config.SUPPORT_CHANNEL,
                icon_custom_emoji_id="5325773869540205894",
                **get_style(2)
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"], 
                callback_data="settingsback_helper",
                icon_custom_emoji_id="5989830505615331276",
                **get_style(3)
            )
        ],
    ]
    return buttons
