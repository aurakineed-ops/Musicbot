# -----------------------------------------------
# 🔸 AALIYA MUSIC BOT Project
# 🔹 Developed & Maintained by: Aaliya Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Aaliya Music Bot
# -----------------------------------------------
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import random
from SIMPLE_MUSIC import app


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice([
            "Fʟᴀᴡs ᴇxɪsᴛ, ʙᴜᴛ sᴏ ᴅᴏᴇs ᴘᴏᴛᴇɴᴛɪᴀʟ. Kᴇᴇᴘ ɴᴜʀᴛᴜʀɪɴɢ ᴛʜɪs.",
            "A ɢᴏᴏᴅ sᴛᴀʀᴛ ʙᴜᴛ ᴛʜᴇʀᴇ's ʀᴏᴏᴍ ᴛᴏ ɢʀᴏᴡ.",
            "Iᴛ's ᴊᴜsᴛ ᴛʜᴇ ʙᴇɢɪɴɴɪɴɢ ᴏғ sᴏᴍᴇᴛʜɪɴɢ ʙᴇᴀᴜᴛɪғᴜʟ.",
        ])
    elif love_percentage <= 70:
        return random.choice([
            "A sᴛʀᴏɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ɪs ᴛʜᴇʀᴇ. Kᴇᴇᴘ ɴᴜʀᴛᴜʀɪɴɢ ɪᴛ.",
            "Yᴏᴜ'ᴠᴇ ɢᴏᴛ ᴀ ɢᴏᴏᴅ ᴄʜᴀɴᴄᴇ. Wᴏʀᴋ ᴏɴ ɪᴛ.",
            "Lᴏᴠᴇ ɪs ʙʟᴏssᴏᴍɪɴɢ, ᴋᴇᴇᴘ ɢᴏɪɴɢ.",
        ])
    else:
        return random.choice([
            "Fʟᴀᴡʟᴇss ᴄᴏɴɴᴇᴄᴛɪᴏɴ.",
            "Tʜᴇ sʏsᴛᴇᴍ ʀᴇᴄᴏʀᴅs ᴛʜɪs ᴀs ᴀ ᴘᴇʀғᴇᴄᴛ ʙᴏɴᴅ !",
            "Dᴇsᴛɪɴᴇᴅ ᴛᴏ ʙᴇ ᴛᴏɢᴇᴛʜᴇʀ. Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs !",
        ])


@app.on_message(filters.command("love", prefixes="/"))
async def love_command(client, message):
    args = message.text.split(None, 2)[1:]
    if len(args) < 2:
        return await message.reply_text(
            "<b>ᴜsᴀɢᴇ:</b>\n<b>⦿ /love [ɴᴀᴍᴇ 1] [ɴᴀᴍᴇ 2]</b>"
        )

    name1, name2 = args[0].strip(), args[1].strip()
    love_percentage = random.randint(10, 100)
    love_message = get_random_message(love_percentage)

    response = (
        "<blockquote><emoji id='5364040533498932357'>💎</emoji>  ˹Y ᴏ ʀ ᴜ  ʟ σ ᴠ є  ϻ ᴧ ᴛ ʀ ɪ x\n"
        "──────────────────\n"
        f"<emoji id='6154635934135490309'>💗</emoji> η ᴧ ϻ є  1 : <code>{name1}</code>\n"
        f"<emoji id='6154635934135490309'>💗</emoji> η ᴧ ϻ є  2 : {name2}\n\n"
        f"<emoji id='6294226146531744488'>💐</emoji> ϻ ᴧ ᴛ ᴄ ʜ : {love_percentage}%\n\n"
        f"<emoji id='5363992034728229166'>✨</emoji> {love_message}\n"
        "──────────────────\n"
        "<emoji id='6293832040332664717'>❤️</emoji> ᴘσᴡєʀєᴅ ʙʏ : ♪ ˹Yᴏʀᴜ ꭙ Mᴜꜱɪᴄ !! <emoji id='6172657075743625817'>🥂</emoji></blockquote>"
    )
    await message.reply_text(response, parse_mode=ParseMode.HTML)
