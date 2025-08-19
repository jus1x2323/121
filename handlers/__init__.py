from .user import router as user_router
from .admin import router as admin_router
from .orders import router as orders_router
from .cart import router as cart_router

def register_handlers(dp):
    """Register all handlers"""
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(orders_router)
    dp.include_router(cart_router)