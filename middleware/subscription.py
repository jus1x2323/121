from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
import logging
from config.settings import ADMIN_ID, CHANNEL_ID
from utils.messages import send_subscription_request


class SubscriptionMiddleware(BaseMiddleware):
    """Middleware for checking user subscription to channel"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        # Skip check for admin
        if event.from_user.id == ADMIN_ID:
            return await handler(event, data)

        # Skip check for start command and subscription verification
        if event.text and (event.text.startswith('/start') or event.text == '✅ Проверить подписку'):
            return await handler(event, data)

        # Check subscription
        if not await self.is_subscribed(event.from_user.id):
            await send_subscription_request(event.chat.id, self.bot)
            return

        return await handler(event, data)
    
    async def is_subscribed(self, user_id: int) -> bool:
        """Check if user is subscribed to the channel"""
        try:
            chat_member = await self.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
            return chat_member.status in [
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR
            ]
        except Exception as e:
            logging.error(f"Error checking subscription: {e}")
            return False