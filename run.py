import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

from app.user import user


async def main():
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
