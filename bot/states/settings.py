from aiogram.fsm.state import State, StatesGroup


class Settings(StatesGroup):
    MAIN = State()
    LANG = State()
    LOGOUT = State()
