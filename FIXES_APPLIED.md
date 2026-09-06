# Music bot fixes

This build includes fixes for:

- HTML Telegram mentions being sent with Markdown parsing.
- Reply-based `gntag` and `hitag` commands never entering reply mode.
- `/mention` batches and leftover members.
- Broken text escaping in `tagall`.
- Invalid member names and malformed emoji links.
- Stale tagging state after Telegram/API errors.
- Duplicate `/all`, `/cancel`, `/stop`, and `/admins` command handlers.
- Filter handling for unsupported media, missing database records, and multiple matches.
- Race-prone manually generated filter document IDs.

The archive intentionally does not include `.env`, `.env.bak`, or the Git
metadata directory. Configure secrets through the deployment environment.