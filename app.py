from aiogram import executor, Dispatcher
from tortoise import Tortoise
from loader import dp, db, scheduler, bot
import middlewares
import filters
import handlers
from data import config
from utils.db_api import init_db
from utils.postpone_message import send_postpone_messages
from utils.delete_events import delete
from utils.send_notification import send


async def on_startup(dp: Dispatcher):
    await init_db()
    scheduler.add_job(send_postpone_messages, "cron", second=1, args=(bot,))
    scheduler.add_job(delete, "cron", hour=23, minute=59, args=(bot,))
    scheduler.add_job(send, "cron", second=1, args=(bot,))
    scheduler.start()


async def on_shutdown(dp: Dispatcher):
    await Tortoise.close_connections()


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=config.SKIP_UPDATES, on_startup=on_startup, on_shutdown=on_shutdown)
