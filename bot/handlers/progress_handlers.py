from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from storage import users

router = Router()


@router.message(Command("check_progress"))
async def check_progress(message: Message):
    user_id = message.from_user.id
    if user_id not in users:
        return await message.answer("Сначала настройте профиль!")

    user = users[user_id]
    water_remaining = user['water_goal'] - user['logged_water']
    calories_remaining = user['calorie_goal'] - user['logged_calories'] + user['burned_calories']

    progress = (
        "📊 Ваш прогресс:\n\n"
        f"💧 Вода: {user['logged_water']}/{user['water_goal']} мл\n"
        f"🔥 Калории: {user['logged_calories']:.0f}/{user['calorie_goal']:.0f} ккал\n"
        f"🏃 Сожжено: {user['burned_calories']} ккал\n"
        f"Баланс: {calories_remaining:.0f} ккал осталось\n"
        f"Баланс: {water_remaining:.0f} мл воды осталось"
    )

    await message.answer(progress)




