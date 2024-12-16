from aiogram import F, types
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Group, SwitchTo
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const

from bot.handlers.files import getters, handlers, keyboards
from bot.states import Files


def scrollgroup_window() -> Window:
    return Window(
        Const("Choose file."),
        keyboards.sg_files(handlers.on_file),
        Button(
            Const("⬅️ Back"),
            id="files_back",
            on_click=handlers.on_back,
            when=~F["dialog_data"]["fsnode"].user_path,
        ),
        Button(
            Const("⬇️ Download"),
            id="files_download",
            on_click=handlers.on_download,
            when=~F["dialog_data"]["fsnode"].is_dir & F["dialog_data"]["fsnode"].is_readable,
        ),
        SwitchTo(
            Const("🆕 Add"),
            id="files_add",
            state=Files.NEW,
            when=~F["dialog_data"]["fsnode"].is_dir & F["dialog_data"]["fsnode"].is_updatable,
        ),
        SwitchTo(
            Const("⬇️ Select to downloads"),
            id="files_multidownload",
            state=Files.MULTIDOWNLOAD,
            when=F["dialog_data"]["fsnode"].is_dir & F["dialog_data"]["fsnode"].is_readable,
        ),
        Button(
            Const("❌ Delete"),
            id="files_multidelete",
            on_click=handlers.on_delete,
            when=~F["dialog_data"]["fsnode"].user_path != "",
        ),
        SwitchTo(
            Const("❌ Select to delete"),
            id="files_delete",
            state=Files.MULTIDELETE,
            when=F["dialog_data"]["fsnode"].is_dir,
        ),
        Cancel(
            Const("Close"),
            id="files_close",
        ),
        state=Files.SCROLLGROUP,
        getter=getters.get_fsnode,
    )


def not_found_window() -> Window:
    return Window(
        Const("File not found."),
        Cancel(
            Const("Exit"),
            id="file_not_found_cancel",
        ),
        state=Files.NOT_FOUND,
    )


def multidownload_window() -> Window:
    return Window(
        Const("Select files to download."),
        keyboards.ms_sg_files(handlers.on_multidownload_select),
        Button(
            Const("Confirm"),
            id="files_multidownload_confirm",
            on_click=handlers.on_multidownload_confirm,
        ),
        SwitchTo(
            Const("Back"),
            id="files_multidownload_back",
            state=Files.SCROLLGROUP,
        ),
        state=Files.MULTIDOWNLOAD,
        getter=getters.get_downloadable_fsnodes,
    )


def multidelete_window() -> Window:
    return Window(
        Const("Select files to delete."),
        keyboards.ms_sg_files(handlers.on_multidelete_select),
        Button(
            Const("Confirm"),
            id="files_multidelete_confirm",
            on_click=handlers.on_multidelete_confirm,
        ),
        SwitchTo(
            Const("Back"),
            id="files_multidelete_back",
            state=Files.SCROLLGROUP,
        ),
        state=Files.MULTIDELETE,
        getter=getters.get_deletable_fsnodes,
    )


def new_window() -> Window:
    return Window(
        Const("Choose new file."),
        Group(
            SwitchTo(
                Const("Folder"),
                id="files_new_folder",
                state=Files.NEW_FOLDER,
            ),
            SwitchTo(
                Const("Files"),
                id="files_new_file",
                state=Files.NEW_FILES,
            ),
        ),
        SwitchTo(
            Const("Back"),
            id="files_new_back",
            state=Files.SCROLLGROUP,
        ),
        state=Files.NEW,
    )


def new_folder_window() -> Window:
    return Window(
        Const("Write folder name."),
        MessageInput(
            handlers.new_folder_handler,
            content_types=[types.ContentType.TEXT],
        ),
        SwitchTo(
            Const("Back"),
            id="files_new_folder_back",
            state=Files.NEW,
        ),
        state=Files.NEW_FOLDER,
    )


def new_file_window() -> Window:
    return Window(
        Const("Send files."),
        MessageInput(
            handlers.new_file_handler,
            content_types=[types.ContentType.DOCUMENT],
        ),
        Button(
            Const("✔️ Finish"),
            id="files_new_file_back",
            on_click=handlers.on_complete,
        ),
        markup_factory=ReplyKeyboardFactory(
            resize_keyboard=True,
            selective=True,
            one_time_keyboard=True,
        ),
        state=Files.NEW_FILES,
    )
