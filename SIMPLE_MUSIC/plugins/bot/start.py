import asyncio
import random
import time
import requests
from html import escape
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import config
from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.platforms.Youtube import get_exact_video_info
from SIMPLE_MUSIC.misc import _boot_
from SIMPLE_MUSIC.plugins.sudo.sudoers import sudoers_list
from SIMPLE_MUSIC.utils import bot_sys_stats
from SIMPLE_MUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from SIMPLE_MUSIC.utils.decorators.language import LanguageStart
from SIMPLE_MUSIC.utils.formatters import get_readable_time
from SIMPLE_MUSIC.utils.inline import help_pannel_page1, private_panel, start_panel
from strings import get_string

# <emoji id='6082375377123023700'>✅</emoji> Purana tareeqa: Wapas START_IMG_URL import kar diya
from config import BANNED_USERS

# 💖 Heart effect on /start (private chats only)
HEART_EFFECTS = ["5159385139981059251"]
FALLBACK_EFFECTS = ["💖", "❤️", "💗", "💓", "💞", "💕", "💝"]


async def delete_effect_message(chat_id: int, message_id: int):
    await asyncio.sleep(2)
    try:
        requests.post(
            f"https://api.telegram.org/bot{config.BOT_TOKEN}/deleteMessage",
            json={"chat_id": chat_id, "message_id": message_id},
            timeout=5,
        )
    except Exception:
        pass


async def send_heart_effect_private(chat_id: int, retries: int = 3):
    """Sends a floating heart-effect message that auto-deletes, private chats only."""
    for _attempt in range(retries):
        try:
            effect_id = random.choice(HEART_EFFECTS)
            emoji = random.choice(FALLBACK_EFFECTS)
            response = requests.post(
                f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": emoji, "message_effect_id": effect_id},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    message_id = data.get("result", {}).get("message_id")
                    if message_id:
                        asyncio.create_task(delete_effect_message(chat_id, message_id))
                        return True
            await asyncio.sleep(0.5)
        except Exception:
            await asyncio.sleep(0.5)
    return False


async def send_welcome_animation(message: Message):
    """Small 'Welcome Baby' cycling text animation before the real start message."""
    welcome_msgs = [
        "<emoji id='5411200584374056500'>🎁</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6217332007001658871'>⚣</emoji>",
        "<emoji id='6327605773362794574'>🩷</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6215221185194497730'>🥳</emoji>",
        "<emoji id='5364040533498932357'>💎</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6215176835362198693'>💥</emoji>",
        "<emoji id='6294226146531744488'>💐</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6219844953711844584'>🤩</emoji>",
        "<emoji id='5363992034728229166'>✨</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6237602603371337712'>💌</emoji>",
        "<emoji id='6293832040332664717'>❤️</emoji> Wᴇʟᴄᴏᴍᴇ Bᴀʙʏ ꨄ {}.. <emoji id='6240054458466702947'>💞</emoji>",
    ]
    try:
        lol = await message.reply_text(welcome_msgs[0].format(message.from_user.mention))
        for msg in welcome_msgs[1:]:
            await asyncio.sleep(0.3)
            await lol.edit_text(msg.format(message.from_user.mention))
        await asyncio.sleep(1.5)
        await lol.delete()
    except Exception:
        pass

async def send_logs_bg(message, text_type="started"):
    if await is_on_off(2):
        try:
            text = f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>๏ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>๏ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}"
            if text_type == "sudolist":
                text = f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>."
            elif text_type == "info":
                text = f"❖ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>."
            await app.send_message(chat_id=config.LOGGER_ID, text=text)
        except:
            pass

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message):
    try:
        await client.send_reaction(chat_id=message.chat.id, message_id=message.id, emoji="❤️", big=True)
    except Exception:
        pass
    asyncio.create_task(add_served_user(message.from_user.id))
    _ = get_string("en")

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name.startswith("help"):
            keyboard = help_pannel_page1(_)
            await client.send_photo(
                chat_id=message.chat.id,
                photo=config.START_IMG_URL,
                caption=_['help_1'].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            asyncio.create_task(send_logs_bg(message, "sudolist"))
            
        elif name.startswith("info_"):
            # The payload is the exact YouTube video ID from the playback card.
            video_id = name.split("info_", 1)[1].strip()
            result = await get_exact_video_info(video_id)
            if not result:
                await message.reply_text("Track information is unavailable for this video.")
                return

            video_id = str(result.get("videoId") or video_id)
            title = escape(str(result.get("title") or "Unknown"))
            duration = escape(str(result.get("durationText") or "Unknown"))
            stats = result.get("statistics") or {}
            views = escape(str(stats.get("viewCount") or result.get("viewCount") or "Unknown"))
            channel = escape(str(result.get("channelTitle") or result.get("channel") or "YouTube"))
            channel_id = result.get("channelId")
            channellink = result.get("channelUrl") or (
                f"https://www.youtube.com/channel/{channel_id}"
                if channel_id
                else "https://www.youtube.com"
            )
            link = result.get("watchUrl") or f"https://www.youtube.com/watch?v={video_id}"
            published = escape(str(result.get("publishedText") or result.get("publishedAt") or "Unknown"))
            thumbnail = result.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

            searched_text = (
                "<b>✦ ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ✦</b>\n\n"
                f"<b>📌 ᴛɪᴛʟᴇ :</b> <code>{title}</code>\n\n"
                f"<b>⏳ ᴅᴜʀᴀᴛɪᴏɴ :</b> <code>{duration}</code>\n"
                f"<b><emoji id='5208841018379612211'>👀</emoji> ᴠɪᴇᴡs :</b> <code>{views}</code>\n"
                f"<b>⏰ ᴘᴜʙʟɪsʜᴇᴅ :</b> <code>{published}</code>\n"
                f"<b><emoji id='6098158454222887821'>📎</emoji> ᴄʜᴀɴɴᴇʟ :</b> <a href=\"{channellink}\">{channel}</a>\n\n"
                f"<b>🔗 ᴠɪᴅᴇᴏ :</b> <a href=\"{link}\">ᴏᴘᴇɴ ᴏɴ ʏᴏᴜᴛᴜʙᴇ</a>"
            )
            key = InlineKeyboardMarkup([
                [InlineKeyboardButton(text=_["S_B_8"], url=link), InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT)],
            ])
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            asyncio.create_task(send_logs_bg(message, "info"))
    else:
        # Reaction
        try:
            await message.react(random.choice(FALLBACK_EFFECTS))
        except Exception:
            pass

        # 💖 Heart effect + welcome animation (private only)
        asyncio.create_task(send_heart_effect_private(message.chat.id))
        await send_welcome_animation(message)

        out = private_panel(_)
        await client.send_photo(
            chat_id=message.chat.id,
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention, "Mina 0.5s", "0.2 GB", "1.2%", "14%", "<emoji id='5258203794772085854'>⚡</emoji> Fast", "<emoji id='6086954744268460848'>🔥</emoji> Active", app.username),
            reply_markup=InlineKeyboardMarkup(out),
        )
        asyncio.create_task(send_logs_bg(message, "started"))


@app.on_callback_query(filters.regex("home") & ~BANNED_USERS)
@LanguageStart
async def home_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    out = private_panel(_)
    await CallbackQuery.edit_message_text(
        text=_["start_2"].format(CallbackQuery.from_user.mention, app.mention, "Mina 0.5s", "0.2 GB", "1.2%", "14%", "<emoji id='5258203794772085854'>⚡</emoji> Fast", "<emoji id='6086954744268460848'>🔥</emoji> Active", app.username),
        reply_markup=InlineKeyboardMarkup(out),
    )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    try:
        await client.send_reaction(chat_id=message.chat.id, message_id=message.id, emoji="❤️", big=True)
    except Exception:
        pass
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await client.send_photo(
        chat_id=message.chat.id,
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return asyncio.create_task(add_served_chat(message.chat.id))


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)

                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(app.mention, f"https://t.me/{app.username}?start=sudolist", config.SUPPORT_CHAT),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(message.from_user.mention, app.mention, message.chat.title, app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                asyncio.create_task(add_served_chat(message.chat.id))
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
