"""FsNode menu states group."""

from aiogram.fsm.state import State, StatesGroup


class FsNodeMenuStatesGroup(StatesGroup):
    """A group of states for handling actions related to fsnode menu.

    This includes uploading files and creating new directories within the user's Nextcloud storage.
    It is used to transfer fsnode id through handlers.
    """

    UPLOAD = State()
    MKDIR = State()
