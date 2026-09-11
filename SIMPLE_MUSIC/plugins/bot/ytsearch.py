# -----------------------------------------------
# Yoru Music Bot — YouTube search command
# -----------------------------------------------
from pyrogram.types import Message
from pyrogram import filters

from SIMPLE_MUSIC import app
from SIMPLE_MUSIC.platforms.Youtube import search_youtube_api


@app.on_message(filters.command("search"))
async def ytsearch(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("/search needs an argument!")
        return

    query = message.text.split(None, 1)[1].strip()
    status = await message.reply_text("Searching YouTube...")
    try:
        results = await search_youtube_api(query)
        if not results:
            await status.edit("No YouTube results found.")
            return

        lines = []
        for index, result in enumerate(results[:5], 1):
            video_id = result.get("videoId")
            if not video_id:
                continue
            title = result.get("title", "Unknown title")
            duration = result.get("durationText", "Unknown")
            views = result.get("viewCount") or result.get("views") or "Unknown"
            channel = result.get("channelTitle") or result.get("channel") or "Unknown"
            watch_url = result.get("watchUrl") or f"https://www.youtube.com/watch?v={video_id}"
            lines.append(
                f"{index}. {title}\n"
                f"Duration: {duration}\n"
                f"Views: {views}\n"
                f"Channel: {channel}\n"
                f"{watch_url}\n"
            )

        await status.edit("\n".join(lines) if lines else "No valid YouTube results found.")
    except Exception as error:
        await status.edit(f"Search failed: {error}")
