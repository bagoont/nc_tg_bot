from aiogram_dialog import DialogManager
from nc_py_api import FsNode

from bot.utils import MIME_SYMBOLS


async def get_fsnode(dialog_manager: DialogManager, **middleware_data) -> dict | None:
    ctx = dialog_manager.current_context()

    fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content = ctx.dialog_data.get("fsnode_content")

    return {
        "fsnode": fsnode,
        "is_root": fsnode.user_path == "",
        "is_dir": fsnode.is_dir,
        "fsnode_content": [
            (
                nested_fsnode.file_id,
                "📁" if nested_fsnode.is_dir else MIME_SYMBOLS.get(nested_fsnode.info.mimetype, ""),
                nested_fsnode.name,
            )
            for nested_fsnode in fsnode_content
        ],
    }


async def get_downloadable_fsnodes(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()

    fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content = ctx.dialog_data.get("fsnode_content")

    downloadable_fsnodes = []
    for fsnode in fsnode_content:
        if not fsnode.is_dir:
            downloadable_fsnodes.append(fsnode)

    return {
        "fsnode": fsnode,
        "fsnode_content": [
            (
                nested_fsnode.file_id,
                "📁" if nested_fsnode.is_dir else MIME_SYMBOLS.get(nested_fsnode.info.mimetype, ""),
                nested_fsnode.name,
            )
            for nested_fsnode in downloadable_fsnodes
        ],
    }


async def get_deletable_fsnodes(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()

    fsnode: FsNode = ctx.dialog_data.get("fsnode")
    fsnode_content = ctx.dialog_data.get("fsnode_content")

    deletable_fsnodes = []
    for fsnode in fsnode_content:
        if fsnode.is_deletable:
            deletable_fsnodes.append(fsnode)

    return {
        "fsnode": fsnode,
        "fsnode_content": [
            (
                nested_fsnode.file_id,
                "📁" if nested_fsnode.is_dir else MIME_SYMBOLS.get(nested_fsnode.info.mimetype, ""),
                nested_fsnode.name,
            )
            for nested_fsnode in deletable_fsnodes
        ],
    }
