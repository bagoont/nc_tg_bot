from typing import Any

from aiogram import F
from aiogram.types import ContentType
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi, Progress

from bot.dialogs.files import getters, handlers, keyboards
from bot.dialogs.files.states import Create, Files, Multiselect


def _is_selected(data: dict[Any, Any], widget: Whenable, manager: DialogManager) -> bool:
    return bool(manager.current_context().widget_data["multiselect"])


def scrollgroup() -> Window:
    return Window(
        Const("__file__"),
        keyboards.sg_fsnodes(handlers.on_file, items_key="children"),
        Button(
            Const("__go_back__"),
            id="back",
            on_click=handlers.on_back,
            when=F["fsnode"].user_path,
        ),
        Button(
            Const("__multiselect__"),
            id="multiselect",
            on_click=handlers.on_multiselect,
            when=F["fsnode"].is_dir,
        ),
        Button(
            Const("__download__"),
            id="download",
            on_click=handlers.on_download,
            when=~F["fsnode"].is_dir & F["fsnode"].is_readable,
        ),
        Button(
            Const("__delte__"),
            id="delete",
            on_click=handlers.on_delete,
            when=F["fsnode"].user_path & F["fsnode"].is_deletable,
        ),
        Button(
            Const("__create__"),
            id="create",
            on_click=handlers.on_create,
            when=F["fsnode"].is_dir & F["fsnode"].is_updatable,
        ),
        state=Files.SCROLLGROUP,
        getter=getters.get_fsnodes,
    )


def multiselect() -> Window:
    return Window(
        Const("__muiltiselect__"),
        keyboards.ms_sg_fsnodes(items_key="children"),
        Button(
            Const("__download__"),
            id="download",
            on_click=handlers.on_multidownload,
            when=_is_selected,
        ),
        Button(
            Const("__delete__"),
            id="delete",
            on_click=handlers.on_multidelete,
            when=_is_selected,
        ),
        Button(
            Const("__drop__"),
            id="drop",
            on_click=handlers.on_multiselect_drop,
            when=_is_selected,
        ),
        Cancel(
            Const("__return__"),
        ),
        state=Multiselect.MULTISELECT,
        getter=getters.get_fsnodes,
    )


def multidownload() -> Window:
    return Window(
        Multi(
            Const("__multidownload__"),
            Progress("progress"),
        ),
        state=Multiselect.MUTLTIDOWNOLOAD,
        getter=getters.get_progress,
    )


def multidelete() -> Window:
    return Window(
        Multi(
            Const("__multidelete__"),
            Progress("progress"),
        ),
        state=Multiselect.MULTIDELETE,
        getter=getters.get_progress,
    )


def create() -> Window:
    return Window(
        Const("__type__"),
        SwitchTo(
            Const("__folder__"),
            id="folder",
            state=Create.FOLDER,
        ),
        SwitchTo(
            Const("__files__"),
            id="file",
            state=Create.FILES,
        ),
        Cancel(
            Const("__cance__"),
        ),
        state=Create.TYPE,
    )


def create_folder() -> Window:
    return Window(
        Const("__wait_folder_name__"),
        MessageInput(
            handlers.folder_name_handler,
            content_types=[ContentType.TEXT],
        ),
        SwitchTo(
            Const("__go_back__"),
            id="back",
            state=Create.TYPE,
        ),
        state=Create.FOLDER,
    )


def proccess_documents() -> Window:
    return Window(
        Const("__wait_files__"),
        MessageInput(
            handlers.document_handler,
            content_types=[ContentType.DOCUMENT],
        ),
        keyboards.sg_files(handlers.on_document, items_key="documents"),
        Button(
            Const("__upload__"),
            id="upload",
            on_click=handlers.upload_document,
            when=F["documents"],
        ),
        SwitchTo(
            Const("__go_back__"),
            id="back",
            state=Create.TYPE,
            on_click=handlers.clean_documents,
        ),
        getter=getters.get_documents,
        state=Create.FILES,
    )


def upload_documents() -> Window:
    return Window(
        Multi(
            Format("__uploading_files__"),
            Progress("progress"),
        ),
        state=Create.UPLOAD,
        getter=getters.get_progress,
    )
