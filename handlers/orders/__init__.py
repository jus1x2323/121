from aiogram import Router
from .orders import router as orders_router
from .history import router as history_router

# Create main orders router
router = Router(name="orders")

# Include sub-routers
router.include_router(orders_router)
router.include_router(history_router)