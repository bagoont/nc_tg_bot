from bot.dialogs import files, search, settings, trash_bin

routers = (files.router, search.router, trash_bin.router, settings.router)
