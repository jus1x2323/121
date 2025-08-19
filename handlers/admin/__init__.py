from aiogram import Router
from .basic import router as basic_router

# Create main admin router
router = Router(name="admin")

# Include sub-routers
router.include_router(basic_router)