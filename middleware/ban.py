from aiogram import BaseMiddleware
from database.models import DatabaseManager


class BanCallbackMiddleware(BaseMiddleware):
    """Middleware for checking if user is banned on callback queries"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id
        
        # Check if user is banned (allow certain callbacks for banned users)
        if await self.db.is_user_banned(user_id) and event.data not in ["settings", "user_status", "main_menu"]:
            await event.answer("🚫 Вы заблокированы и не можете выполнять действия", show_alert=True)
            return
        
        return await handler(event, data)