"""Configuration settings for the Nextcloud Telegram Bot.

This module contains classes that define the configuration settings necessary for the operation
of the Nextcloud Telegram Bot. These settings include database connection details, Redis
configuration, webhook settings, Nextcloud server details, and Telegram bot credentials.
"""

from pathlib import Path

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self

BASE_DIR = Path(__file__)

SQLITE_URL = "sqlite+aiosqlite:///./database.db"

MAX_TG_FILESIZE = 50 * 2**20
MIN_CHUNK_SIZE = 5 * 2**20
MAX_CHUNK_SIZE = 2**31


class Webhook(BaseSettings):
    """Configuration for a webhook endpoint.

    Webhook settings are optional and are used when the bot is configured
    to receive updates via a webhook.

    :param WEBHOOK_BASE_URL: The base URL for the webhook endpoint.
    :param WEBHOOK_HOST: The host of webhook.
    :param WEBHOOK_PORT: The port number on which the webhook server listens.
    :param WEBHOOK_PATH: The path under which the webhook endpoint is accessible.
    :param WEBHOOK_SECRET: A secret token used for webhook verification, defaults to None.
    """

    BASEURL: str
    HOST: str
    PORT: int
    PATH: str
    SECRET: str | None = None


class Nextcloud(BaseSettings):
    """Configuration to communicate with a Nextcloud server.

    :param NC_BASE_URL:
    :param NC_SCHEME: Protocol used to communicate with the Nextcloud server, defaults to "https".
    :param NC_HOST: Hostname of the Nextcloud server.
    :param NC_PORT: Port number on which the Nextcloud server listens, defaults to 80.
    :param NC_FILE_SIZE:
    :param NC_CHUNK_SIZE: Maximum size of file chunks for uploads, defaults to MIN_CHUNK_SIZE.
    """

    SCHEME: str = "https"
    HOST: str
    PORT: int = 443
    FILESIZE: int = 5 * 2**40
    CHUNKSIZE: int = MIN_CHUNK_SIZE
    BASEURL: str = ""
    AUTH_TIMEOUT: int = 20 * 60  # TODO: Add validation. Must less than 20 min.

    @model_validator(mode="after")
    def validate_baseurl(self) -> Self:
        """Validate and set the BASEURL attribute of the model."""
        if self.BASEURL == "":
            self.BASEURL = f"{self.SCHEME}://{self.HOST}:{self.PORT}"
        return self

    @field_validator("CHUNKSIZE")
    @classmethod
    def validate_chunksize(cls, v: int) -> int:
        """Validates the chunk size against minimum and maximum limits."""
        if MIN_CHUNK_SIZE > v > MAX_CHUNK_SIZE:
            msg = f"The size of chunks must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
            raise ValueError(msg)
        return v


class Database(BaseSettings):
    """Configuration for connecting to a database.

    :param DB_USERNAME: The username for database authentication.
    :param DB_PASSWORD: The password for database authentication.
    :param DB_HOSTNAME: The hostname of the database server.
    :param DB_PORT: The port number on which the database server listens, defaults to 5432.
    :param DB_DB: The name of the database.
    :param DB_DRIVER: The database driver to use, defaults to "asyncpg".
    :param DB_SYSTEM: The type of database system, defaults to "postgresql".
    """

    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: int = 5432
    DB: str
    DRIVER: str = "asyncpg"
    SYSTEM: str = "postgresql"


class Redis(BaseSettings):
    """Configuration for connecting to a Redis cache.

    Redis connection settings are optional and fall back to in-memory storage if not provided.

    :param REDIS_USERNAME: Uername for Redis authentication, defaults to None.
    :param REDIS_PASSWORD: Password for Redis authentication, defaults to None.
    :param REDIS_HOSTNAME: Hostname of the Redis server.
    :param REDIS_PORT: Port number on which the Redis server listens, defaults to 6379.
    :param REDIS_DB: Database number within Redis to connect to, defaults to 1.
    """

    USERNAME: str | None = None
    PASSWORD: str | None = None
    DB: str | int = 0
    HOSTNAME: str
    PORT: int = 6379


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="_",
    )
    DEBUG: bool = False
    APP_NAME: str = "Nextcloud Telegram Bot"
    # TODO: Validate if DEFAULT_LANGUAGE in AVLAIABLE_LANGUAGE
    DEFAULT_LANGUAGE: str = "en"
    AVALIABLE_LANGUAGES: list[str] = ["en", "ru"]
    LOG_LEVEL: str = "INFO"

    TG_TOKEN: str
    TG_SCROLLING_HEIGHT: int = 8
    TG_FILESIZE: int = MAX_TG_FILESIZE
    TG_CHUNK_SIZE: int = MIN_CHUNK_SIZE
    TG_DROP_PENDING_UPDATES: bool = True
    TG_API_SERVER: str | None = None
    TG_LOCAL_MODE: bool = False

    nc: Nextcloud
    db: Database | None = None
    redis: Redis | None = None
    webhook: Webhook | None = None

    @field_validator("TG_CHUNK_SIZE")
    @classmethod
    def validate_chunksize(cls, v: int) -> int:
        """Validates the chunk size against minimum and maximum limits."""
        if MIN_CHUNK_SIZE > v > MAX_TG_FILESIZE:
            msg = f"The size of chunks must be between {MIN_CHUNK_SIZE} and {MAX_CHUNK_SIZE}."
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_local_mode(self) -> Self:
        """Checks if the `local_mode` field is True and if the `api_server` field is None."""
        if self.TG_LOCAL_MODE and self.TG_API_SERVER is None:
            msg = "Local mode requires API server to be set."
            raise ValueError(msg)
        return self


settings = Settings()
