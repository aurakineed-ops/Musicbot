Yoru Music Bot — GitHub Cookies Source Backup

This backup contains the bot source and configuration used with the automatic GitHub cookies indirection source.

The source URL is stored in config.py under COOKIES_URL. The file at that source contains the current cookies URL; changing that remote file allows cookie rotation without changing the bot source.

This backup intentionally excludes .env, tokens, MongoDB credentials, session strings, downloaded media, cookie files, logs, virtual environments, caches, and other private runtime data.

To restore, extract the archive into a clean Yoru Music Bot source directory, restore secrets separately in .env, install dependencies, and start the bot with the normal launcher.
