"""Search states group."""

from aiogram.fsm.state import State, StatesGroup


class SearchStatesGroup(StatesGroup):
    """A group of states for handling search-related actions."""

    SEARCH = State()
