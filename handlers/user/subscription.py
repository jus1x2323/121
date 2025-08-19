from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ChatMemberStatus
import logging
from config.settings import CHANNEL_ID
from utils.keyboards import get_main_menu

router = Router(name="user_subscription")


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    """Handle subscription check callback"""
    try:
        chat_member = await callback.bot.get_chat_member(
            chat_id=CHANNEL_ID, 
            user_id=callback.from_user.id
        )
        
        is_subscribed = chat_member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
        
        if is_subscribed:
            welcome_text = (
                f"✅ Отлично, {callback.from_user.first_name}!\n\n"
                "🛍 Теперь вы можете пользоваться всеми функциями бота.\n"
                "Выберите интересующий вас раздел:"
            )
            
            await callback.message.edit_text(
                welcome_text,
                reply_markup=get_main_menu(),
                parse_mode="HTML"
            )
        else:
            await callback.answer(
                "❌ Вы ещё не подписались на канал. Подпишитесь и попробуйте снова.",
                show_alert=True
            )
        
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        await callback.answer(
            "❌ Произошла ошибка при проверке подписки. Попробуйте позже.",
            show_alert=True
        )