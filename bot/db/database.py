"""Creates an asynchronous SQLAlchemy engine and session maker."""

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core import SQLITE_URL, settings

db_url = (
    URL.create(
        drivername=f"{settings.db.SYSTEM}+{settings.db.DRIVER}",
        username=settings.db.USERNAME,
        database=settings.db.DB,
        password=settings.db.PASSWORD,
        port=settings.db.PORT,
        host=settings.db.HOSTNAME,
    ).render_as_string(hide_password=False)
    if settings.db
    else SQLITE_URL
)
engine = create_async_engine(db_url)
session_maker = async_sessionmaker(engine)
