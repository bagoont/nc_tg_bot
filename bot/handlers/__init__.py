from . import auth, common, files, search, settings, trashbin

routers = (common.router, auth.router, files.router, search.router, trashbin.router, settings.router)
