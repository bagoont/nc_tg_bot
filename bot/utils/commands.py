import enum

from aiogram.types import BotCommand


class Commands(enum.Enum):
    auth = BotCommand(command="auth", description="Authenticate to use Nextcloud bot features.")
    help = BotCommand(command="help", description="Get help on using Nextcloud bot commands.")
    files = BotCommand(command="files", description="Interact with your Nextcloud files.")
    search = BotCommand(command="search", description="Search for files and folders in your Nextcloud account.")
    trashbin = BotCommand(command="trashbin", description="Manage files and folders in your Nextcloud trashbin.")
    settings = BotCommand(command="settings", description="Configure your Nextcloud bot preferences.")
