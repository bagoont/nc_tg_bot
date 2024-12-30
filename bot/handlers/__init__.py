from bot.core import settings
from bot.handlers import auth, errors

routers = [auth.router]

if not settings.DEBUG:
    routers.append(errors.router)
