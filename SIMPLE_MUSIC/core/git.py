# -----------------------------------------------
# Yoru Music Bot — local source protection
# -----------------------------------------------
"""Disable upstream self-updates so uploaded source is never overwritten."""

import asyncio
import shlex
from typing import Tuple

from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    """Keep the uploaded Yoru Music Bot source unchanged."""
    LOGGER(__name__).info("GitHub upstream updates disabled; using uploaded source.")
    return
