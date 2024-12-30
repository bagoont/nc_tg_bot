from typing import Any

from aiogram_dialog import DialogManager
from nc_py_api import FsNode

from bot.utils import MIME_SYMBOLS


async def get_fsnodes(dialog_manager: DialogManager, **middleware_data: Any) -> dict[str, Any]:
    ctx = dialog_manager.current_context()

    fsnodes: list[FsNode] = ctx.dialog_data.get("fsnodes")

    return {
        "fsnodes": [
            {
                "file_id": fsnode.file_id,
                "symbol": "📁" if fsnode.is_dir else MIME_SYMBOLS.get(fsnode.info.mimetype, ""),
                "name": fsnode.name,
            }
            for fsnode in fsnodes
            if fsnode.is_readable
        ]
    }
