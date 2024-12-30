from enum import Enum

from aiogram.types import BotCommand


class Commands(Enum):
    auth = BotCommand(command="auth", description="Authenticate to use Nextcloud bot features.")
    help = BotCommand(command="help", description="Get help on using Nextcloud bot commands.")
    files = BotCommand(command="files", description="Interact with your Nextcloud files.")
    search = BotCommand(command="search", description="Search for files and folders in your Nextcloud account.")
    trash_bin = BotCommand(command="trashbin", description="Manage files and folders in your Nextcloud trash bin.")
    settings = BotCommand(command="settings", description="Configure your Nextcloud bot preferences.")
