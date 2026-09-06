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
import asyncio
from html import escape
from pyrogram.enums import ChatType, ParseMode
from SIMPLE_MUSIC import app
from pyrogram import filters
from SIMPLE_MUSIC.utils.Simple_ban import admin_filter

SPAM_CHATS = []


@app.on_message(filters.command("mention") & filters.group & admin_filter)
async def tag_all_users(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text(
            "<b>ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ</b>"
        )
    if chat_id in SPAM_CHATS:
        return await message.reply_text(
            "A tagging process is already running. Use /alloff."
        )

    text = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    SPAM_CHATS.append(chat_id)
    usernum = 0
    usertxt = ""
    try:
        async for member in app.get_chat_members(chat_id):
            if chat_id not in SPAM_CHATS:
                break
            user = member.user
            if not user or user.is_bot or user.is_deleted:
                continue
            usernum += 1
            name = escape(user.first_name or "User")
            usertxt += f"\n⊚ <a href='tg://user?id={user.id}'>{name}</a>\n"
            if usernum == 5:
                if replied:
                    await replied.reply_text(
                        usertxt,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                else:
                    await app.send_message(
                        chat_id,
                        f"{escape(text, quote=False)}\n{usertxt}",
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""

        if usernum and chat_id in SPAM_CHATS:
            if replied:
                await replied.reply_text(
                    usertxt,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            else:
                await app.send_message(
                    chat_id,
                    f"{escape(text or '', quote=False)}\n{usertxt}",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
    finally:
        if chat_id in SPAM_CHATS:
            SPAM_CHATS.remove(chat_id)
           
@app.on_message(filters.command("alloff") & filters.group & admin_filter)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try :
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass   
        return await message.reply_text("<b>ᴛᴀɢ ᴀʟʟ sᴜᴄᴄᴇssғᴜʟʟʏ sᴛᴏᴘᴘᴇᴅ!</b>")     
                                     
    else :
        await message.reply_text("<b>ɴᴏ ᴘʀᴏᴄᴇss ᴏɴɢᴏɪɴɢ!</b>")  
        return       
