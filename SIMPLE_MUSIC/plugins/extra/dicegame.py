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
from pyrogram import Client, enums, filters
import asyncio
from SIMPLE_MUSIC import app as app
from pyrogram.handlers import MessageHandler


@app.on_message(filters.command("dice"))
async def dice(bot, message):
    x=await bot.send_dice(message.chat.id)
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
  
@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x=await bot.send_dice(message.chat.id, "<emoji id='5463274047771000031'>🎯</emoji>")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)

@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "<emoji id='5384327463629233871'>🏀</emoji>")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("jackpot"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "<emoji id='5453884647966524953'>🎰</emoji>")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("ball"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "<emoji id='5769392945530674662'>🎳</emoji>")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
@app.on_message(filters.command("football"))
async def basket(bot, message):
    x=await bot.send_dice(message.chat.id, "<emoji id='5375159220280762629'>⚽</emoji>")
    m=x.dice.value
    await message.reply_text(f"Hey {message.from_user.mention} your Score is : {m}",quote=True)
__help__ = """
 Play Game With Emojis:
/dice - Dice <emoji id='5260547274957672345'>🎲</emoji>
/dart - Dart <emoji id='5463274047771000031'>🎯</emoji>
/basket - Basket Ball <emoji id='5384327463629233871'>🏀</emoji>
/ball - Bowling Ball <emoji id='5769392945530674662'>🎳</emoji>
/football - Football <emoji id='5375159220280762629'>⚽</emoji>
/jackpot - Spin slot machine <emoji id='5453884647966524953'>🎰</emoji>
 """

__mod_name__ = "Dɪᴄᴇ"
