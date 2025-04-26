from aiogram import Dispatcher, Bot

from config import Settings
from database.db import create_table
from user_router.main import router as user_router
from user_router.back_handler import router as back_router
from user_router.other_handler import router as other_router
from admin_router.main import router as admin_router

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)

async def main():
    create_table()
    dp = Dispatcher()
    dp.include_routers(other_router, admin_router, user_router, back_router) 

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    
    create_table()
    asyncio.run(main())