from typing import Any

from aiogram_dialog import DialogManager

from bot.core import settings
from bot.utils import LANG_SYMBOLS


async def get_languages(dialog_manager: DialogManager, **middleware_data: Any) -> dict[str, Any]:
    return {
        "languages": [
            {
                "iso": LANG_SYMBOLS[lang]["iso"],
                "symbol": LANG_SYMBOLS[lang]["symbol"],
                "name": LANG_SYMBOLS[lang]["name"],
            }
            for lang in settings.AVALIABLE_LANGUAGES
        ]
    }
