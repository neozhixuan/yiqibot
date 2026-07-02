# Wedding Telegram Reminder Bot

A deploy-ready Python Telegram bot for Railway. It sends friendly wedding reminder messages to a Telegram channel 10 minutes before each scheduled wedding event.

## What it does

- Uses Python 3 and `python-telegram-bot` v20+ async API.
- Schedules all events in `Asia/Singapore` timezone, UTC+8.
- Sends each reminder 10 minutes before the event start time.
- Skips reminders whose reminder time has already passed when the worker starts.
- Logs every skipped event, upcoming reminder, sent reminder, and send failure to stdout for Railway logs.
- Continues to the next event if one Telegram send fails.

## Files

```text
main.py          # Scheduler/reminder worker
requirements.txt # Python dependencies
Procfile         # Railway worker start command
README.md        # Railway deployment guide
```

## Telegram setup checklist

1. Make sure the bot has been added to the Telegram channel.
2. Give the bot permission to post messages in the channel.
3. This project uses the Bot API channel format:

```python
RAW_CHANNEL_ID = "562953664827933"
CHANNEL_ID = "-100562953664827933"
```

Telegram channels and supergroups usually require the `-100` prefix for `chat_id`.

## Local test

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The script will print logs showing which event is next and how long it will sleep. If the event reminder time has already passed, it will skip that event.

## Deploy to Railway

### 1. Create a GitHub repository

If you want to deploy through GitHub, create a new repository under:

```text
https://github.com/neozhixuan
```

For example:

```text
wedding-telegram-reminder-bot
```

Then push these files to the repository:

```bash
git init
git add main.py requirements.txt Procfile README.md
git commit -m "Add wedding Telegram reminder bot"
git branch -M main
git remote add origin https://github.com/neozhixuan/wedding-telegram-reminder-bot.git
git push -u origin main
```

### 2. Create a Railway project

1. Go to Railway.
2. Click **New Project**.
3. Choose **Deploy from GitHub repo**.
4. Select the repository you created.
5. Railway should detect the Python app automatically.

### 3. Confirm the worker command

The included `Procfile` tells Railway to run the app as a worker:

```text
worker: python main.py
```

This is important because the bot is a background scheduler, not a web server.

### 4. Deploy

After Railway deploys, open the deployment logs. You should see logs similar to:

```text
Wedding reminder bot started. Timezone: Asia/Singapore. Channel: -100562953664827933
Loaded 26 wedding events
Next reminder: 'Parents Veiling & Shu Tou' at 2026-07-03 20:50:00 SGT. Sleeping for ... seconds.
```

### 5. Keep the worker running

On Railway free tier, make sure your worker service is running during the wedding period. Since the script sleeps until each event, it should stay active as a Railway worker process.

If Railway restarts the worker, the script will safely skip reminders whose reminder time has already passed and continue with upcoming events.

## Editing event messages

All events are defined in `EVENTS` inside `main.py`. Each event has:

```python
WeddingEvent(
    title="Event title",
    start=datetime(2026, 7, 4, 10, 0, tzinfo=SGT),
    message="Reminder message...",
)
```

To change a reminder, edit the event's `message`. To change the schedule, edit the `start` datetime.

## Important notes

- All times are Singapore time (`Asia/Singapore`, UTC+8).
- The reminder offset is controlled by:

```python
REMINDER_OFFSET = timedelta(minutes=10)
```

- If you want to avoid committing the bot token in GitHub, move `BOT_TOKEN` into a Railway environment variable later. For this requested deploy-ready version, the token is currently placed directly in `main.py`.
