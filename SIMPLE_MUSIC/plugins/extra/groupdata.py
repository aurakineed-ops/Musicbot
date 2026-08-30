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
import os
import time
from asyncio import sleep
from pyrogram import Client, filters
from pyrogram import enums, filters
from SIMPLE_MUSIC import app

@app.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("GETTING INFORMATION...")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED):
            banned += 1
        async for member in app.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = "{:.2f}".format(end_time - start_time)
        await sent_message.edit(f"""
**<emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji>
➲ NAME : {message.chat.title} <emoji id='6082375377123023700'>✅</emoji>
➲ MEMBERS : [ {count} ]<emoji id='5992129361090711368'>🫂</emoji>
<emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji>
➲ BOTS : {bot}<emoji id='5422439311196834318'>💡</emoji>
➲ ZOMBIES : {deleted_acc}<emoji id='5190680981824085932'>🧟</emoji>
➲ BANNED : {banned}<emoji id='5472267631979405211'>🚫</emoji>
➲ PREMIUM USERS : {premium_acc}<emoji id='5384490809825450636'>🎁</emoji>
<emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji><emoji id='5229113891081956317'>➖</emoji>
TIME TAKEN : {timelog} S**""")
    else:
        sent_message = await message.reply_text("ONLY ADMINS CAN USE THIS !")
        await sleep(5)
        await sent_message.delete()
