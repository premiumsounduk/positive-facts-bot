# Positive Facts Bot

A Telegram bot that delivers one positive fact per day about real human progress since the year 2000.

Most news is negative by design — it captures attention. But the data tells a different story. Child mortality has halved. Extreme poverty has fallen below 10% for the first time in history. Diseases that paralysed children for centuries have been eradicated. Solar energy is now the cheapest electricity source ever recorded. This bot exists to surface that story, one fact at a time.

Every morning at 09:00 UK time, subscribers receive a single verified fact — a real number, a real year, a real milestone. No opinion, no spin. Just progress.

---

## What it covers

30 facts spanning 2000–2025 across seven categories:

- **Health** — vaccines, disease eradication, HIV/AIDS, child and maternal mortality
- **Poverty** — extreme poverty rates, economic development, hunger reduction
- **Education** — literacy, school enrolment, gender parity
- **Technology** — smartphones, solar energy, AI, space exploration
- **Environment** — ozone recovery, renewable energy growth, conservation wins
- **Human rights** — marriage equality, decriminalisation, legal protections
- **Science** — genome sequencing, the Higgs boson, black hole imaging, CRISPR

---

## Commands

| Command   | What it does                              |
|-----------|-------------------------------------------|
| `/start`  | Subscribe — receive a fact every day at 09:00 UK time |
| `/stop`   | Unsubscribe                               |
| `/today`  | Get today's fact right now               |
| `/random` | Get a random fact from the full list     |

---

## How it works

- Facts live in `facts.json` — a plain list of objects with a `year`, `category`, and `fact`
- Each day's fact is chosen by `day_of_year % total_facts`, so all subscribers always get the same fact on the same day and the cycle repeats automatically
- Subscribers are stored in `subscribers.json` — a plain list of Telegram chat IDs, no database required
- The daily 09:00 job runs via APScheduler inside the same async event loop as the bot
- If a subscriber blocks the bot, they are automatically removed from the list

---

## Setup

### 1. Get a bot token

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy the token you receive

### 2. Clone and configure

```bash
git clone https://github.com/premiumsounduk/positive-facts-bot.git
cd positive-facts-bot
cp .env.example .env
```

Edit `.env`:

```
BOT_TOKEN=your_token_here
```

### 3. Install and run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bot.py
```

Find your bot on Telegram and send `/start`.

---

## Deploy on Render.com

To keep the bot running 24/7 after closing your laptop, deploy it as a background worker on Render.

1. Push the repo to GitHub
2. Sign in at [render.com](https://render.com) and click **New → Background Worker**
3. Connect your GitHub repo
4. Set the build command to `pip install -r requirements.txt` and start command to `python3 bot.py`
5. Add `BOT_TOKEN` as an environment variable with your token
6. Click **Create Background Worker** and check the logs to confirm it's live

> Note: `subscribers.json` resets on each deploy since it lives on Render's local filesystem. For permanent persistence, use a mounted Render Disk or a free hosted database like [Supabase](https://supabase.com).

---

## Adding more facts

Edit `facts.json` and add entries following this format:

```json
{
  "year": 2024,
  "category": "health",
  "fact": "Your fact here."
}
```

The more facts you add, the longer the cycle before it repeats.
