from aiogram.fsm.state import StatesGroup, State

class ProfileStates(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()

class FoodLogStates(StatesGroup):
    quantity = State()
