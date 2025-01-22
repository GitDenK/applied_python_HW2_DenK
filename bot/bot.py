import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import Config
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares import LoggingMiddleware

from handlers import profile_handlers, tracking_handlers, progress_handlers

async def main():
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(LoggingMiddleware())
    dp.include_router(profile_handlers.router)
    dp.include_router(tracking_handlers.router)
    dp.include_router(progress_handlers.router)

    # Регистрация команд меню
    await bot.set_my_commands(
        commands=[
            types.BotCommand(command="start", description="Запустить бота"),
            types.BotCommand(command="set_profile", description="Настройка профиля"),
            types.BotCommand(command="log_water", description="Добавить воду"),
            types.BotCommand(command="log_food", description="Добавить еду"),
            types.BotCommand(command="log_workout", description="Добавить тренировку"),
            types.BotCommand(command="check_progress", description="Проверить прогресс"),
        ],
        scope=types.BotCommandScopeDefault()
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())







