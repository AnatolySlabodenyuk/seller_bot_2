import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import BOT_TOKEN
from handlers import user_handlers


def main():
    logging.basicConfig(level=logging.INFO)

    async def _main():
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(user_handlers.router)
        await dp.start_polling(bot)

    asyncio.run(_main())


if __name__ == "__main__":
    main()
