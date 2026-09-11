# Yoru Music Bot

Private backup of the Yoru Music Bot source. The project includes Telegram music playback, YouTube search and download paths, API-first audio resolving, stream controls, and the simple Yoru AI command module.

## Backup safety

Runtime secrets are intentionally excluded from this repository. Do not commit `.env`, bot tokens, MongoDB connection strings, session files, cookies, downloaded media, logs, or virtual environments. Configure those values separately on the VPS using the existing private environment file.

Audio playback uses the configured GameOver resolver API directly and does not fetch YouTube cookies. Set `GAMEOVER_API_URL` and `GAMEOVER_API_KEY` in the private environment before starting the bot; see `.env.example`.

## Simple AI commands

The simple AI module supports `/ask`, `/chatgpt`, and `/yoru`. It uses the configured Yoru personality and does not register a broad group-message listener.

## Restore overview

Extract the repository into a clean bot directory, restore private environment values separately, install the dependencies from `requirements.txt`, and start the bot with the VPS launcher. Never place production secrets into the repository.
