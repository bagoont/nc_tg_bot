from bot.dialogs import files, search, settings, trashbin

routers = (files.router, search.router, trashbin.router, settings.router)
