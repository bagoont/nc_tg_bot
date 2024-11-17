from sqlalchemy import select, update, delete, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import User
from bot.db.crud.exceptions import UserAlreadyExistsException, UserNotFoundException


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
    """Returns user by tg-id.

    :param session: An `AsyncSession` object.
    :param tg_id: A Telegram ID.
    :return: `User` or `None`.
    """
    stmt = select(User).where(User.tg_id == tg_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    """Returns user by its id.

    :param session: An `AsyncSession` object.
    :param user_id: An ID.
    :return: `User` or `None`.
    """
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_user(session: AsyncSession, tg_id: int, tg_name: str | None, login: str, app_password: str) -> User:
    """Creates `User` object.

    :return: Created `User`
    """
    existed_user = await get_user_by_tg_id(session, tg_id)
    if existed_user is not None:
        raise UserAlreadyExistsException(username=tg_name)

    obj = User(tg_id=tg_id, tg_name=tg_name, login=login, app_password=app_password)

    session.add(obj)
    await session.flush()
    await session.refresh(obj)

    return obj


async def update_user(
    session: AsyncSession,
    user_id: UUID,
    tg_id: str | None = None,
    tg_name: str | None = None,
    login: str | None = None,
    app_password: str | None = None,
) -> User:
    """Updates user.

    :param session:
    :param user_id:
    :param telegram_id:
    :param full_name:
    :return:
    """
    user = await get_user_by_id(session, user_id)

    if user is None:
        raise UserNotFoundException(user_id=user_id)

    stmt = update(User).where(User.id == user_id)

    if tg_id is not None:
        stmt = stmt.values(tg_id=tg_id)
    if tg_name is not None:
        stmt = stmt.values(tg_name=tg_name)
    if login is not None:
        stmt = stmt.values(login=login)
    if app_password is not None:
        stmt = stmt.values(app_password=app_password)

    await session.execute(stmt)

    updated_user = await get_user_by_id(session, user_id)

    if updated_user is None:
        raise RuntimeError

    return updated_user


async def delete_user(session: AsyncSession, user_id: UUID) -> None:
    """Deletes `User` object.

    :param user_id:
    :param session: An `AsyncSession` object
    :return:
    """
    if await get_user_by_id(session, user_id) is None:
        raise ValueError("Invalid user ID passed.")

    stmt = delete(User).where(User.id == user_id)

    await session.execute(stmt)
