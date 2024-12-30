from typing import Any

from aiogram_dialog import DialogManager
from nc_py_api import FsNode


async def get_fsnodes(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    fsnodes: list[FsNode] = dialog_manager.dialog_data["fsnodes"]

    return {
        "fsnode": fsnodes[0],
        "children": [fsnode for fsnode in fsnodes[1:] if fsnode.is_readable],
    }


async def get_documents(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {
        "documents": dialog_manager.dialog_data.get("documents", []),
    }


async def get_progress(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {
        "name": dialog_manager.dialog_data.get("name"),
        "progress": dialog_manager.dialog_data.get("progress", 0),
    }
