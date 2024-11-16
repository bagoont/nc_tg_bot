"""Routers and handlers."""

from .auth import auth_router
from .default import default_router
from .menu import menu_router

__all__ = (
    "default_router",
    "auth_router",
    "menu_router",
)

routers = (
    default_router,
    auth_router,
    menu_router,
)
