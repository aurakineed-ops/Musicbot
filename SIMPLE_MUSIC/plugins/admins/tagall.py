# ---------------------------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 Developed & Maintained by: Yoru Music Bot ()
# 📅 Copyright © 2025 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by Yoru Music Bot
# ---------------------------------------------------------------

import asyncio
from html import escape
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
import random
import re
from SIMPLE_MUSIC import app

SPAM_CHATS = []
EMOJI = [
    "<emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji><emoji id='5316558987141852841'>🦋</emoji>",
    "<emoji id='5454136337345037322'>🧚</emoji><emoji id='5222044641200720562'>🌸</emoji><emoji id='5474268541278493225'>🧋</emoji><emoji id='5404573776253825754'>🍬</emoji>🫖",
    "<emoji id='5208923808169222461'>🥀</emoji><emoji id='5404835520150773707'>🌷</emoji><emoji id='6102617459204822706'>🌹</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='5192959294470895031'>💐</emoji>",
    "<emoji id='5222044641200720562'>🌸</emoji>🌿💮🌱🌵",
    "❤️<emoji id='5280723695579438810'>💚</emoji><emoji id='5283006736985234502'>💙</emoji><emoji id='5283077114319347060'>💜</emoji><emoji id='5370986599423156302'>🖤</emoji>",
    "<emoji id='5258509003738066969'>💓</emoji><emoji id='5219862119209520083'>💕</emoji><emoji id='5219862119209520083'>💞</emoji><emoji id='5364201435858744869'>💗</emoji><emoji id='5431429648409969727'>💖</emoji>",
    "<emoji id='5222044641200720562'>🌸</emoji><emoji id='5192959294470895031'>💐</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='6102617459204822706'>🌹</emoji><emoji id='5316558987141852841'>🦋</emoji>",
    "<emoji id='5364137887522628949'>🍔</emoji>🦪🍛🍲🥗",
    "🍎<emoji id='5418365569076304689'>🍓</emoji><emoji id='5415722218569089767'>🍒</emoji><emoji id='5852518588686011408'>🍑</emoji>🌶️",
    "<emoji id='5474268541278493225'>🧋</emoji>🥤<emoji id='5474268541278493225'>🧋</emoji><emoji id='5413704369918978673'>🥛</emoji><emoji id='5361964771509808811'>🍷</emoji>",
    "<emoji id='5404573776253825754'>🍬</emoji><emoji id='5287295223175604777'>🍭</emoji><emoji id='5420462646988123921'>🧁</emoji><emoji id='6334379727062566543'>🎂</emoji>🍡",
    "🍨🧉<emoji id='5363978187753670318'>🍺</emoji><emoji id='5463051955012122780'>☕</emoji>🍻",
    "🥪🥧<emoji id='5258378333653056711'>🍦</emoji>🍥🍚",
    "🫖<emoji id='5463051955012122780'>☕</emoji>🍹<emoji id='5361964771509808811'>🍷</emoji><emoji id='5413704369918978673'>🥛</emoji>",
    "<emoji id='5463051955012122780'>☕</emoji><emoji id='5303548912726982102'>🧃</emoji><emoji id='5213249338452485580'>🍩</emoji><emoji id='5258378333653056711'>🍦</emoji>🍙",
    "🍁🌾💮🍂🌿",
    "🌨️🌥️⛈️🌩️🌧️",
    "<emoji id='5404835520150773707'>🌷</emoji>🏵️<emoji id='5222044641200720562'>🌸</emoji><emoji id='5440748683765227563'>🌺</emoji><emoji id='5192959294470895031'>💐</emoji>",
    "💮🌼🌻🍀🍁",
    "<emoji id='5190680981824085932'>🧟</emoji>🦸🦹🧙<emoji id='5936271765218006741'>👸</emoji>",
    "🧅🍠<emoji id='5318752353925471388'>🥕</emoji>🌽<emoji id='5431469278073207884'>🥦</emoji>",
    "<emoji id='5357233044694508227'>🐷</emoji><emoji id='5305787660135063955'>🐹</emoji><emoji id='6111671507962829973'>🐭</emoji>🐨<emoji id='5206642759628241872'>🐻</emoji>‍❄️",
    "<emoji id='5316558987141852841'>🦋</emoji><emoji id='5278653070371206372'>🐇</emoji>🐀🐈🐈‍⬛",
    "🌼🌳🌲🌴🌵",
    "🥩🍋<emoji id='5456419915621742790'>🍐</emoji><emoji id='5438195085189595667'>🍈</emoji><emoji id='6273709899507568922'>🍇</emoji>",
    "<emoji id='6093451264555750089'>🍴</emoji><emoji id='5424978787920021797'>🍽</emoji>️<emoji id='5371042017386176566'>🔪</emoji>🍶🥃",
    "🕌<emoji id='5330116450843636190'>🏰</emoji>🏩⛩️🏩",
    "🎉<emoji id='5404573776253825754'>🎊</emoji><emoji id='5278651867780377852'>🎈</emoji><emoji id='6334379727062566543'>🎂</emoji><emoji id='5363882032025849098'>🎀</emoji>",
    "🪴🌵🌴🌳🌲",
    "🎄🎋🎍🎑🎎",
    "🦅🦜🕊️🦤🦢",
    "🦤🦩🦚🦃<emoji id='5368684320858843385'>🦆</emoji>",
    "<emoji id='5362063083311214432'>🐬</emoji><emoji id='5420642954010175242'>🦭</emoji>🦈<emoji id='6282818902372128272'>🐋</emoji><emoji id='5400362079783770689'>🐳</emoji>",
    "<emoji id='5283202076392827429'>🐔</emoji><emoji id='5384574037701696503'>🐟</emoji><emoji id='5397842858126353661'>🐠</emoji>🐡<emoji id='5361600498153564481'>🦐</emoji>",
    "🦩<emoji id='5222474515887435551'>🦀</emoji><emoji id='5474140796066210842'>🦑</emoji><emoji id='5352815688010441881'>🐙</emoji>🦪",
    "🐦<emoji id='5380003148821712039'>🦂</emoji><emoji id='6282555152725447369'>🕷</emoji>️<emoji id='5913384919584741274'>🕸</emoji>️<emoji id='5192907136388059100'>🐚</emoji>",
    "🥪🍰🥧🍨🍨",
    "🥬<emoji id='5305336095863485125'>🍉</emoji><emoji id='5420462646988123921'>🧁</emoji>🧇<emoji id='5361837567463399422'>🔮</emoji>",
]

def clean_text(text):
    """Escape user text before sending it as HTML."""
    if not text:
        return ""
    return escape(text, quote=False)

async def is_admin(chat_id, user_id):
    if not user_id:
        return False
    try:
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if admin.user and admin.user.id == user_id:
                return True
    except Exception:
        return False
    return False

async def process_members(chat_id, members, text=None, replied=None):
    tagged_members = 0
    usernum = 0
    usertxt = ""
    for member in members:
        if chat_id not in SPAM_CHATS:
            break
        user = member.user
        if not user or user.is_deleted or user.is_bot:
            continue
            
        tagged_members += 1
        usernum += 1
        
        name = escape(user.first_name or "User")
        usertxt += f"<a href='tg://user?id={user.id}'>{name}</a> "
        
        if usernum == 5:
            while True:
                try:
                    if replied:
                        await replied.reply_text(
                            usertxt,
                            disable_web_page_preview=True,
                            parse_mode=ParseMode.HTML
                        )
                    else:
                        await app.send_message(
                            chat_id,
                            f"{text}\n{usertxt}",
                            disable_web_page_preview=True,
                            parse_mode=ParseMode.HTML
                        )
                    break
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
            await asyncio.sleep(2)
            usernum = 0
            usertxt = ""
    
    if usernum > 0 and chat_id in SPAM_CHATS:
        try:
            if replied:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML
                )
            else:
                await app.send_message(
                    chat_id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            await app.send_message(chat_id, f"Error sending final batch: {str(e)}")
    
    return tagged_members

@app.on_message(
    filters.command(
        ["all", "allmention", "mentionall", "tagall"],
        prefixes=["/", "@", "#"]
    ) & filters.group
)
async def tag_all_users(_, message):
    admin = await is_admin(
        message.chat.id,
        message.from_user.id if message.from_user else None
    )
    if not admin:
        return await message.reply_text("Only admins can use this command.")

    if message.chat.id in SPAM_CHATS:  
        return await message.reply_text(  
            "Tagging process is already running. Use /cancel to stop it."  
        )  
    
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:  
        return await message.reply_text(  
            "Give some text to tag all, like: `@all Hi Friends`"  
        )  
    
    try:  
        # Get all members at once to avoid multiple iterations
        members = []
        async for m in app.get_chat_members(message.chat.id):
            members.append(m)
        
        total_members = sum(
            1 for m in members
            if m.user and not m.user.is_bot and not m.user.is_deleted
        )
        SPAM_CHATS.append(message.chat.id)
        
        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])
        
        tagged_members = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )
        
        summary_msg = f"""
<emoji id='6082375377123023700'>✅</emoji> Tagging completed!

Total members: {total_members}
Tagged members: {tagged_members}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:  
        await asyncio.sleep(e.value)  
    except Exception as e:  
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")  
    finally:  
        try:  
            SPAM_CHATS.remove(message.chat.id)  
        except Exception:  
            pass

@app.on_message(
    filters.command(
        ["admintag", "adminmention", "report"],
        prefixes=["/", "@", "#"]
    ) & filters.group
)
async def tag_all_admins(_, message):
    if not message.from_user:
        return

    admin = await is_admin(message.chat.id, message.from_user.id)  
    if not admin:  
        return await message.reply_text("Only admins can use this command.")  

    if message.chat.id in SPAM_CHATS:  
        return await message.reply_text(  
            "Tagging process is already running. Use /cancel to stop it."  
        )  
    
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:  
        return await message.reply_text(  
            "Give some text to tag admins, like: `@admins Hi Friends`"  
        )  
    
    try:  
        # Get all admins at once
        members = []
        async for m in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS  
        ):
            members.append(m)
        
        total_admins = len(members)
        SPAM_CHATS.append(message.chat.id)
        
        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])
        
        tagged_admins = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )
        
        summary_msg = f"""
<emoji id='6082375377123023700'>✅</emoji> Admin tagging completed!

Total admins: {total_admins}
Tagged admins: {tagged_admins}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:  
        await asyncio.sleep(e.value)  
    except Exception as e:  
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")  
    finally:  
        try:  
            SPAM_CHATS.remove(message.chat.id)  
        except Exception:  
            pass

@app.on_message(
    filters.command(
        [
            "stopmention",
            "cancelmention",
            "offmention",
            "mentionoff",
            "cancelall",
        ],
        prefixes=["/", "@", "#"],
    ) & filters.group
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(
        chat_id,
        message.from_user.id if message.from_user else None
    )
    if not admin:
        return await message.reply_text("Only admins can use this command.")

    if chat_id in SPAM_CHATS:  
        try:  
            SPAM_CHATS.remove(chat_id)  
        except Exception:  
            pass  
        return await message.reply_text("Tagging process successfully stopped!")  
    else:  
        return await message.reply_text("No tagging process is currently running!")
