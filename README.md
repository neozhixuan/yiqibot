# Wedding Telegram Reminder Bot

Small Telegram reminder bot for Railway.

## Structure

```text
main.py          # Railway entrypoint
bot/             # App modules
tests/           # Unit tests
Procfile         # Railway worker command
```

## Required env vars

Set these in a local `.env` file or in Railway Variables:

```env
BOT_TOKEN=your_telegram_bot_token
RAW_CHANNEL_ID=562953664827933
```

You can use `CHANNEL_ID=-100...` instead of `RAW_CHANNEL_ID` if you prefer the full Telegram chat id.
You can also use `CHANNEL_ID=@your_channel_username` for a public channel username.

Optional:

```env
TIMEZONE_NAME=Asia/Singapore
REMINDER_MINUTES=10
```

Railway deployment notices are sent automatically when Railway provides values like `RAILWAY_DEPLOYMENT_ID` or `RAILWAY_IMAGE`.

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Tests

```bash
python3 -m unittest discover -s tests
```

## Railway

- Keep the worker command as `python main.py`
- Add the required env vars in Railway
- Make sure the bot can post into the target Telegram channel
