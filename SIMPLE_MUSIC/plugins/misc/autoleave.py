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
import asyncio
from datetime import datetime, timedelta
from pyrogram.enums import ChatType
import config
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.core.call import SIMPLE, autoend
from SIMPLE_MUSIC.misc import db
from SIMPLE_MUSIC.utils.database import get_client, group_assistant, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(
            config.AUTO_LEAVE_ASSISTANT_TIME
        ):
            from SIMPLE_MUSIC.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.iter_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            "supergroup",
                            "group",
                            "channel",
                        ]:
                            chat_id = i.chat.id
                            if (
                                chat_id != config.LOGGER_ID
                                and i.chat.id != -1002006121442
                                and i.chat.id != -1001939309491
                            ):
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(
                                            chat_id
                                        )
                                        left += 1
                                    except:
                                        continue
                except:
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in list(autoend.keys()):
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await SIMPLE.stop_stream(chat_id)
                except:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.",
                    )
                except:
                    continue


asyncio.create_task(auto_end())


async def monitor_alone_vc():
    """Unlike the one-time check at join, this keeps watching every 20s for
    as long as music is playing — if everyone leaves the videochat partway
    through a song, it starts the same 1-minute leave-countdown that
    /autoend already uses; if someone comes back in time, it's cancelled."""
    while not await asyncio.sleep(20):
        if not await is_autoend():
            continue
        for chat_id in list(db.keys()):
            try:
                if not await is_active_chat(chat_id):
                    continue
                assistant = await group_assistant(SIMPLE, chat_id)
                users = len(await assistant.get_participants(chat_id))
            except Exception:
                continue
            if users <= 1:  # only the assistant itself is left
                if not autoend.get(chat_id):
                    autoend[chat_id] = datetime.now() + timedelta(minutes=1)
            else:
                autoend[chat_id] = {}


asyncio.create_task(monitor_alone_vc())
