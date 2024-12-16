from aiogram_dialog import DialogManager

from bot.utils import MIME_SYMBOLS


async def get_fsnodes(dialog_manager: DialogManager, **middleware_data) -> dict | None:
    ctx = dialog_manager.current_context()

    fsnodes = ctx.dialog_data.get("fsnodes")

    return {
        "fsnodes": [
            (
                fsnode.file_id,
                "📁" if fsnode.is_dir else MIME_SYMBOLS.get(fsnode.info.mimetype, ""),
                fsnode.name,
            )
            for fsnode in fsnodes
        ],
    }
