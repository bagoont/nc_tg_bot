"""Abstract and base inline keyboard classes for fsnode boards."""

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import InlineKeyboardButton
from nc_py_api.files import FsNode

from bot.core import settings
from bot.utils import MIME_SYMBOLS

FSNODE_BUTTON_TEXT_LENGTH = 32


class _FsNodeAbstractBoard(ABC):
    @abstractmethod
    def get_kb(self) -> InlineKeyboardMarkup:
        raise NotImplementedError

    @abstractmethod
    def build_fsnode_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError

    @abstractmethod
    def build_pag_buttons(self) -> InlineKeyboardBuilder:
        raise NotImplementedError


class _FsNodeBaseBoard(_FsNodeAbstractBoard, ABC):
    """Base class for fsnode boards."""

    fsnode_callback_data: type[CallbackData]
    actions_callback_data: type[CallbackData]
    actions: type[IntEnum]

    def __init__(
        self,
        fsnodes: list[FsNode],
        page: int = 0,
        page_size: int = settings.TG_PAGE_SIZE,
        **kwargs: Any,
    ) -> None:
        self.builder = InlineKeyboardBuilder()
        self.fsnodes = sorted(fsnodes, key=lambda x: x.is_dir, reverse=True)
        self.page = page
        self.page_size = page_size
        self.kwargs = kwargs

    def get_kb(self) -> InlineKeyboardMarkup:
        """Return fsnode InlineKeyboardMarkup."""
        self.builder.attach(self.build_fsnode_buttons())
        self.builder.attach(self.build_pag_buttons())
        self.builder.attach(self.build_actions_buttons())
        return self.builder.as_markup()

    def build_fsnode_buttons(self) -> InlineKeyboardBuilder:
        """Builds fsnode buttons based on the current page and page size.

        :return: InlineKeyboardBuilder with fsnode buttons.
        """
        builder = InlineKeyboardBuilder()

        start_index = self.page * self.page_size
        end_index = (self.page + 1) * self.page_size

        for fsnode in self.fsnodes[start_index:end_index]:
            prefix = MIME_SYMBOLS.get(fsnode.info.mimetype, "")

            builder.button(
                text=(
                    f"{prefix} {fsnode.name[:FSNODE_BUTTON_TEXT_LENGTH]}"
                    f"{'/' if fsnode.is_dir else ''}"
                ),
                callback_data=self.fsnode_callback_data(
                    file_id=fsnode.file_id,
                    page=self.page,
                ).pack(),
            )

        builder.adjust(1)
        return builder

    def build_pag_buttons(self) -> InlineKeyboardBuilder:
        """Builds the pagination buttons for navigating through fsnodes.

        :return: InlineKeyboardBuilder with pagination buttons.
        """
        if not hasattr(self.actions, "PAG_BACK") or not hasattr(self.actions, "PAG_NEXT"):
            msg = (
                "Pagination actions such as 'PAG_BACK' and 'PAG_NEXT' "
                "must be defined in the CallbackData's actions."
            )
            raise AttributeError(msg)

        builder = InlineKeyboardBuilder()

        total_fsnodes = len(self.fsnodes)
        total_pages = (total_fsnodes + self.page_size - 1) // self.page_size

        if total_pages > 1:
            if self.page > 0:
                builder.add(
                    InlineKeyboardButton(
                        text=LazyProxy("fsnode-pag-back-button"),
                        callback_data=self.actions_callback_data(
                            action=self.actions.PAG_BACK,
                            page=self.page,
                            **self.kwargs,
                        ).pack(),
                    ),
                )

            builder.button(text=f"{self.page + 1}/{total_pages}", callback_data="page")

            if total_pages - 1 > self.page:
                builder.add(
                    InlineKeyboardButton(
                        text=LazyProxy("fsnode-pag-next-button"),
                        callback_data=self.actions_callback_data(
                            action=self.actions.PAG_NEXT,
                            page=self.page,
                            **self.kwargs,
                        ).pack(),
                    ),
                )

        builder.adjust(3)
        return builder

    @abstractmethod
    def build_actions_buttons(self) -> InlineKeyboardBuilder:
        """Builds the actions buttons for the keyboard.

        :return: InlineKeyboardBuilder with actions buttons.
        """
        raise NotImplementedError
