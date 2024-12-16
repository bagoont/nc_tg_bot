"""Base model class for SQLAlchemy ORM."""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

uuid_pk = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True, default=uuid.uuid4)]


class Base(DeclarativeBase):
    """The base class for all models."""

    __allow_unmapped__ = False

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
