from aiogram_dialog import DialogManager
from nc_py_api import FsNode

from bot.utils import MIME_SYMBOLS


async def get_fsnode(dialog_manager: DialogManager, **middleware_data) -> dict | None:
    ctx = dialog_manager.current_context()

    fsnodes = ctx.dialog_data.get("fsnodes")

    return {
        "fsnodes": [
            (
                nested_fsnode.file_id,
                "📁" if nested_fsnode.is_dir else MIME_SYMBOLS.get(nested_fsnode.info.mimetype, ""),
                nested_fsnode.name,
            )
            for fsndoe in fsnodes
        ],
    }
