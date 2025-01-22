from aiogram.fsm.state import State, StatesGroup


class Files(StatesGroup):
    SCROLLGROUP = State()


class Multiselect(StatesGroup):
    MULTISELECT = State()
    MUTLTIDOWNOLOAD = State()
    MULTIDELETE = State()


class Create(StatesGroup):
    TYPE = State()
    FOLDER = State()
    FILES = State()
    UPLOAD = State()
