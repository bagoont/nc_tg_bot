from typing import Any

from aiogram_dialog import DialogManager
from nc_py_api import FsNode


async def get_fsnodes(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    fsnodes: list[FsNode] = dialog_manager.dialog_data["fsnodes"]

    return {
        "fsnodes": fsnodes,
    }
