"""Main and useful functions for handlers."""

from typing import Any, TypeVar

from aiogram.types import InlineKeyboardMarkup
from aiogram_i18n import I18nContext
from nc_py_api import FsNode

from bot.core import settings
from bot.keyboards import FsNodeMenuBoard, SearchBoard, TrashbinBoard
from bot.utils import MIME_SYMBOLS

R = TypeVar("R")


def get_human_readable_bytes(num: float, suffix: str = "B") -> str:
    """A function that convert a number of bytes into a human-readable format.

    :param num: The number of bytes to convert.
    :param suffix: The suffix to append to the converted value, defaults to "B".
    :return: A human-readable string representing the byte value.
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 2**10:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 2**10
    return f"{num:.1f}Yi{suffix}"


def get_page_items(
    item_list: list[R],
    page: int = 0,
    page_size: int = settings.TG_PAGE_SIZE,
) -> list[R]:
    """Return a slice of the input list `item_list` based on the provided `page` and `page_size`.

    :param item_list: The list from which to extract the items.
    :param page: The page number to retrieve. Defaults to 0.
    :param page_size: The number of items per page, defaults to `settings.TG_PAGE_SIZE`.
    :return: A list containing the items on the specified page.
    """
    start_index = page * page_size
    end_index = (page + 1) * page_size
    return item_list[start_index:end_index]


def get_fsnode_msg(
    i18n: I18nContext,
    fsnode: FsNode,
    attached_fsnodes: list[FsNode],
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup]:
    """Returns contenr for fsnode message."""
    text = i18n.get(
        "fsnode",
        type="dir" if fsnode.is_dir else "file",
        symbol="📂" if fsnode.is_dir else MIME_SYMBOLS.get(fsnode.info.mimetype, ""),
        name=fsnode.name,
        path=fsnode.user_path if fsnode.user_path else "/",
        user=fsnode.user,
        favorite="🌕" if fsnode.info.favorite else "🌑",
        size=get_human_readable_bytes(fsnode.info.size),
        last_modified=fsnode.info.last_modified,
    )
    reply_markup = FsNodeMenuBoard(
        fsnode=fsnode,
        attached_fsnodes=attached_fsnodes,
        **kwargs,
    ).get_kb()
    return text, reply_markup


def get_trashbin_msg(
    i18n: I18nContext,
    trashbin: list[FsNode],
    trashbin_size: int,
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup | None]:
    """Returns contenr for trashbin message."""
    if trashbin == []:
        text = i18n.get("trashbin-empty")
        return text, None
    fsnodes_on_page = get_page_items(trashbin, **kwargs)
    fsnodes_text = "\n".join(
        [
            i18n.get(
                "trashbin-item",
                path=fsnode.info.trashbin_original_location if fsnode.info.trashbin_original_location else "/",
            )
            for fsnode in fsnodes_on_page
        ],
    )
    trashbin_text = i18n.get(
        "trashbin",
        count=len(trashbin),
        size=get_human_readable_bytes(trashbin_size),
    )
    text = f"{trashbin_text}\n{fsnodes_text}"
    reply_markup = TrashbinBoard(
        fsnodes=trashbin,
        **kwargs,
    ).get_kb()
    return text, reply_markup


def get_search_msg(
    i18n: I18nContext,
    query: str,
    fsnodes: list[FsNode],
    **kwargs: Any,
) -> tuple[str, InlineKeyboardMarkup | None]:
    """Returns contenr for search message."""
    if fsnodes == []:
        text = i18n.get("search-empty")
        return text, None
    fsnodes_on_page = get_page_items(fsnodes, **kwargs)
    fsnodes_text = "\n".join(
        [i18n.get("search-item", path=fsnode.user_path if fsnode.user_path else "/") for fsnode in fsnodes_on_page],
    )
    text = f"{i18n.get('search', count=len(fsnodes), query=query)}\n{fsnodes_text}"
    reply_markup = SearchBoard(
        query=query,
        fsnodes=fsnodes,
        **kwargs,
    ).get_kb()
    return text, reply_markup
