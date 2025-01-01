"""This package is used for a bot logic implementation."""
from .help import help_router
from .start import start_router
from .commands import commands_router
from .admin import admin_router

routers = (admin_router, start_router, help_router, commands_router,)
