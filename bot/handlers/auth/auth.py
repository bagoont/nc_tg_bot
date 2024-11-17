"""Authentication in Nextcloud handler."""

from urllib.parse import urlparse

from aiogram.types import Message
from aiogram_i18n import I18nContext
from nc_py_api import AsyncNextcloud, NextcloudException
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core import settings
from bot.keyboards import menu_board
from bot.db.crud import get_user_by_tg_id, create_user

AUTH_TIMEOUT = 60 * 20
AUTH_TIMEOUT_IN_MIN = AUTH_TIMEOUT // 60


def replace_with_base_url(url: str) -> str:
    """Replce url for authentification with base url."""
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(settings.nc.BASEURL)

    netloc = parsed_base_url.hostname
    if parsed_base_url.port:
        netloc = f"{netloc}:{parsed_base_url.port}"

    return parsed_url._replace(
        scheme=parsed_base_url.scheme,
        netloc=netloc,
    ).geturl()


async def auth(message: Message, i18n: I18nContext, nc: AsyncNextcloud, db: AsyncSession) -> Message | bool:
    """Authenticate a user in Nextcloud.

    Initialize the login flow, polling for credentials, and add user to the database.

    :param message: Message object.
    :param i18n: Internationalization context.
    :param nc: Nextcloud API client.
    :param db: Database session.
    """
    if await get_user_by_tg_id(db, message.from_user.id):
        return await message.reply(text=i18n.get("already-authorized"), reply_markup=menu_board())

    init = await nc.loginflow_v2.init(user_agent=settings.APP_NAME)

    url = replace_with_base_url(init.login)
    if not url.startswith("https"):
        url = f"<code>{url}</code>"
    text = i18n.get("auth-init", url=url, timeout=AUTH_TIMEOUT_IN_MIN)
    init_message = await message.reply(text=text)

    try:
        credentials = await nc.loginflow_v2.poll(token=init.token, timeout=AUTH_TIMEOUT)
    except NextcloudException:
        return await init_message.edit_text(text=i18n.get("auth-timeout"))

    user = await create_user(
        db,
        tg_id=message.from_user.id,
        tg_name=message.from_user.username,
        login=credentials.login_name,
        app_password=credentials.app_password,
    )

    await init_message.edit_text(text=i18n.get("auth-success"))

    return await message.reply(text=i18n.get("auth-welcome"), reply_markup=menu_board())
