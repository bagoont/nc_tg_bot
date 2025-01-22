from aiogram.fsm.state import State, StatesGroup


class Search(StatesGroup):
    INPUT_QUERY = State()
    SCROLLGROUP = State()
    NOT_FOUND = State()
