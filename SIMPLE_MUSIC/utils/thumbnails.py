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
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from config import YOUTUBE_IMG_URL, YT_SEARCH_API_URL

# Constants
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../cache")
os.makedirs(CACHE_DIR, exist_ok=True)

PANEL_W, PANEL_H = 763, 545
PANEL_X = (1280 - PANEL_W) // 2
PANEL_Y = 88
TRANSPARENCY = 170
INNER_OFFSET = 36

THUMB_W, THUMB_H = 542, 273
THUMB_X = PANEL_X + (PANEL_W - THUMB_W) // 2
THUMB_Y = PANEL_Y + INNER_OFFSET

TITLE_X = 377
META_X = 377
TITLE_Y = THUMB_Y + THUMB_H + 10
META_Y = TITLE_Y + 45

BAR_X, BAR_Y = 388, META_Y + 45
BAR_RED_LEN = 280
BAR_TOTAL_LEN = 480

ICONS_W, ICONS_H = 415, 45
ICONS_X = PANEL_X + (PANEL_W - ICONS_W) // 2
ICONS_Y = BAR_Y + 48

MAX_TITLE_WIDTH = 580

def trim_to_width(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> str:
    ellipsis = "…"
    if font.getlength(text) <= max_w:
        return text
    for i in range(len(text) - 1, 0, -1):
        if font.getlength(text[:i] + ellipsis) <= max_w:
            return text[:i] + ellipsis
    return ellipsis

async def get_thumb(videoid: str, title: str = None, duration: str = None, views: str = None, thumbnail_url: str = None) -> str:
    # v5 avoids old cards generated from an unrelated search result.
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_v5.png")
    if os.path.exists(cache_path):
        return cache_path

    # Never search again by video ID: that can return another video and wrong metadata.
    title = re.sub(r"\W+", " ", title or "YouTube Track").title()
    thumbnail = (thumbnail_url or f"https://i.ytimg.com/vi/{videoid}/hq720.jpg").split("?")[0]
    real_yt_url = thumbnail
    duration = duration or "Unknown"
    views = views or "Unknown Views"

    is_live = not duration or str(duration).strip().lower() in {"", "live", "live now"}
    duration_text = "Live" if is_live else duration or "Unknown Mins"

    # Download thumbnail
    thumb_path = os.path.join(CACHE_DIR, f"thumb{videoid}.png")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
    except Exception:
        return real_yt_url if real_yt_url else YOUTUBE_IMG_URL

    # Create base image - wrap entire PIL section to fallback to real YT thumbnail on any error
    try:
        base = Image.open(thumb_path).resize((1280, 720)).convert("RGBA")
        bg = ImageEnhance.Brightness(base.filter(ImageFilter.BoxBlur(10))).enhance(0.6)

        # Frosted glass panel
        panel_area = bg.crop((PANEL_X, PANEL_Y, PANEL_X + PANEL_W, PANEL_Y + PANEL_H))
        overlay = Image.new("RGBA", (PANEL_W, PANEL_H), (255, 255, 255, TRANSPARENCY))
        frosted = Image.alpha_composite(panel_area, overlay)
        mask = Image.new("L", (PANEL_W, PANEL_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W, PANEL_H), 50, fill=255)
        bg.paste(frosted, (PANEL_X, PANEL_Y), mask)

        # Draw details
        draw = ImageDraw.Draw(bg)
        try:
            title_font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../assets/assets/font2.ttf"), 32)
            regular_font = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../assets/assets/font.ttf"), 18)
        except OSError:
            title_font = regular_font = ImageFont.load_default()

        thumb = base.resize((THUMB_W, THUMB_H))
        tmask = Image.new("L", thumb.size, 0)
        ImageDraw.Draw(tmask).rounded_rectangle((0, 0, THUMB_W, THUMB_H), 20, fill=255)
        bg.paste(thumb, (THUMB_X, THUMB_Y), tmask)

        draw.text((TITLE_X, TITLE_Y), trim_to_width(title, title_font, MAX_TITLE_WIDTH), fill="black", font=title_font)
        draw.text((META_X, META_Y), f"YouTube | {views}", fill="black", font=regular_font)

        # Progress bar
        draw.line([(BAR_X, BAR_Y), (BAR_X + BAR_RED_LEN, BAR_Y)], fill="red", width=6)
        draw.line([(BAR_X + BAR_RED_LEN, BAR_Y), (BAR_X + BAR_TOTAL_LEN, BAR_Y)], fill="gray", width=5)
        draw.ellipse([(BAR_X + BAR_RED_LEN - 7, BAR_Y - 7), (BAR_X + BAR_RED_LEN + 7, BAR_Y + 7)], fill="red")

        draw.text((BAR_X, BAR_Y + 15), "00:00", fill="black", font=regular_font)
        end_text = "Live" if is_live else duration_text
        draw.text((BAR_X + BAR_TOTAL_LEN - (90 if is_live else 60), BAR_Y + 15), end_text, fill="red" if is_live else "black", font=regular_font)

        # Icons
        icons_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../assets/assets/play_icons.png")
        if os.path.isfile(icons_path):
            ic = Image.open(icons_path).resize((ICONS_W, ICONS_H)).convert("RGBA")
            r, g, b, a = ic.split()
            black_ic = Image.merge("RGBA", (r.point(lambda *_: 0), g.point(lambda *_: 0), b.point(lambda *_: 0), a))
            bg.paste(black_ic, (ICONS_X, ICONS_Y), black_ic)

        # Cleanup and save
        try:
            os.remove(thumb_path)
        except OSError:
            pass

        bg.save(cache_path)
        return cache_path

    except Exception as pil_err:
        # PIL failed - return the actual YouTube thumbnail URL instead of generic logo
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return real_yt_url if (real_yt_url and real_yt_url != YOUTUBE_IMG_URL) else YOUTUBE_IMG_URL
