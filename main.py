import asyncio
import os


from aiogram import Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from dotenv import load_dotenv
from src.handlers.user_private import user_private_router
from src.handlers.user_group import user_group_router
from src.handlers.non_text import non_text_router
from src.common.bot_command_list import private
from src.common.alloweb_updates import ALLOWED_UPDATES
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
load_dotenv()

TOKEN = os.environ.get("TOKEN")
default = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN, default=default)
dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(non_text_router)
dp.include_router(user_group_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
    asyncio.run(main())
