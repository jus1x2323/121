from aiogram import Router
from .basic import router as basic_router
from .menu import router as menu_router
from .subscription import router as subscription_router

# Create main user router
router = Router(name="user")

# Include sub-routers
router.include_router(basic_router)
router.include_router(menu_router) 
router.include_router(subscription_router)