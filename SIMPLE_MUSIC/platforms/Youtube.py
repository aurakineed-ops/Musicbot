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
import os
import re
import time
from typing import Union

import aiohttp
import aiofiles
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import Playlist

from SIMPLE_MUSIC import LOGGER
from SIMPLE_MUSIC.utils.formatters import time_to_seconds
from SIMPLE_MUSIC.utils.cookies import fetch_cookie_file
from SIMPLE_MUSIC.core.mongo import mongodb

gameoverdb = mongodb.gameover_cache
GAMEOVER_PERSIST_TTL_SECONDS = 6 * 60 * 60  # 6 hours; re-resolved automatically after this


async def get_persisted_gameover(vidid: str):
    try:
        doc = await gameoverdb.find_one({"vidid": vidid})
        if not doc:
            return None
        if time.time() - doc.get("saved_at", 0) > GAMEOVER_PERSIST_TTL_SECONDS:
            return None
        return doc.get("data")
    except Exception:
        return None


async def save_persisted_gameover(vidid: str, data: dict):
    try:
        await gameoverdb.update_one(
            {"vidid": vidid},
            {"$set": {"vidid": vidid, "data": data, "saved_at": time.time()}},
            upsert=True,
        )
    except Exception:
        pass


from config import (API_URL, VIDEO_API_URL, API_KEY, YT_API_KEY, YTPROXY_URL,
                    VDA_API_URL, VDA_API_KEY, VDA_AUDIO_QUALITY, VDA_VIDEO_FORMAT,
                    YT_SEARCH_API_URL, VDA_KEYS_URL, GAMEOVER_API_URL, GAMEOVER_API_KEY)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
CLIENT_SESSION = None

VDA_KEYS_CACHE = None
SEARCH_CACHE = {}
DETAILS_CACHE = {}
VIDEO_INFO_CACHE = {}
GAMEOVER_CACHE = {}
CACHE_TTL_SECONDS = 120


async def _get_vda_keys():
    """Load remote JSON keys once, with an environment key as fallback."""
    global VDA_KEYS_CACHE
    if VDA_KEYS_CACHE is not None:
        return VDA_KEYS_CACHE
    keys = []
    if VDA_API_KEY:
        keys.append(VDA_API_KEY)
    try:
        session = await get_session()
        async with session.get(VDA_KEYS_URL, timeout=aiohttp.ClientTimeout(total=8, sock_connect=4, sock_read=6)) as response:
            if response.status == 200:
                payload = await response.json(content_type=None)
                if isinstance(payload, dict):
                    keys.extend(str(value).strip() for value in payload.values() if str(value).strip())
                elif isinstance(payload, list):
                    keys.extend(str(value).strip() for value in payload if str(value).strip())
    except Exception:
        pass
    VDA_KEYS_CACHE = list(dict.fromkeys(keys))
    return VDA_KEYS_CACHE


async def engine_vda(link: str, is_video: bool, path: str) -> str:
    """Try each VDA key in order, polling the first accepted job to completion."""
    keys = await _get_vda_keys()
    if not keys:
        return None
    session = await get_session()
    for api_key in keys:
        try:
            params = {
                "url": link,
                "format": VDA_VIDEO_FORMAT if is_video else "mp3",
                "apikey": api_key,
                "allow_extended_duration": "0",
                "no_merge": "0",
            }
            if not is_video:
                params["audio_quality"] = VDA_AUDIO_QUALITY
            async with session.get(
                f"{VDA_API_URL}/ajax/download.php",
                params=params,
                timeout=aiohttp.ClientTimeout(total=18, sock_connect=5, sock_read=12),
            ) as response:
                if response.status != 200:
                    continue
                job = await response.json(content_type=None)
            if not job.get("success"):
                continue
            download_url = job.get("url")
            progress_url = job.get("progress_url")
            job_id = job.get("id")
            if not download_url and job_id:
                progress_url = progress_url or f"{VDA_API_URL}/api/progress?id={job_id}"
                for _ in range(60):
                    await asyncio.sleep(1)
                    async with session.get(
                        progress_url,
                        timeout=aiohttp.ClientTimeout(total=10, sock_connect=4, sock_read=7),
                    ) as progress_response:
                        if progress_response.status != 200:
                            continue
                        status = await progress_response.json(content_type=None)
                    download_url = status.get("download_url") or status.get("url")
                    if download_url or str(status.get("progress")).lower() in ("error", "failed"):
                        break
            if download_url:
                result = await _download_stream(download_url, path)
                if result:
                    return result
        except Exception:
            continue
    return None


_TITLE_NOISE_RE = re.compile(
    r"\(.*?\)|\[.*?\]|\{.*?\}|official\s*(video|audio|music\s*video)?|lyrics?\s*(video)?|"
    r"full\s*(video|song|audio)|hd|4k|new\s*song|latest\s*song|video\s*song",
    re.IGNORECASE,
)


def _clean_query_for_gameover(title: str) -> str:
    """Strip common noise (Official Video, [Lyrics], HD, etc.) so the search API gets a cleaner query."""
    if not title:
        return title
    cleaned = _TITLE_NOISE_RE.sub("", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -|")
    return cleaned or title


async def resolve_gameover(query: str):
    """Cookie-less direct resolve: search text in, direct stream_url out. No file download needed."""
    if not query:
        return None
    try:
        session = await get_session()
        async with session.get(
            GAMEOVER_API_URL,
            params={"key": GAMEOVER_API_KEY, "search": query},
            timeout=aiohttp.ClientTimeout(total=10, sock_connect=4, sock_read=6),
        ) as response:
            if response.status != 200:
                return None
            data = await response.json(content_type=None)
        if isinstance(data, dict) and data.get("status") == "success" and data.get("stream_url"):
            return data
    except Exception:
        pass
    return None


async def _prefetch_gameover(vidid: str, title: str):
    """Fired in the background right after search, so download() finds it already cached = instant play."""
    try:
        persisted = await get_persisted_gameover(vidid)
        if persisted and persisted.get("stream_url"):
            GAMEOVER_CACHE[vidid] = (time.monotonic(), persisted)
            return
        resolved = await resolve_gameover(_clean_query_for_gameover(title))
        if resolved and resolved.get("stream_url"):
            GAMEOVER_CACHE[vidid] = (time.monotonic(), resolved)
            await save_persisted_gameover(vidid, resolved)
    except Exception:
        pass


async def search_youtube_api(query: str):
    """Search YouTube through the public JSON API, with a short in-process cache."""
    cache_key = " ".join(str(query).split()).lower()
    now = time.monotonic()
    cached = SEARCH_CACHE.get(cache_key)
    if cached and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]
    try:
        session = await get_session()
        async with session.get(
            YT_SEARCH_API_URL,
            params={"p": query},
            timeout=aiohttp.ClientTimeout(total=10, sock_connect=4, sock_read=7),
        ) as response:
            if response.status != 200:
                return []
            payload = await response.json(content_type=None)
        results = payload.get("results", []) if isinstance(payload, dict) else []
        SEARCH_CACHE[cache_key] = (now, results)
        return results
    except Exception:
        return []


async def get_session():
    global CLIENT_SESSION
    if CLIENT_SESSION is None or CLIENT_SESSION.closed:
        CLIENT_SESSION = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0))
    return CLIENT_SESSION

def _result_thumbnail(result, video_id):
    """Return the thumbnail belonging to the same API result/video ID."""
    raw = result.get("thumbnail")
    if isinstance(raw, dict):
        for key in ("maxres", "high", "medium", "default"):
            value = raw.get(key)
            if isinstance(value, dict) and value.get("url"):
                return value["url"].split("?")[0]
            if isinstance(value, str) and value:
                return value.split("?")[0]
    elif isinstance(raw, list):
        for value in raw:
            if isinstance(value, dict) and value.get("url"):
                return value["url"].split("?")[0]
            if isinstance(value, str) and value:
                return value.split("?")[0]
    elif isinstance(raw, str) and raw:
        return raw.split("?")[0]
    return f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"


async def _download_stream(url, path, headers=None):
    try:
        session = await get_session()
        # Total download time unlimited; a short stalled-read timeout enables quick retry.
        timeout = aiohttp.ClientTimeout(total=None, sock_connect=5, sock_read=12)
        
        async with session.get(url, headers=headers, timeout=timeout) as response:
            if response.status == 200:
                async with aiofiles.open(path, mode='wb') as f:
                    # 4MB chunks improve throughput while keeping memory bounded.
                    async for chunk in response.content.iter_chunked(4 * 1024 * 1024):
                        await f.write(chunk)
                if os.path.exists(path) and os.path.getsize(path) > 1024:
                    return path
    except:
        pass
    if os.path.exists(path):
        try: os.remove(path)
        except: pass
    return None

async def engine_shrutibots(vid_id: str, is_video: bool, path: str) -> str:
    try:
        session = await get_session()
        v_type = "video" if is_video else "audio"
        async with session.get(f"{API_URL}/download", params={"url": vid_id, "type": v_type}, timeout=5) as resp:
            if resp.status != 200: return None
            token = (await resp.json()).get("download_token")
            if not token: return None
        return await _download_stream(f"{API_URL}/stream/{vid_id}?type={v_type}&token={token}", path)
    except: return None

async def engine_xbit(vid_id: str, is_video: bool, path: str) -> str:
    if not YTPROXY_URL or not YT_API_KEY: return None
    try:
        session = await get_session()
        headers = {"x-api-key": YT_API_KEY}
        async with session.get(f"{YTPROXY_URL}/info/{vid_id}", headers=headers, timeout=5) as resp:
            if resp.status != 200: return None
            data = await resp.json()
        if data.get('status') == 'success':
            url = data['video_url'] if is_video else data['audio_url']
            return await _download_stream(url, path, headers)
    except: return None

async def engine_nexgen(vid_id: str, is_video: bool, path: str) -> str:
    if not API_KEY: return None
    try:
        url = f"{VIDEO_API_URL}/video/{vid_id}?api={API_KEY}" if is_video else f"{API_URL}/song/{vid_id}?api={API_KEY}"
        session = await get_session()
        async with session.get(url, timeout=5) as resp:
            if resp.status != 200: return None
            data = await resp.json()
            if data.get("status", "").lower() == "done" and data.get("link"):
                return await _download_stream(data.get("link"), path)
    except: return None


async def engine_shuvo(link: str, is_video: bool, path: str) -> str:
    SHUVO_API = "https://youtube-api-all-in-one-by-shuvo.onrender.com"
    SHUVO_KEY = "SHUVO-apis"
    try:
        import json as _json
        session = await get_session()
        headers = {"X-API-Key": SHUVO_KEY, "Content-Type": "application/json"}
        endpoint = "/api/download" if is_video else "/api/audio"
        payload = _json.dumps({"url": link}).encode()
        async with session.post(
            f"{SHUVO_API}{endpoint}", data=payload, headers=headers,
            timeout=aiohttp.ClientTimeout(total=25)
        ) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
        dl_url = (
            data.get("download_url") or data.get("audio_url") or
            data.get("url") or data.get("link") or
            (data.get("data") or {}).get("download_url") or
            (data.get("data") or {}).get("url")
        )
        if dl_url:
            return await _download_stream(dl_url, path)
    except Exception:
        pass
    return None

async def engine_cookie(link: str, is_video: bool, path: str) -> str:
    """Try yt-dlp with the owner-configured cookies file first."""
    cookie_file = await fetch_cookie_file()
    if not cookie_file:
        return None
    loop = asyncio.get_running_loop()

    def cookie_download():
        options = {
            "format": (
                "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                if is_video else "bestaudio/best"
            ),
            "outtmpl": path,
            "cookiefile": cookie_file,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "retries": 2,
            "fragment_retries": 2,
            "merge_output_format": "mp4" if is_video else None,
        }
        if not is_video:
            options["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": VDA_AUDIO_QUALITY,
                }
            ]
        options = {key: value for key, value in options.items() if value is not None}
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([link])

    try:
        await loop.run_in_executor(None, cookie_download)
    except Exception:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
        return None
    return path if os.path.exists(path) and os.path.getsize(path) > 1024 else None


async def _core_download(link: str, is_video: bool) -> str:
    vid_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link.split("/")[-1].split("?")[0]
    ext = "mp4" if is_video else "mp3"
    final_path = os.path.join(DOWNLOAD_DIR, f"{vid_id}.{ext}")

    if os.path.exists(final_path) and os.path.getsize(final_path) > 1024:
        return final_path

    # Owner cookies are tried first; all failures fall through to the API engines.
    cookie_path = await engine_cookie(link, is_video, f"{final_path}_cookie")
    if cookie_path and os.path.exists(cookie_path):
        try:
            os.rename(cookie_path, final_path)
            return final_path
        except OSError:
            return cookie_path

    vda_path = await engine_vda(link, is_video, f"{final_path}_vda")
    if vda_path and os.path.exists(vda_path):
        try:
            os.rename(vda_path, final_path)
            return final_path
        except OSError:
            return vda_path

    # Keep the existing API engines as non-cookie fallbacks.
    tasks = [
        asyncio.create_task(engine_shuvo(link, is_video, f"{final_path}_shuvo")),
        asyncio.create_task(engine_shrutibots(vid_id, is_video, f"{final_path}_shruti")),
        asyncio.create_task(engine_xbit(vid_id, is_video, f"{final_path}_xbit")),
        asyncio.create_task(engine_nexgen(vid_id, is_video, f"{final_path}_nexgen")),
    ]
    winner = None
    for future in asyncio.as_completed(tasks):
        try:
            res = await future
            if res:
                winner = res
                for task in tasks:
                    task.cancel()
                break
        except Exception:
            pass
    if winner and os.path.exists(winner):
        try:
            os.rename(winner, final_path)
            return final_path
        except OSError:
            return winner

    loop = asyncio.get_running_loop()
    def fallback_ytdl():
        opts = {
            "format": "best[height<=480]/best" if is_video else "bestaudio/best",
            "outtmpl": final_path,
            "quiet": True,
            "nocheckcertificate": True,
            "no_warnings": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        }
        yt_dlp.YoutubeDL(opts).download([link])

    try:
        await loop.run_in_executor(None, fallback_ytdl)
    except Exception:
        return None
    return final_path if os.path.exists(final_path) and os.path.getsize(final_path) > 1024 else None

async def download_song(link: str) -> str:
    return await _core_download(link, is_video=False)

async def download_video(link: str) -> str:
    return await _core_download(link, is_video=True)


async def get_exact_video_info(video_id: str):
    """Resolve one exact YouTube ID with cookies first and API fallback second."""
    video_id = str(video_id or "").strip()
    cached = VIDEO_INFO_CACHE.get(video_id)
    if cached and time.monotonic() - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,}", video_id):
        return None
    link = f"https://www.youtube.com/watch?v={video_id}"
    cookie_file = await fetch_cookie_file()
    loop = asyncio.get_running_loop()

    def extract_exact():
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        }
        if cookie_file:
            options["cookiefile"] = cookie_file
        with yt_dlp.YoutubeDL(options) as ydl:
            return ydl.extract_info(link, download=False)

    data = None
    try:
        data = await loop.run_in_executor(None, extract_exact)
    except Exception:
        data = None

    if data and data.get("id") == video_id:
        duration_seconds = int(data.get("duration") or 0)
        mins, secs = divmod(duration_seconds, 60)
        result = {
            "videoId": video_id,
            "title": data.get("title") or "Unknown",
            "durationText": f"{mins:02d}:{secs:02d}",
            "durationSeconds": duration_seconds,
            "thumbnail": data.get("thumbnail") or f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            "viewCount": data.get("view_count") or "Unknown",
            "channelTitle": data.get("uploader") or data.get("channel") or "YouTube",
            "channelUrl": data.get("channel_url") or "https://www.youtube.com",
            "publishedAt": data.get("upload_date") or "Unknown",
            "watchUrl": link,
        }
        VIDEO_INFO_CACHE[video_id] = (time.monotonic(), result)
        return result

    # Cookie/yt-dlp failure: use the API only if it returns the same exact ID.
    for result in await search_youtube_api(video_id):
        if str(result.get("videoId", "")) == video_id:
            VIDEO_INFO_CACHE[video_id] = (time.monotonic(), result)
            return result
    return None


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message: messages.append(message_1.reply_to_message)
        for msg in messages:
            for ent in (msg.entities or []):
                if ent.type == MessageEntityType.URL: return (msg.text or msg.caption)[ent.offset : ent.offset + ent.length]
            for ent in (msg.caption_entities or []):
                if ent.type == MessageEntityType.TEXT_LINK: return ent.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        # Direct YouTube URL — resolve the exact ID with cookies first.
        if re.search(self.regex, link):
            try:
                direct_id = link.split("v=")[-1].split("&")[0]
                exact = await get_exact_video_info(direct_id)
                if exact:
                    vid = exact.get("videoId") or direct_id
                    dur_sec = int(exact.get("durationSeconds") or 0)
                    dur_min = exact.get("durationText") or "00:00"
                    thumbnail = exact.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                    return exact.get("title", "Unknown"), dur_min, dur_sec, thumbnail, vid
            except Exception:
                pass  # fallback to search below
        search_results = await search_youtube_api(link)
        if not search_results:
            raise ValueError("No YouTube results found")
        result = search_results[0]
        title = result.get("title", "Unknown")
        duration_min = result.get("durationText") or "00:00"
        vidid = result.get("videoId")
        thumbnail = _result_thumbnail(result, vidid) if vidid else ""
        if not vidid:
            raise ValueError("Search result has no video ID")
        duration_sec = int(result.get("durationSeconds") or time_to_seconds(duration_min)) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[0]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[1]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        return (await self.details(link, videoid))[3]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        try:
            res = await download_video(link)
            return (1, res) if res else (0, "Video download failed")
        except Exception as e:
            return 0, f"Video download error: {e}"

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
        if "&" in link: link = link.split("&")[0]
        try:
            videos = (await Playlist.get(link)).get("videos") or []
            return [data["id"] for data in videos[:limit] if data and data.get("id")]
        except: return []

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        # Direct YouTube URL — resolve the exact ID with cookies first.
        if re.search(self.regex, link):
            try:
                direct_id = link.split("v=")[-1].split("&")[0]
                exact = await get_exact_video_info(direct_id)
                if exact:
                    vid = exact.get("videoId") or direct_id
                    return {
                        "title": exact.get("title", "Unknown"),
                        "link": exact.get("watchUrl") or f"https://www.youtube.com/watch?v={vid}",
                        "vidid": vid,
                        "duration_min": exact.get("durationText") or "00:00",
                        "thumb": exact.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    }, vid
            except Exception:
                pass  # fallback to search below
        search_results = await search_youtube_api(link)
        if not search_results:
            raise ValueError("No YouTube results found")
        result = search_results[0]
        vidid = result.get("videoId")
        if not vidid:
            raise ValueError("Search result has no video ID")
        thumb = _result_thumbnail(result, vidid)
        duration_text = result.get("durationText") or "00:00"
        cached_info = {
            "videoId": vidid,
            "title": result.get("title", "Unknown"),
            "durationText": duration_text,
            "durationSeconds": int(result.get("durationSeconds") or time_to_seconds(duration_text)),
            "thumbnail": thumb.split("?")[0],
            "watchUrl": result.get("watchUrl") or f"https://www.youtube.com/watch?v={vidid}",
        }
        VIDEO_INFO_CACHE[vidid] = (time.monotonic(), cached_info)
        # Pre-resolve the cookie-less GameOver stream in the background so download() is instant later.
        asyncio.create_task(_prefetch_gameover(vidid, cached_info["title"]))
        return {
            "title": cached_info["title"],
            "link": cached_info["watchUrl"],
            "vidid": vidid,
            "duration_min": duration_text,
            "thumb": cached_info["thumbnail"],
        }, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        base_fmt_opts = {"quiet": True, "no_warnings": True, "extractor_args": {"youtube": {"player_client": ["android", "web"]}}, }
        cookie_file = await fetch_cookie_file()
        if cookie_file:
            base_fmt_opts["cookiefile"] = cookie_file
        try:
            with yt_dlp.YoutubeDL(base_fmt_opts) as ydl:
                info = ydl.extract_info(link, download=False)
        except Exception:
            with yt_dlp.YoutubeDL(base_fmt_opts) as ydl:
                info = ydl.extract_info(link, download=False)
        return [{"format": f["format"], "filesize": f.get("filesize"), "format_id": f["format_id"], "ext": f["ext"], "format_note": f.get("format_note"), "yturl": link} for f in info["formats"] if "dash" not in str(f.get("format", "")).lower()], link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        if "&" in link: link = link.split("&")[0]
        results = await search_youtube_api(link)
        if not results or query_type >= len(results):
            raise ValueError("No YouTube results found")
        res = results[query_type]
        thumb = _result_thumbnail(res, res["videoId"])
        return res.get("title", "Unknown"), res.get("durationText") or "00:00", thumb, res["videoId"]

    async def download(
        self, link: str, mystic, video: Union[bool, str] = None, videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None, songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None, title: Union[bool, str] = None,
    ) -> str:
        if videoid: link = self.base + link
        
        is_video = bool(video)
        vid_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link.split("/")[-1].split("?")[0]

        # GameOver direct API — check the background-prefetched cache first (instant, no extra round-trip).
        if not is_video:
            cached = GAMEOVER_CACHE.get(vid_id)
            if cached and time.monotonic() - cached[0] < CACHE_TTL_SECONDS:
                stream_url = cached[1].get("stream_url")
                if stream_url:
                    return stream_url, False
            # In-memory cache expired/missing — check the persistent (mongodb) cache before calling the API again.
            persisted = await get_persisted_gameover(vid_id)
            if persisted and persisted.get("stream_url"):
                GAMEOVER_CACHE[vid_id] = (time.monotonic(), persisted)
                return persisted["stream_url"], False

        title_text = None
        duration_sec = 0
        is_live = False
        try:
            title_text, _, duration_sec, _, _ = await self.details(link)
        except:
            is_live = True

        # GameOver direct API — cookie-less, search-based resolve straight to a playable stream_url.
        if not is_video:
            try:
                query = _clean_query_for_gameover(title_text) or vid_id
                resolved = await resolve_gameover(query)
                if resolved and resolved.get("stream_url"):
                    GAMEOVER_CACHE[vid_id] = (time.monotonic(), resolved)
                    await save_persisted_gameover(vid_id, resolved)
                    return resolved["stream_url"], False
            except Exception:
                pass

        # <emoji id='5258203794772085854'>⚡</emoji> 1 HOUR LIMIT BYPASS (>3600 sec)
        if is_live or duration_sec == 0 or duration_sec > 3600:
            # Cookies-first direct URL resolution for live/long videos.
            cookie_file = await fetch_cookie_file()
            if cookie_file:
                try:
                    loop = asyncio.get_running_loop()

                    def extract_cookie_direct_url():
                        cookie_opts = {
                            "quiet": True,
                            "no_warnings": True,
                            "skip_download": True,
                            "noplaylist": True,
                            "cookiefile": cookie_file,
                            "format": "best[height<=720]/best" if is_video else "bestaudio/best",
                            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
                        }
                        with yt_dlp.YoutubeDL(cookie_opts) as ydl:
                            info = ydl.extract_info(link, download=False)
                            return info.get("url") or (info.get("formats") or [{}])[-1].get("url")

                    cookie_direct_url = await loop.run_in_executor(None, extract_cookie_direct_url)
                    if cookie_direct_url:
                        return cookie_direct_url, False
                except Exception:
                    pass

            try:
                session = await get_session()
                async with session.get(f"{YTPROXY_URL}/info/{vid_id}", headers={"x-api-key": YT_API_KEY}, timeout=3) as r:
                    if r.status == 200:
                        data = await r.json()
                        stream_url = data.get('video_url') if is_video else data.get('audio_url')
                        if stream_url: return stream_url, False 
            except: pass
            
            loop = asyncio.get_running_loop()
            def extract_direct_url():
                format_str = "best[height<=480]/best" if is_video else "bestaudio/best"
                base_opts = {
                    "quiet": True, "no_warnings": True,
                    "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
                    "format": format_str,
                }
                # VPS pe bina cookies android client kaam karta hai
                try:
                    with yt_dlp.YoutubeDL(base_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        url = info.get("url") or (info.get("formats") or [{}])[-1].get("url")
                        if url: return url
                except Exception:
                    pass
                # Fallback without cookies; VDA handles authenticated downloads.
                try:
                    with yt_dlp.YoutubeDL(base_opts) as ydl:
                        info = ydl.extract_info(link, download=False)
                        return info.get("url") or (info.get("formats") or [{}])[-1].get("url")
                except Exception:
                    return None


            
            try:
                direct_url = await loop.run_in_executor(None, extract_direct_url)
                if direct_url: return direct_url, False
            except: pass

        # <emoji id='5258203794772085854'>⚡</emoji> REGULAR DOWNLOAD (Chunk mode for Zero Error)
        try:
            res = await _core_download(link, is_video)
            return (res, True) if res else (None, False)
        except:
            return None, False