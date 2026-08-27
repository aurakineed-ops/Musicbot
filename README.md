# Aaliya Music Bot

Private backup of the Aaliya Music Bot source. The project includes Telegram music playback, YouTube search and download paths, cookies-first YouTube handling with API fallbacks, stream controls, and the simple Aaliya AI command module.

## Backup safety

Runtime secrets are intentionally excluded from this repository. Do not commit `.env`, bot tokens, MongoDB connection strings, session files, cookies, downloaded media, logs, or virtual environments. Configure those values separately on the VPS using the existing private environment file.

The YouTube cookies source is configured through `COOKIES_URL` in `config.py` and points to the GitHub indirection source used for cookie rotation. The remote indirection file can be updated without changing this code backup.

## Simple AI commands

The simple AI module supports `/ask`, `/chatgpt`, and `/aaliya`. It uses the configured Aaliya personality and does not register a broad group-message listener.

## Restore overview

Extract the repository into a clean bot directory, restore private environment values separately, install the dependencies from `requirements.txt`, and start the bot with the VPS launcher. Never place production secrets into the repository.
