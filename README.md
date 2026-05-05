# positive-facts-bot

A Telegram bot that sends one positive fact per day about human progress since the year 2000 — covering global health, poverty, education, technology, environment, human rights, and science.

## Features

- Daily fact at 09:00 UK time, cycling deterministically through `facts.json`
- `/start` — subscribe to daily facts
- `/stop` — unsubscribe
- `/today` — get today's fact on demand
- `/random` — get a random fact
- Automatically removes subscribers who block the bot
- No database required — subscribers stored in `subscribers.json`

## Setup

### 1. Create a Telegram bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the token BotFather gives you

### 2. Clone and configure

```bash
git clone https://github.com/premiumsounduk/positive-facts-bot.git
cd positive-facts-bot
cp .env.example .env
```

Edit `.env` and paste your token:

```
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run locally

```bash
python bot.py
```

Open Telegram, find your bot, and send `/start`.

---

## Deploy on Render.com (background worker)

Render runs the bot 24/7 as a background worker with no web server needed.

### Steps

1. Push your repo to GitHub (`.env` is already in `.gitignore`)

2. Go to [render.com](https://render.com) and sign in

3. Click **New → Background Worker**

4. Connect your GitHub repo (`positive-facts-bot`)

5. Fill in the settings:
   - **Name:** `positive-facts-bot`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

6. Under **Environment Variables**, add:
   - Key: `BOT_TOKEN`
   - Value: your Telegram bot token

7. Click **Create Background Worker**

Render will build and start the bot. Check the logs tab to confirm it's running.

### Persistent storage note

`subscribers.json` is written to the local filesystem on Render and resets on each deploy. For permanent subscriber persistence, consider:
- Storing `subscribers.json` on a mounted **Render Disk** (paid feature)
- Migrating to a free database such as [Supabase](https://supabase.com)

---

## Customising facts

Edit `facts.json` to add, remove, or change facts. Each entry must follow this schema:

```json
{
  "year": 2023,
  "category": "health",
  "fact": "Your fact text here."
}
```

The daily fact is chosen by `day_of_year % total_facts`, so the cycle is fully deterministic and consistent across all subscribers.
