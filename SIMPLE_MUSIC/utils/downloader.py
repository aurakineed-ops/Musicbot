# -----------------------------------------------
# 🔸 YORU MUSIC BOT Project
# 🔹 Developed & Maintained by: Yoru Music Bot ()
# 📅 Copyright © 2026 – All Rights Reserved
# -----------------------------------------------
from os import path
import os
import yt_dlp

BASE_OPTS = {
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "format": "bestaudio[ext=m4a]/bestaudio/best",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "extractor_args": {"youtube": {"player_client": ["tv", "web", "mweb"]}},
}


def download(url: str, my_hook) -> str:
    opts = {
        **BASE_OPTS,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        ydl.add_progress_hook(my_hook)
        ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
