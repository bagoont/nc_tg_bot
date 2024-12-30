from aiogram.fsm.state import State, StatesGroup


class Trash_bin(StatesGroup):
    SCROLLGROUP = State()
    MULTISELECT = State()
    TRASH = State()
    CLEANUP = State()
    EMPTY = State()
