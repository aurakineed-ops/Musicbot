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
import hashlib
import os
from datetime import datetime, timedelta
from typing import Union
from ntgcalls import ConnectionNotFound, TelegramServerError
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import PyTgCalls, exceptions, types
from pytgcalls.pytgcalls_session import PyTgCallsSession
import config
from SIMPLE_MUSIC import LOGGER, YouTube, app
from SIMPLE_MUSIC.misc import db
from SIMPLE_MUSIC.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_lang,
    get_loop,
    group_assistant,
    is_autoend,
    is_autoplay,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from SIMPLE_MUSIC.utils.exceptions import AssistantErr
from SIMPLE_MUSIC.utils.formatters import check_duration, seconds_to_min, speed_converter
from SIMPLE_MUSIC.utils.inline.play import stream_markup, stream_caption
from SIMPLE_MUSIC.utils.stream.autoclear import auto_clean
from SIMPLE_MUSIC.utils.thumbnails import get_thumb as gen_thumb
from strings import get_string

autoend = {}
counter = {}

async def _clear_(chat_id: int):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)

class Call(PyTgCalls):
    def __init__(self):
        PyTgCallsSession.notice_displayed = True

        self.userbot1 = Client(
            name="SIMPLEAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            name="SIMPLEAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            name="SIMPLEAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            name="SIMPLEAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            name="SIMPLEAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    def _build_stream(
        self,
        source: str,
        video: bool,
        ffmpeg: str | None = None,
    ) -> types.MediaStream:
        # Reconnect flags: if the remote CDN (GameOver stream_url etc.) has a
        # brief network hiccup, ffmpeg reconnects and keeps feeding audio
        # instead of the stream stalling/buffering. Harmless no-op for local
        # files. Any caller-supplied ffmpeg params (seek etc.) are appended
        # after these so both keep working together.
        reconnect = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_at_eof 1"
        combined_ffmpeg = f"{reconnect} {ffmpeg}" if ffmpeg else reconnect
        return types.MediaStream(
            media_path=source,
            audio_parameters=types.AudioQuality.HIGH,
            video_parameters=types.VideoQuality.HD_720p,
            audio_flags=types.MediaStream.Flags.REQUIRED,
            video_flags=(
                types.MediaStream.Flags.AUTO_DETECT
                if video
                else types.MediaStream.Flags.IGNORE
            ),
            ffmpeg_parameters=combined_ffmpeg,
        )

    async def _play_on_assistant(
        self,
        client: PyTgCalls,
        chat_id: int,
        stream: types.MediaStream,
    ):
        try:
            await client.play(
                chat_id=chat_id,
                stream=stream,
                config=types.GroupCallConfig(auto_start=False),
            )
        except exceptions.NoActiveGroupCall:
            raise
        except exceptions.NoAudioSourceFound:
            raise
        except (ConnectionNotFound, TelegramServerError):
            raise
        except Exception:
            raise

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_call(chat_id, close=False)
        except Exception:
            pass

    async def stop_stream_force(self, chat_id: int):
        for string, client in [
            (config.STRING1, self.one),
            (config.STRING2, self.two),
            (config.STRING3, self.three),
            (config.STRING4, self.four),
            (config.STRING5, self.five),
        ]:
            if not string:
                continue
            try:
                await client.leave_call(chat_id, close=False)
            except Exception:
                pass
        try:
            await _clear_(chat_id)
        except Exception:
            pass

    async def speedup_stream(self, chat_id: int, file_path, speed, playing):
        assistant = await group_assistant(self, chat_id)
        if str(speed) != "1.0":
            base = os.path.basename(file_path)
            chatdir = os.path.join(os.getcwd(), "playback", str(speed))
            if not os.path.isdir(chatdir):
                os.makedirs(chatdir)
            out = os.path.join(chatdir, base)
            if not os.path.isfile(out):
                if str(speed) == "0.5":
                    vs = 2.0
                elif str(speed) == "0.75":
                    vs = 1.35
                elif str(speed) == "1.5":
                    vs = 0.68
                elif str(speed) == "2.0":
                    vs = 0.5
                else:
                    vs = 1.0
                proc = await asyncio.create_subprocess_shell(
                    cmd=(
                        "ffmpeg "
                        "-i "
                        f"{file_path} "
                        "-filter:v "
                        f"setpts={vs}*PTS "
                        "-filter:a "
                        f"atempo={speed} "
                        f"{out}"
                    ),
                    stdin=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await proc.communicate()
        else:
            out = file_path
        dur = await asyncio.get_event_loop().run_in_executor(None, check_duration, out)
        dur = int(dur)
        played, con_seconds = speed_converter(playing[0]["played"], speed)
        duration = seconds_to_min(dur)
        xx = f"-ss {played} -to {duration}"
        video_mode = playing[0]["streamtype"] == "video"
        stream = self._build_stream(out, video=video_mode, ffmpeg=xx)
        if str(db[chat_id][0]["file"]) == str(file_path):
            await self._play_on_assistant(assistant, chat_id, stream)
        else:
            raise AssistantErr("Umm")
        if str(db[chat_id][0]["file"]) == str(file_path):
            exis = (playing[0]).get("old_dur")
            if not exis:
                db[chat_id][0]["old_dur"] = db[chat_id][0]["dur"]
                db[chat_id][0]["old_second"] = db[chat_id][0]["seconds"]
            db[chat_id][0]["played"] = con_seconds
            db[chat_id][0]["dur"] = duration
            db[chat_id][0]["seconds"] = dur
            db[chat_id][0]["speed_path"] = out
            db[chat_id][0]["speed"] = speed

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except Exception:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_call(chat_id, close=False)
        except Exception:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        stream = self._build_stream(link, video=bool(video))
        await self._play_on_assistant(assistant, chat_id, stream)

    async def try_autoplay_on_empty(self, chat_id: int, popped: dict) -> bool:
        """Call this whenever a manual action (skip/stop/etc.) just emptied the
        queue, BEFORE leaving the call — lets /autoplay keep the music going
        the same way it does when a song ends naturally. Returns True if it
        picked up and is now playing something (caller should NOT leave)."""
        if not popped:
            LOGGER(__name__).warning(f"[autoplay] try_autoplay_on_empty: no 'popped' entry for chat {chat_id}")
            return False
        if not await is_autoplay(chat_id):
            LOGGER(__name__).info(f"[autoplay] disabled for chat {chat_id}, not attempting")
            return False
        try:
            assistant = await group_assistant(self, chat_id)
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] group_assistant lookup failed for chat {chat_id}")
            return False
        result = await self._autoplay_next(assistant, chat_id, popped)
        LOGGER(__name__).info(f"[autoplay] try_autoplay_on_empty result for chat {chat_id}: {result}")
        return result

    async def show_no_more_songs_card(self, chat_id: int, popped: dict):
        """Queue is empty and autoplay didn't/couldn't pick anything up —
        instead of leaving immediately, stay connected and show a card with
        a one-tap Autoplay button that searches + plays right away."""
        original_chat_id = (popped or {}).get("chat_id") or chat_id
        self._pending_seed[chat_id] = {
            "title": (popped or {}).get("title") or "",
            "vidid": (popped or {}).get("vidid"),
            "chat_id": original_chat_id,
            "user_id": (popped or {}).get("user_id") or 0,
        }
        try:
            await app.send_message(
                original_chat_id,
                "<blockquote><emoji id='6147943438785449262'>🎵</emoji> <b>Nᴏ Mᴏʀᴇ Sᴏɴɢs ɪɴ ᴛʜᴇ Qᴜᴇᴜᴇ</b>\n"
                "ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ ʜᴀs ᴇɴᴅᴇᴅ — ʜɪᴛ ᴀᴜᴛᴏᴘʟᴀʏ ᴛᴏ ᴋᴇᴇᴘ ᴛʜᴇ ᴍᴜsɪᴄ ɢᴏɪɴɢ.</blockquote>",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(
                        text="Aᴜᴛᴏᴩʟᴀʏ",
                        callback_data=f"autoplay_search_now {chat_id}",
                        **({"icon_custom_emoji_id": "5258334469152054985"} if getattr(config, "BUTTON_ICON", False) else {}),
                    )]]
                ),
            )
        except Exception:
            pass

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        ffmpeg = f"-ss {to_seek} -to {duration}"
        video_mode = mode == "video"
        stream = self._build_stream(
            file_path,
            video=video_mode,
            ffmpeg=ffmpeg,
        )
        await self._play_on_assistant(assistant, chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        stream = self._build_stream(link, video=True)
        await self._play_on_assistant(assistant, config.LOG_GROUP_ID, stream)
        await asyncio.sleep(0.2)
        try:
            await assistant.leave_call(config.LOG_GROUP_ID, close=False)
        except Exception:
            pass

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)
        stream = self._build_stream(link, video=bool(video))
        try:
            await self._play_on_assistant(assistant, chat_id, stream)
        except exceptions.NoActiveGroupCall:
            raise AssistantErr(_["call_8"])
        except exceptions.NoAudioSourceFound:
            raise AssistantErr(_["call_10"])
        except (ConnectionNotFound, TelegramServerError):
            raise AssistantErr(_["call_10"])
        except Exception:
            raise AssistantErr(_["call_10"])
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=1)

    _autoplay_history: dict = {}
    _autoplay_reserved: dict = {}  # chat_id -> True once the next song is already queued ahead of time
    _pending_seed: dict = {}       # chat_id -> {"title","vidid","chat_id","user_id"} of the last song, kept for the "No More Songs" card's Autoplay button
    _autoplay_pool: dict = {}      # chat_id -> {"tracks": [...], "index": 0, "limit": 0}

    async def _pick_related_track(self, chat_id: int, seed_vidid: str):
        """Primary picker: YouTube's own Mix/Radio list for the last played
        video (real algorithmic 'up next', not a keyword search) — far less
        prone to looping back over the same handful of songs than searching
        the current title over and over."""
        from SIMPLE_MUSIC.platforms.Youtube import get_related_videos, get_exact_video_info
        import random as _random

        if not seed_vidid or seed_vidid.startswith("ga_"):
            return None  # no real YouTube ID to seed a Mix from

        history = self._autoplay_history.setdefault(chat_id, [])
        try:
            related = await get_related_videos(seed_vidid) or []
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] get_related_videos('{seed_vidid}') failed")
            related = []

        candidates = [r for r in related if r.get("videoId") and r["videoId"] not in history]
        if not candidates:
            return None  # don't fall back to repeats — let the caller try the next tier

        pool = candidates[:5]
        _random.shuffle(pool)
        for pick in pool:
            vidid = pick["videoId"]
            try:
                info = await get_exact_video_info(vidid)
            except Exception:
                info = None
            title = (info or {}).get("title") or pick.get("title") or "Autoplay"
            duration = (info or {}).get("durationText") or "00:00"
            try:
                file_path, _direct = await YouTube.download(vidid, None, videoid=True, video=None)
            except Exception:
                LOGGER(__name__).exception(f"[autoplay] download failed for related '{title}' ({vidid})")
                continue
            if not file_path:
                continue
            history.append(vidid)
            history[:] = history[-15:]  # keep last 15 so a full session doesn't repeat too soon
            return {
                "title": title,
                "duration": duration,
                "stream_url": file_path,
                "vidid": vidid,
                "thumbnail": None,
            }
        return None

    async def _pick_search_track(self, chat_id: int, seed_title: str):
        """Secondary picker: plain title search (own search API, real
        video_ids), used only when the Mix has nothing fresh left."""
        from SIMPLE_MUSIC.platforms.Youtube import search_youtube_api
        import random as _random

        history = self._autoplay_history.setdefault(chat_id, [])
        clean_seed = " ".join(str(seed_title or "").split())
        try:
            results = await search_youtube_api(clean_seed) or []
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] search_youtube_api('{clean_seed}') failed")
            results = []

        candidates = [r for r in results if r.get("videoId") and r["videoId"] not in history]
        if not candidates:
            # Every result overlaps recent history — do NOT ignore history
            # just to force a pick; that's exactly what causes repeats.
            # Let the caller fall through to the playlist pool instead.
            return None

        pool = candidates[:5]
        _random.shuffle(pool)
        for pick in pool:
            vidid = pick["videoId"]
            title = pick.get("title") or "Autoplay"
            duration = pick.get("durationText") or "00:00"
            try:
                file_path, _direct = await YouTube.download(vidid, None, videoid=True, video=None)
            except Exception:
                LOGGER(__name__).exception(f"[autoplay] download failed for '{title}' ({vidid})")
                continue
            if not file_path:
                continue
            history.append(vidid)
            history[:] = history[-15:]  # keep last 15 so a full session doesn't repeat too soon
            return {
                "title": title,
                "duration": duration,
                "stream_url": file_path,
                "vidid": vidid,
                "thumbnail": None,
            }
        return None

    async def _pick_next_track(self, chat_id: int, seed_title: str, seed_vidid: str = None):
        """YouTube Mix (real algorithmic related-videos) first, then a plain
        title search, then the endless curated playlist pool — each tier only
        used when the one before it has nothing fresh left, so autoplay never
        simply stops AND never has to fall back to repeating something."""
        track = await self._pick_related_track(chat_id, seed_vidid)
        if track:
            return track
        track = await self._pick_search_track(chat_id, seed_title)
        if track:
            return track
        LOGGER(__name__).info(f"[autoplay] no fresh Mix/search candidates, falling back to playlist pool for chat {chat_id}")
        return await self._pick_pool_track(chat_id)

    async def _ensure_autoplay_pool(self, chat_id: int):
        """Keeps a big batch of tracks (real video_id + resolve_url each) pulled
        straight from a curated playlist. When running low, re-fetches the SAME
        playlist with a bigger `limit` — that just returns more tracks from it,
        so the pool can never run dry, no matter how long autoplay runs."""
        from SIMPLE_MUSIC.platforms.Youtube import gameover_playlist

        pool = self._autoplay_pool.setdefault(chat_id, {"tracks": [], "index": 0, "limit": 0})
        remaining = len(pool["tracks"]) - pool["index"]
        if remaining > 3:
            return pool
        new_limit = pool["limit"] + config.GAMEOVER_AUTOPLAY_BATCH_SIZE
        try:
            tracks = await gameover_playlist(config.GAMEOVER_AUTOPLAY_PLAYLIST, new_limit)
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] gameover_playlist(limit={new_limit}) failed for chat {chat_id}")
            tracks = []
        if tracks:
            pool["tracks"] = tracks
            pool["limit"] = new_limit
        elif not pool["tracks"]:
            LOGGER(__name__).warning(f"[autoplay] playlist pool fetch returned nothing for chat {chat_id}")
        return pool

    _NOISE_WORDS = {
        "official", "video", "audio", "lyrics", "lyric", "music", "ft", "feat",
        "featuring", "hd", "hq", "the", "a", "an", "mv", "visualizer", "song",
        "prod", "remix", "version", "edit",
    }

    def _titles_relate(self, title_a: str, title_b: str) -> bool:
        """Loose sanity check: do these two titles share at least one real
        keyword? Guards against the resolve API silently substituting an
        unrelated track for a blocked/unavailable one."""
        def keywords(t):
            words = "".join(c if c.isalnum() else " " for c in t.lower()).split()
            return {w for w in words if len(w) > 2 and w not in self._NOISE_WORDS}

        a, b = keywords(title_a), keywords(title_b)
        if not a or not b:
            return True  # not enough to judge — don't block on it
        return bool(a & b)

    async def _pick_pool_track(self, chat_id: int):
        """Pull the next fresh track out of the pool and resolve it to a
        playable stream_url. Real video_id in, so thumbnails/captions work
        exactly like a normal YouTube song."""
        from SIMPLE_MUSIC.platforms.Youtube import resolve_gameover_by_url

        history = self._autoplay_history.setdefault(chat_id, [])
        for _attempt in range(60):  # safety cap so a stuck pool can't loop forever
            pool = await self._ensure_autoplay_pool(chat_id)
            tracks = pool["tracks"]
            if pool["index"] >= len(tracks):
                LOGGER(__name__).warning(f"[autoplay] pool exhausted and could not grow for chat {chat_id}")
                return None
            track = tracks[pool["index"]]
            pool["index"] += 1

            vidid = track.get("video_id")
            norm_title = " ".join(str(track.get("title") or "").split()).lower()
            if not vidid or vidid in history:
                continue
            resolve_url = track.get("resolve_url")
            if not resolve_url:
                continue
            try:
                resolved = await resolve_gameover_by_url(resolve_url)
            except Exception:
                LOGGER(__name__).exception(f"[autoplay] resolve failed for '{track.get('title')}'")
                continue
            if resolved and resolved.get("stream_url"):
                confirmed_title = resolved.get("title") or track.get("title") or "Autoplay"
                if norm_title and not self._titles_relate(norm_title, confirmed_title):
                    LOGGER(__name__).warning(
                        f"[autoplay] resolve mismatch, skipping: wanted '{track.get('title')}' got '{confirmed_title}'"
                    )
                    continue
                history.append(vidid)
                history[:] = history[-15:]  # keep last 15 so a full session doesn't repeat too soon
                # Use what the resolve engine actually confirms it fetched —
                # not the playlist's guess — so the caption never shows a
                # different song than what's really playing.
                confirmed_duration = resolved.get("duration") or track.get("duration") or "00:00"
                return {
                    "title": confirmed_title,
                    "duration": confirmed_duration,
                    "stream_url": resolved["stream_url"],
                    "vidid": vidid,
                    "thumbnail": None,
                }
        LOGGER(__name__).warning(f"[autoplay] gave up after 60 candidates for chat {chat_id}")
        return None

    def _reserved_card(self, index: int, title: str, duration: str, requester: str) -> str:
        return (
            "<blockquote>🎉 <b>TRACK RESERVED — PLAYING SOON : #{idx}</b>\n\n"
            "🎵 <b>SONG :</b> {title}\n"
            "⏱ <b>LENGTH :</b> {dur} MINS\n"
            "🙋 <b>REQUESTER :</b> {req}\n\n"
            "💃 GET READY! YOUR SONG IS COMING UP NEXT.</blockquote>"
        ).format(idx=index, title=title[:60], dur=duration, req=requester)

    async def reserve_next_autoplay(self, chat_id: int, original_chat_id: int, seed_title: str, requester: str = "Autoplay", seed_vidid: str = None):
        """Proactively fetch + queue ONE autoplay song ahead of time while the
        current song is still playing, so there's zero gap between tracks."""
        from SIMPLE_MUSIC.utils.stream.queue import put_queue

        if self._autoplay_reserved.get(chat_id):
            return False
        try:
            track = await self._pick_next_track(chat_id, seed_title, seed_vidid)
            if not track:
                return False
            vidid = track["vidid"]
            await put_queue(
                chat_id, original_chat_id, track["stream_url"],
                track["title"], track["duration"], "Autoplay", vidid, 0, "audio",
                image=track.get("thumbnail"),
            )
            self._autoplay_reserved[chat_id] = True
            return True
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] reserve_next_autoplay failed for chat {chat_id}")
            return False

    async def _autoplay_next(self, client: PyTgCalls, chat_id: int, popped: dict) -> bool:
        """Fires only if a song wasn't already reserved ahead of time (fallback
        path) — picks + plays the next autoplay track immediately."""
        try:
            from SIMPLE_MUSIC.utils.stream.queue import put_queue

            seed_title = popped.get("title") or ""
            seed_vidid = popped.get("vidid")
            track = await self._pick_next_track(chat_id, seed_title, seed_vidid)
            if not track:
                return False
            vidid = track["vidid"]

            stream_obj = self._build_stream(track["stream_url"], video=False)
            try:
                await self._play_on_assistant(client, chat_id, stream_obj)
            except Exception:
                LOGGER(__name__).exception(f"[autoplay] _play_on_assistant failed for chat {chat_id}")
                return False

            original_chat_id = popped.get("chat_id")
            await put_queue(
                chat_id, original_chat_id, track["stream_url"],
                track["title"], track["duration"], "Autoplay", vidid, popped.get("user_id") or 0, "audio",
                image=track.get("thumbnail"),
            )
            db[chat_id][0]["played"] = 0
            self._autoplay_reserved[chat_id] = False

            language = await get_lang(chat_id)
            _ = get_string(language)
            title = track["title"].title()[:23]
            img = track.get("thumbnail") or await gen_thumb(vidid, title=title, duration=track["duration"])
            button = await stream_markup(_, chat_id)
            run = await app.send_photo(
                has_spoiler=True,
                chat_id=original_chat_id,
                photo=img,
                caption=stream_caption(title, track["duration"], "Autoplay"),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            return True
        except Exception:
            LOGGER(__name__).exception(f"[autoplay] _autoplay_next failed for chat {chat_id}")
            return False

    async def change_stream(self, client: PyTgCalls, chat_id: int):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            await auto_clean(popped)
            if not check:
                if popped and await is_autoplay(chat_id):
                    queued = await self._autoplay_next(client, chat_id, popped)
                    if queued:
                        return
                await _clear_(chat_id)
                await self.show_no_more_songs_card(chat_id, popped)
                return  # stay connected, idle, waiting for the Autoplay tap

        except Exception:
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id, close=False)
            except Exception:
                return
        queued = check[0]["file"]
        self._autoplay_reserved[chat_id] = False
        if len(check) == 1 and await is_autoplay(chat_id):
            asyncio.create_task(
                self.reserve_next_autoplay(chat_id, check[0]["chat_id"], check[0]["title"], "Autoplay", check[0].get("vidid"))
            )
        language = await get_lang(chat_id)
        _ = get_string(language)
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        original_chat_id = check[0]["chat_id"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        db[chat_id][0]["played"] = 0
        exis = (check[0]).get("old_dur")
        if exis:
            db[chat_id][0]["dur"] = exis
            db[chat_id][0]["seconds"] = check[0]["old_second"]
            db[chat_id][0]["speed_path"] = None
            db[chat_id][0]["speed"] = 1.0
        video = True if str(streamtype) == "video" else False
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            stream = self._build_stream(link, video=video)
            try:
                await self._play_on_assistant(client, chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            img = await gen_thumb(videoid, title=title, duration=check[0]["dur"])
            button = await stream_markup(_, chat_id)
            run = await app.send_photo(
                has_spoiler=True,
                chat_id=original_chat_id,
                photo=img,
                caption=stream_caption(title[:23], check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "vid_" in queued:
            mystic = await app.send_message(original_chat_id, _["call_7"])
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=video,
                )
            except Exception:
                return await mystic.edit_text(
                    _["call_6"], disable_web_page_preview=True
                )
            stream = self._build_stream(file_path, video=video)
            try:
                await self._play_on_assistant(client, chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            img = await gen_thumb(videoid, title=title, duration=check[0]["dur"])
            button = await stream_markup(_, chat_id)
            await mystic.delete()
            run = await app.send_photo(
                has_spoiler=True,
                chat_id=original_chat_id,
                photo=img,
                caption=stream_caption(title[:23], check[0]["dur"], user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

        elif "index_" in queued:
            stream = self._build_stream(videoid, video=video)
            try:
                await self._play_on_assistant(client, chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            button = await stream_markup(_, chat_id)
            run = await app.send_photo(
                has_spoiler=True,
                chat_id=original_chat_id,
                photo=config.STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            stream = self._build_stream(queued, video=video)
            try:
                await self._play_on_assistant(client, chat_id, stream)
            except Exception:
                return await app.send_message(
                    original_chat_id,
                    text=_["call_6"],
                )
            if videoid == "telegram":
                button = await stream_markup(_, chat_id)
                queue_image = check[0].get("image")
                run = await app.send_photo(
                    has_spoiler=True,
                    chat_id=original_chat_id,
                    photo=(
                        queue_image
                        if queue_image
                        else (
                            config.TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else config.TELEGRAM_VIDEO_URL
                        )
                    ),
                    caption=stream_caption(title[:23], check[0]["dur"], user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = await stream_markup(_, chat_id)
                run = await app.send_photo(
                    has_spoiler=True,
                    chat_id=original_chat_id,
                    photo=config.SOUNCLOUD_IMG_URL,
                    caption=stream_caption(title[:23], check[0]["dur"], user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                queue_image = check[0].get("image")
                img = queue_image if queue_image else await gen_thumb(videoid, title=title, duration=check[0]["dur"])
                button = await stream_markup(_, chat_id)
                run = await app.send_photo(
                    has_spoiler=True,
                    chat_id=original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        title[:23],
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(self.one.ping)
        if config.STRING2:
            pings.append(self.two.ping)
        if config.STRING3:
            pings.append(self.three.ping)
        if config.STRING4:
            pings.append(self.four.ping)
        if config.STRING5:
            pings.append(self.five.ping)
        return str(round(sum(pings) / len(pings), 3)) if pings else "0"

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client...\n")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
        for string, client in [
            (config.STRING1, self.one),
            (config.STRING2, self.two),
            (config.STRING3, self.three),
            (config.STRING4, self.four),
            (config.STRING5, self.five),
        ]:
            if not string:
                continue
            @client.on_update()
            async def _update_handler(_, update: types.Update, _client=client):
                if isinstance(update, types.StreamEnded):
                    if update.stream_type == types.StreamEnded.Type.AUDIO:
                        await self.change_stream(_client, update.chat_id)
                elif isinstance(update, types.ChatUpdate):
                    if update.status in [
                        types.ChatUpdate.Status.KICKED,
                        types.ChatUpdate.Status.LEFT_GROUP,
                        types.ChatUpdate.Status.CLOSED_VOICE_CHAT,
                    ]:
                        await self.stop_stream(update.chat_id)

SIMPLE = Call()