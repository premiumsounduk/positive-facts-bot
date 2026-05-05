# positive-facts-bot

A Telegram bot that sends one positive fact per day about human progress since the year 2000 — covering global health, poverty, education, technology, environment, human rights, and science.

---

## What we built and why

The idea was simple: the world has made extraordinary progress in the last 25 years, but the news rarely reflects it. This bot sends one verified, sourced positive fact every morning at 09:00 UK time — a small daily reminder that things are genuinely getting better.

### How it works

1. **Facts are stored in `facts.json`** — a plain array of 30 objects, each with a `year`, `category`, and `fact`. No database, no API calls, no cost.

2. **The daily fact is chosen deterministically** — using the day of the year (`day_of_year % total_facts`), so every subscriber always gets the same fact on the same day. The cycle repeats once the facts run out.

3. **Subscribers are stored in `subscribers.json`** — a plain list of Telegram chat IDs. When someone sends `/start`, their ID is added. When they block the bot or send `/stop`, they are removed. No database needed.

4. **APScheduler fires the daily job at 09:00 UK time** — it uses `AsyncIOScheduler` so it runs inside the same asyncio event loop as the bot, started via python-telegram-bot's `post_init` hook. No threading issues.

5. **python-telegram-bot v21+ handles all Telegram communication** — fully async, using `CommandHandler` for each command and `run_polling` to keep the connection alive.

---

## Project structure

```
positive-facts-bot/
├── bot.py              # Main bot — commands, scheduler, daily sender
├── facts.json          # 30 positive facts from 2000–2025
├── subscribers.json    # Active subscriber chat IDs (auto-managed)
├── .env                # Your secret bot token (not committed to git)
├── .env.example        # Template for the .env file
├── .gitignore          # Excludes .env and subscribers.json from git
├── requirements.txt    # Pinned Python dependencies
└── README.md           # This file
```

---

## Commands

| Command   | Description                          |
|-----------|--------------------------------------|
| `/start`  | Subscribe to daily facts at 09:00 UK |
| `/stop`   | Unsubscribe                          |
| `/today`  | Get today's fact on demand           |
| `/random` | Get a random fact from the list      |

---

## Fact categories

The 30 starter facts span 7 categories across 2000–2025:

- `health` — disease eradication, vaccines, HIV/AIDS progress, child mortality
- `poverty` — extreme poverty reduction, economic development
- `education` — literacy rates, school enrolment
- `technology` — smartphones, solar energy, AI, space telescopes
- `environment` — ozone recovery, renewables, conservation
- `human_rights` — marriage equality, decriminalisation
- `science` — genome sequencing, Higgs boson, black hole imaging, CRISPR

---

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
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run locally

```bash
python3 bot.py
```

Open Telegram, find your bot, and send `/start`.

---

## Deploy on Render.com (background worker)

Render runs the bot 24/7 as a background worker — no web server needed.

### Steps

1. Push your repo to GitHub (`.env` is already in `.gitignore`)

2. Go to [render.com](https://render.com) and sign in

3. Click **New → Background Worker**

4. Connect your GitHub repo (`positive-facts-bot`)

5. Fill in the settings:
   - **Name:** `positive-facts-bot`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 bot.py`

6. Under **Environment Variables**, add:
   - Key: `BOT_TOKEN`
   - Value: your Telegram bot token

7. Click **Create Background Worker**

Render will build and deploy the bot. Check the **Logs** tab to confirm it's running.

### Persistent storage note

`subscribers.json` lives on Render's local filesystem and resets on each new deploy. For permanent persistence across deploys, consider:
- A mounted **Render Disk** (paid feature)
- A free hosted database such as [Supabase](https://supabase.com)

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
