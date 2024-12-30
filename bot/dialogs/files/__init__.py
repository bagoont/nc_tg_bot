from aiogram import Router, filters, types
from aiogram_dialog import Dialog, DialogManager, StartMode
from nc_py_api import AsyncNextcloud

from bot.dialogs.files import handlers, windows
from bot.dialogs.files.states import Files
from bot.filters import AuthFilter
from bot.middlewares import NextcloudMD
from bot.utils import Commands

router: Router = Router(name="files")

router.message.middleware.register(NextcloudMD())
router.callback_query.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.files.value), AuthFilter())
async def files(
    message: types.Message,
    command: filters.CommandObject,
    nc: AsyncNextcloud,
    dialog_manager: DialogManager,
) -> None:
    if command.args:
        await dialog_manager.start(Files.SCROLLGROUP, data={"path": command.args}, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(Files.SCROLLGROUP, mode=StartMode.RESET_STACK)


upload_documents_bg_dialog = Dialog(
    windows.upload_documents(),
    name="upload_documents",
)
multiselect_dialog = Dialog(
    windows.multiselect(),
    windows.multidownload(),
    windows.multidelete(),
    on_start=handlers.on_multiselect_start,
    name="multiselect",
)
create_dialog = Dialog(
    windows.create(),
    windows.create_folder(),
    windows.proccess_documents(),
    on_start=handlers.on_create_start,
    name="create",
)
dialog = Dialog(
    windows.scrollgroup(),
    on_start=handlers.on_start,
    on_process_result=handlers.on_process_result,
    name="files",
)

router.include_router(upload_documents_bg_dialog)
router.include_router(dialog)
router.include_router(multiselect_dialog)
router.include_router(create_dialog)
