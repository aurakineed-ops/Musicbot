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
import importlib
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from SIMPLE_MUSIC import LOGGER, app, userbot
from SIMPLE_MUSIC.core.call import SIMPLE
from SIMPLE_MUSIC.misc import sudo
from SIMPLE_MUSIC.plugins import ALL_MODULES
from SIMPLE_MUSIC.utils.database import get_banned_users, get_gbanned
from SIMPLE_MUSIC.utils.dynamic_settings import load_overrides


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def _run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), _HealthHandler)
    server.serve_forever()


threading.Thread(target=_run_health_server, daemon=True).start()

COMMANDS = [
    BotCommand("start", "❖ sᴛᴀʀᴛ ʙᴏᴛ • ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ"),
    BotCommand("help", "❖ ʜᴇʟᴘ ᴍᴇɴᴜ • ɢᴇᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴀɴᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ"),
    BotCommand("ping", "❖ ᴘɪɴɢ ʙᴏᴛ • ᴄʜᴇᴄᴋ ᴘɪɴɢ ᴀɴᴅ sʏsᴛᴇᴍ sᴛᴀᴛs"),
    BotCommand("ask", "❖ ᴀsᴋ ᴀᴀʟɪʏᴀ • ʜɪɴɢʟɪsʜ ᴀɪ ᴄʜᴀᴛ"),
]


async def setup_bot_commands():
    try:
        await app.set_bot_commands(COMMANDS)
        LOGGER("SIMPLE_MUSIC").info("Bot commands set successfully!")
    except Exception as e:
        LOGGER("SIMPLE_MUSIC").error(f"Failed to set bot commands: {str(e)}")


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐍𝐨𝐭 𝐅𝐢𝐥𝐥𝐞𝐝, 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐀 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐒𝐞𝐬𝐬𝐢𝐨𝐧"
        )
        exit()

    await sudo()
    await load_overrides()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)

    except:
        pass

    await app.start()
    
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        importlib.import_module("SIMPLE_MUSIC.plugins" + all_module)

    LOGGER("SIMPLE_MUSIC.plugins").info(
        "𝗬𝗼𝗿𝘂 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁 𝗜𝘀 𝗥𝗲𝗮𝗱𝘆<emoji id='5317026657540780588'>🥳</emoji>..."
    )

    await userbot.start()
    await SIMPLE.start()

    try:
        await SIMPLE.stream_call(
            "https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4"
        )

    except NoActiveGroupCall:
        LOGGER("SIMPLE_MUSIC").warning(
            "𝗡𝗼 𝗮𝗰𝘁𝗶𝘃𝗲 𝘃𝗼𝗶𝗰𝗲 𝗰𝗵𝗮𝘁 𝗶𝗻 𝗹𝗼𝗴 𝗴𝗿𝗼𝘂𝗽 — 𝘀𝘁𝗮𝗿𝘁 𝗮 𝗩𝗖 𝘁𝗵𝗲𝗿𝗲 𝗶𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗲𝘀𝘁 𝘀𝘁𝗿𝗲𝗮𝗺𝗶𝗻𝗴. 𝗕𝗼𝘁 𝘄𝗶𝗹𝗹 𝗰𝗼𝗻𝘁𝗶𝗻𝘂𝗲 𝗿𝘂𝗻𝗻𝗶𝗻𝗴."
        )

    except:
        pass

    await SIMPLE.decorators()

    LOGGER("SIMPLE_MUSIC").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎𝗬𝗢𝗥𝗨 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧\n╚═════ஜ۩۞۩ஜ════╝"
    )

    await idle()

    await app.stop()
    await userbot.stop()

    LOGGER("SIMPLE_MUSIC").info(
        "𝗦𝗧𝗢𝗣 𝗬𝗢𝗥𝗨 𝗠𝗨𝗦𝗜𝗖🎻 𝗕𝗢𝗧.."
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
