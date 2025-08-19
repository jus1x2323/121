from aiogram import Router
from .cart import router as cart_router

# Create main cart router  
router = Router(name="cart")

# Include sub-routers
router.include_router(cart_router)