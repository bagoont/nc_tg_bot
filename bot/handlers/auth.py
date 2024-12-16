from aiogram import Router, filters, types
from httpx import ConnectError
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.db import UserRepository, session_maker
from bot.middlewares import DatabaseMD, NextcloudMD
from bot.utils import Commands

AUTH_TIMEOUT = 60 * 20
AUTH_TIMEOUT_IN_MIN = AUTH_TIMEOUT // 60

router = Router(name="auth")

router.message.outer_middleware.register(DatabaseMD(session_maker))
router.message.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.auth.value))
async def auth(message: types.Message, nc: AsyncNextcloud, users: UserRepository) -> None:
    if not message.from_user:
        return

    if await users.get_by_tg_id(message.from_user.id):
        await message.reply(text="You are already authorized.")
        return

    init = await nc.loginflow_v2.init(user_agent=settings.APP_NAME)

    url = init.login
    if not url.startswith("https"):
        url = f"<code>{init.login}</code>"
    auth_message = await message.reply(text=f"{url}")

    try:
        credentials = await nc.loginflow_v2.poll(token=init.token, timeout=AUTH_TIMEOUT)
    except ConnectError:
        await auth_message.edit_text(text="Auth timeout.")

    await users.add(
        language=message.from_user.language_code,
        tg_id=message.from_user.id,
        tg_name=message.from_user.username,
        login=credentials.login_name,
        app_password=credentials.app_password,
    )
    await users.session.commit()

    await auth_message.edit_text(text="Auth success.")
