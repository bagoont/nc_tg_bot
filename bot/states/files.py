from aiogram.fsm.state import State, StatesGroup


class Files(StatesGroup):
    SCROLLGROUP = State()
    MULTIDELETE = State()
    MULTIDOWNLOAD = State()
    NEW = State()
    NEW_FOLDER = State()
    NEW_FILES = State()
    NOT_FOUND = State()
