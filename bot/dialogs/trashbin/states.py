from aiogram.fsm.state import State, StatesGroup


class Trashbin(StatesGroup):
    SCROLLGROUP = State()
    MULTISELECT = State()
    TRASH = State()
    CLEANUP = State()
    EMPTY = State()
