from typing import Any

from aiogram_dialog import DialogManager
from nc_py_api import FsNode

from bot.utils import MIME_SYMBOLS


async def get_trash_bin(dialog_manager: DialogManager, **middleware_data: Any) -> dict[str, Any]:
    ctx = dialog_manager.current_context()

    trash_bin: list[FsNode] = ctx.dialog_data.get("trash_bin")

    return {
        "fsnodes": [
            {
                "file_id": trash.file_id,
                "symbol": "📁" if trash.is_dir else MIME_SYMBOLS.get(trash.info.mimetype, ""),
                "name": trash.name,
            }
            for trash in trash_bin
        ],
    }
