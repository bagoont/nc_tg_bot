from aiogram_dialog import DialogManager


async def get_languages(dialog_manager: DialogManager, **middleware_data) -> dict:
    return {
        "languages": [
            ("ru", "🇷🇺", "Russian"),
            ("en", "🇬🇧", "English"),
        ]
    }
