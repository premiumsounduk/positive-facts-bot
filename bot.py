import json
import logging
import os
import random
from datetime import date
from pathlib import Path
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from telegram import Update
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
FACTS_FILE = Path("facts.json")
SUBSCRIBERS_FILE = Path("subscribers.json")
UK_TZ = ZoneInfo("Europe/London")

scheduler = AsyncIOScheduler(timezone=UK_TZ)


def load_facts() -> list[dict]:
    with FACTS_FILE.open() as f:
        return json.load(f)


def load_subscribers() -> list[int]:
    if not SUBSCRIBERS_FILE.exists():
        return []
    with SUBSCRIBERS_FILE.open() as f:
        return json.load(f)


def save_subscribers(subs: list[int]) -> None:
    with SUBSCRIBERS_FILE.open("w") as f:
        json.dump(subs, f)


def format_fact(fact: dict) -> str:
    tag = "#" + fact["category"].replace(" ", "_").replace("-", "_")
    return f"*{fact['year']}*\n\n{fact['fact']}\n\n{tag}"


def get_daily_fact() -> dict:
    facts = load_facts()
    index = (date.today().timetuple().tm_yday - 1) % len(facts)
    return facts[index]


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    subs = load_subscribers()
    if chat_id not in subs:
        subs.append(chat_id)
        save_subscribers(subs)
        await update.message.reply_text(
            "Subscribed! You'll receive one positive fact every day at 09:00 UK time.\n\n"
            "/today — today's fact\n"
            "/random — a random fact\n"
            "/stop — unsubscribe"
        )
    else:
        await update.message.reply_text(
            "You're already subscribed.\n/today — today's fact\n/random — a random one"
        )


async def cmd_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    subs = load_subscribers()
    if chat_id in subs:
        subs.remove(chat_id)
        save_subscribers(subs)
        await update.message.reply_text("Unsubscribed. Use /start to subscribe again anytime.")
    else:
        await update.message.reply_text("You're not subscribed. Use /start to subscribe.")


async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(format_fact(get_daily_fact()), parse_mode="Markdown")


async def cmd_random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    fact = random.choice(load_facts())
    await update.message.reply_text(format_fact(fact), parse_mode="Markdown")


async def send_daily_facts(app: Application) -> None:
    message = format_fact(get_daily_fact())
    subs = load_subscribers()
    blocked: list[int] = []
    for chat_id in subs:
        try:
            await app.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        except (Forbidden, BadRequest) as e:
            logger.warning("Removing blocked/invalid subscriber %s: %s", chat_id, e)
            blocked.append(chat_id)
        except Exception as e:
            logger.error("Failed to send to %s: %s", chat_id, e)
    if blocked:
        save_subscribers([s for s in subs if s not in blocked])
        logger.info("Removed %d blocked subscriber(s)", len(blocked))


async def post_init(app: Application) -> None:
    scheduler.add_job(
        send_daily_facts,
        CronTrigger(hour=9, minute=0),
        args=[app],
    )
    scheduler.start()
    logger.info("Scheduler started — daily facts at 09:00 UK time")


async def post_shutdown(app: Application) -> None:
    scheduler.shutdown(wait=False)


def main() -> None:
    if not TOKEN:
        raise ValueError("BOT_TOKEN not set — add it to your .env file")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("random", cmd_random))

    logger.info("Bot starting…")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
