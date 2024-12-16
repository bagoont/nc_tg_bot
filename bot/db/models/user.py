"""User model."""

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from bot.db.models import Base, uuid_pk


class User(Base):
    """User model.

    :param id: Unique Telegram identifier for the user, primary key.
    :param nc_login: The user's Nextcloud login name.
    :param nc_app_password: The user's Nextcloud app password.
    :param name: The user's name, extracted from their Telegram profile.
    :param first_name: The user's first name, extracted from their Telegram profile.
    :param last_name: The user's last name, extracted from their Telegram profile.
    """

    __tablename__ = "users"

    id: Mapped[uuid_pk]
    language: Mapped[str] = mapped_column(String(3))
    tg_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    tg_name: Mapped[str] = mapped_column(nullable=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    app_password: Mapped[str] = mapped_column(nullable=False)

    @property
    def url(self) -> str:
        """Generates a URL for the user's profile page, typically used for linking purposes."""
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        """Generates a mention string for the user, suitable for use in chat messages."""
        return html.link(value=self.tg_name, link=self.url)
