from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import ProfileStates
from services import calculations, weather
from storage import users
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Добро пожаловать! Для начала работы настройте профиль командой /set_profile"
    )

@router.message(Command("set_profile"))
async def start_profile(message: Message, state: FSMContext):
    await message.answer("Введите ваш вес в кг:")
    await state.set_state(ProfileStates.weight)


@router.message(ProfileStates.weight)
async def process_weight(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число!")
    await state.update_data(weight=float(message.text))
    await message.answer("Введите ваш рост в см:")
    await state.set_state(ProfileStates.height)


@router.message(ProfileStates.height)
async def process_height(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число!")
    await state.update_data(height=float(message.text))
    await message.answer("Введите ваш возраст:")
    await state.set_state(ProfileStates.age)


@router.message(ProfileStates.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число!")
    await state.update_data(age=int(message.text))
    await message.answer("Введите минуты активности в день:")
    await state.set_state(ProfileStates.activity)


@router.message(ProfileStates.activity)
async def process_activity(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Введите число!")
    await state.update_data(activity=int(message.text))
    await message.answer("Введите ваш город:")
    await state.set_state(ProfileStates.city)


@router.message(ProfileStates.city)
async def process_city(message: Message, state: FSMContext):
    user_data = await state.get_data()
    city = message.text

    # Расчет норм
    temperature = weather.get_weather(city)
    water_goal = calculations.calculate_water_norm(
        user_data['weight'],
        user_data['activity'],
        temperature
    )

    calorie_goal = calculations.calculate_calories(
        user_data['weight'],
        user_data['height'],
        user_data['age'],
        user_data['activity']
    )

    # Сохранение данных
    users[message.from_user.id] = {
        **user_data,
        'city': city,
        'water_goal': water_goal,
        'calorie_goal': calorie_goal,
        'logged_water': 0,
        'logged_calories': 0,
        'burned_calories': 0
    }

    await message.answer(
        f"Профиль создан!\n"
        f"💧 Норма воды: {water_goal} мл\n"
        f"🔥 Норма калорий: {calorie_goal:.0f} ккал"
    )
    await state.clear()

