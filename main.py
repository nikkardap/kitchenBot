import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import token
from handler import handler
from handler import callback
# database import db
#from admin import adminAccount



async def main():
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handler.router)
    dp.include_router(callback.router)
    #dp.include_router(db.router)
    #dp.include_router(adminAccount.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
