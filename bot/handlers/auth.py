from aiogram import Router, filters, types
from nc_py_api import AsyncNextcloud

from bot.core import settings
from bot.db import UserRepository
from bot.middlewares import NextcloudMD
from bot.utils import Commands

router: Router = Router(name="auth")

router.message.middleware.register(NextcloudMD())


@router.message(filters.Command(Commands.auth.value))
async def auth(message: types.Message, nc: AsyncNextcloud, users: UserRepository) -> None:
    if await users.get_by_tg_id(message.from_user.id):
        # TODO: To i18n.
        await message.reply(text="You are already authorized.")
        return

    init = await nc.loginflow_v2.init(user_agent=settings.APP_NAME)

    url = init.login
    if not url.startswith("https"):
        url = f"<pre>{init.login}</pre>"
    # TODO: To i18n.
    await message.answer(text=f"{url}")

    credentials = await nc.loginflow_v2.poll(token=init.token, timeout=settings.nc.AUTH_TIMEOUT)

    await users.add(
        language=message.from_user.language_code,
        tg_id=message.from_user.id,
        tg_name=message.from_user.username,
        login=credentials.login_name,
        app_password=credentials.app_password,
    )
    await users.session.commit()

    # TODO: To i18n.
    await message.reply(text="Auth success.")
