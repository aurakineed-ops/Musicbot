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
import config
import aiohttp
from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from SIMPLE_MUSIC import app

STYLES = [
    enums.ButtonStyle.PRIMARY,
    enums.ButtonStyle.SUCCESS,
    enums.ButtonStyle.DANGER
]

def _get_style(style_val):
    if getattr(config, "BUTTON_COLOUR", False):
        return {"style": style_val}
    return {}

@app.on_message(filters.command(["github", "git"]))
async def github(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text("<b>ᴜsᴀɢᴇ:</b> `/git <username>`")

    username = message.text.split(None, 1)[1]
    url = f"https://api.github.com/users/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return await message.reply_text("<emoji id='5472267631979405211'>🚫</emoji> <b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ!</b>")
            elif response.status != 200:
                return await message.reply_text("<emoji id='6098337704682984714'>⚠</emoji>️ <b>ᴇʀʀᴏʀ ғᴇᴛᴄʜɪɴɢ ᴅᴀᴛᴀ!</b>")

            data = await response.json()

    name = data.get("name", "Not specified")
    bio = data.get("bio", "No bio available.")
    blog = data.get("blog", "N/A")
    location = data.get("location", "Unknown")
    company = data.get("company", "N/A")
    created = data.get("created_at", "N/A")
    url = data.get("html_url", "N/A")
    repos = data.get("public_repos", "0")
    followers = data.get("followers", "0")
    following = data.get("following", "0")
    avatar = data.get("avatar_url", None)

    caption = f"""
<emoji id='5325547803936572038'>✨</emoji> <b>ɢɪᴛʜᴜʙ ᴘʀᴏғɪʟᴇ ɪɴꜰᴏ</b>

<emoji id='5373012449597335010'>👤</emoji> <b>ɴᴀᴍᴇ:</b> `{name}`
<emoji id='5462921117423384478'>🔧</emoji> <b>ᴜsᴇʀɴᴀᴍᴇ:</b> `{username}`
📌 <b>ʙɪᴏ:</b> {bio}
<emoji id='5264733042710181045'>🏢</emoji> <b>ᴄᴏᴍᴘᴀɴʏ:</b> {company}
📍 <b>ʟᴏᴄᴀᴛɪᴏɴ:</b> {location}
<emoji id='5224450179368767019'>🌐</emoji> <b>ʙʟᴏɢ:</b> {blog}
<emoji id='6203809036182232315'>🗓</emoji> <b>ᴄʀᴇᴀᴛᴇᴅ ᴏɴ:</b> `{created}`
<emoji id='5357315181649076022'>📁</emoji> <b>ᴘᴜʙʟɪᴄ ʀᴇᴘᴏs:</b> `{repos}`
<emoji id='5258513401784573443'>👥</emoji> <b>ғᴏʟʟᴏᴡᴇʀs:</b> `{followers}` | <b>ғᴏʟʟᴏᴡɪɴɢ:</b> `{following}`
🔗 <b>ᴘʀᴏғɪʟᴇ:</b> [ᴠɪᴇᴡ ᴏɴ ɢɪᴛʜᴜʙ]({url})
""".strip()

    r1 = random.choice(STYLES)
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="close", **_get_style(r1))]]
    )

    if avatar:
        await message.reply_photo(photo=avatar, caption=caption, reply_markup=keyboard)
    else:
        await message.reply_text(caption, reply_markup=keyboard)
