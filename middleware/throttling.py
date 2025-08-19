from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from cachetools import TTLCache
from config.settings import CACHE_MAX_SIZE, CACHE_TTL

# Initialize throttle cache
throttle_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL)


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware for throttling user requests"""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            user_id = user.id
            if user_id in throttle_cache:
                # User is throttled, ignore request
                return
            throttle_cache[user_id] = 1
        
        return await handler(event, data)