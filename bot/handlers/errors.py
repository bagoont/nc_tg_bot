import logging

from aiogram import F, Router
from aiogram.exceptions import AiogramError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from nc_py_api import NextcloudException

router: Router = Router(name="errors")

logger = logging.getLogger("aiogram.event")


@router.error(ExceptionTypeFilter(NextcloudException), F.update.exception.as_("exception"))
async def error_handler(event: ErrorEvent, exception: NextcloudException) -> None:
    try:
        if callback := event.update.callback_query:
            await callback.answer(exception.reason, show_alert=True)
        elif message := event.update.message:
            await message.reply(exception.reason)
    except AiogramError as e:
        # TODO: Write exc text.
        logger.exception("...", exc_info=e)
