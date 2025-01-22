from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services import food_api
from storage import users
from states import FoodLogStates
from aiogram.filters import Command, CommandObject

router = Router()


@router.message(Command("log_water"))
async def log_water(message: Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id not in users:
        return await message.answer("Сначала настройте профиль!")

    if not command.args:
        return await message.answer("Пример использования: /log_water 500")

    try:
        amount = int(command.args)
        users[user_id]['logged_water'] += amount
        remaining = users[user_id]['water_goal'] - users[user_id]['logged_water']
        await message.answer(
            f"✅ Добавлено {amount} мл воды\n"
            f"Осталось: {remaining} мл"
        )
    except ValueError:
        await message.answer("Используйте: /log_water <количество в мл>")


@router.message(Command("log_food"))
async def log_food_start(message: Message, command: CommandObject, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in users:
        return await message.answer("Сначала настройте профиль!")

    if not command.args:
        return await message.answer("Пример использования: /log_food яблоко")

    product = command.args
    calories = food_api.get_product_calories(product)

    if not calories:
        return await message.answer("Продукт не найден 😞")

    await state.update_data(calories=calories)
    await message.answer(f"{product} — {calories} ккал на 100 грамм. Сколько грамм вы съели?")
    await state.set_state(FoodLogStates.quantity)


@router.message(FoodLogStates.quantity)
async def process_weight(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if not message.text.isdigit():
        return await message.answer("Введите число!")
    await state.update_data(quantity=float(message.text))

    user_data = await state.get_data()
    total_calories = user_data['calories'] * user_data['quantity'] / 100
    # Сохранение данных
    users[user_id]['logged_calories'] += total_calories

    await message.answer(
        f"Записано: {total_calories:.1f} ккал."
    )
    await state.clear()


@router.message(Command("log_workout"))
async def log_workout(message: Message, command: CommandObject):
    user_id = message.from_user.id
    if user_id not in users:
        return await message.answer("Сначала настройте профиль!")

    if not command.args:
        return await message.answer("Пример использования: /log_workout бег 30")

    try:
        args = command.args.split()
        if len(args) != 2:
            return await message.answer("Пример использования: /log_workout бег 30")

        workout_type, minutes = args[0], args[1]
        minutes = int(minutes)
        burned = minutes * 10

        users[user_id]['burned_calories'] += burned
        users[user_id]['logged_water'] -= (minutes // 30) * 200

        await message.answer(
            f"🏋️ {workout_type} {minutes} мин — {burned} ккал\n"
            f"💦 Добавьте {200 * (minutes // 30)} мл воды"
        )
    except:
        await message.answer("Используйте: /log_workout <тип> <минуты>")

