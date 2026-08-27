# Aaliya Music Bot - fixed GitHub cookies source
# ------------------------------------------------
import json
import os
import time
from urllib.parse import urlparse

import aiofiles
import aiohttp
from bs4 import BeautifulSoup

from config import COOKIES_URL as ENV_COOKIES_URL

COOKIE_DIR = os.path.join("downloads", ".cookies")
COOKIE_PATH = os.path.join(COOKIE_DIR, "youtube.cookies.txt")

# The GitHub file contains the current cookies-file URL. The URL inside that
# file can be rotated without changing this bot source or its environment.
DEFAULT_COOKIES_SOURCE = (
    "https://raw.githubusercontent.com/replitprivet-dotcom/82beos-wnw/"
    "refs/heads/main/7hwjw.txt"
)
_COOKIE_CACHE = {"source": None, "path": None, "fetched_at": 0.0}
_COOKIE_REFRESH_SECONDS = 300


def _valid_url(url: str) -> bool:
    try:
        parsed = urlparse(str(url).strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def _netscape_lines(text: str):
    return [
        line for line in text.splitlines()
        if line.strip() and (line.lstrip().startswith("#") or len(line.split("\t")) >= 7)
    ]


def _extract_cookie_data(data: bytes):
    """Extract Netscape cookies from raw text or a paste page; never execute data."""
    text = data.decode("utf-8", errors="ignore")
    candidates = [text]

    if "<html" in text[:2000].lower() or "__NEXT_DATA__" in text:
        soup = BeautifulSoup(text, "html.parser")
        next_data = soup.find("script", id="__NEXT_DATA__")
        if next_data and next_data.string:
            try:
                payload = json.loads(next_data.string)
                content = payload.get("props", {}).get("pageProps", {}).get("content")
                if isinstance(content, str):
                    candidates.append(BeautifulSoup(content, "html.parser").get_text("\n"))
            except Exception:
                pass

        for block in soup.select("pre, code"):
            candidates.append(block.get_text("\n"))

        rows = []
        for row in soup.select("tr"):
            cells = row.select("td")
            if cells:
                rows.append(cells[-1].get_text("", strip=False))
        if rows:
            candidates.append("\n".join(rows))

    for candidate in candidates:
        lines = _netscape_lines(candidate)
        if any("\t" in line and len(line.split("\t")) >= 7 for line in lines):
            return ("\n".join(lines) + "\n").encode("utf-8")
    return None


def _configured_source() -> str:
    return str(ENV_COOKIES_URL or DEFAULT_COOKIES_SOURCE).strip()


async def get_cookies_url() -> str:
    """Return the fixed GitHub source configured for automatic cookie rotation."""
    return _configured_source()


async def _fetch_bytes(session, url: str):
    async with session.get(url, allow_redirects=True) as response:
        if response.status != 200:
            return None
        return await response.read()


async def _resolve_cookie_payload(session, source_url: str):
    data = await _fetch_bytes(session, source_url)
    if not data:
        return None

    # The GitHub file is an indirection file containing one current URL.
    text = data.decode("utf-8", errors="ignore")
    nonempty = [line.strip() for line in text.splitlines() if line.strip()]
    if len(nonempty) == 1 and _valid_url(nonempty[0]) and nonempty[0] != source_url:
        data = await _fetch_bytes(session, nonempty[0])
        if not data:
            return None

    return _extract_cookie_data(data)


async def fetch_cookie_file(force: bool = False):
    """Fetch and cache a Netscape-format cookie file from the fixed source."""
    source_url = await get_cookies_url()
    if not source_url or not _valid_url(source_url):
        return None

    now = time.time()
    if (
        not force
        and _COOKIE_CACHE.get("source") == source_url
        and _COOKIE_CACHE.get("path")
        and os.path.exists(_COOKIE_CACHE["path"])
        and now - _COOKIE_CACHE.get("fetched_at", 0) < _COOKIE_REFRESH_SECONDS
    ):
        return _COOKIE_CACHE["path"]

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            cookie_data = await _resolve_cookie_payload(session, source_url)
        if not cookie_data:
            return None

        os.makedirs(COOKIE_DIR, exist_ok=True)
        async with aiofiles.open(COOKIE_PATH, "wb") as cookie_file:
            await cookie_file.write(cookie_data)
        _COOKIE_CACHE.update({"source": source_url, "path": COOKIE_PATH, "fetched_at": now})
        return COOKIE_PATH
    except Exception:
        return None


async def cookie_status(force: bool = False):
    source_url = await get_cookies_url()
    path = await fetch_cookie_file(force=force) if source_url else None
    return source_url, bool(path)


__all__ = ["get_cookies_url", "fetch_cookie_file", "cookie_status", "COOKIE_PATH"]
