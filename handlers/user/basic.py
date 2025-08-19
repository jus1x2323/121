from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from utils.keyboards import get_main_menu

router = Router(name="user_basic")


@router.message(Command("start"))
async def start_command(message: Message):
    """Handle /start command"""
    welcome_text = (
        f"👋 Добро пожаловать, {message.from_user.first_name}!\n\n"
        "🛍 Это магазин цифровых товаров и услуг.\n"
        "Выберите интересующий вас раздел из меню ниже:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )


@router.message(Command("help"))
async def help_command(message: Message):
    """Handle /help command"""
    help_text = (
        "🆘 <b>Помощь по использованию бота</b>\n\n"
        "📍 Основные функции:\n"
        "• 🌟 Покупка Telegram Stars\n"
        "• 👑 Покупка Telegram Premium\n"
        "• 📱 Готовые Telegram аккаунты\n"
        "• 🖼 NFT коллекции\n"
        "• 🚇 Товары Metro Royale\n"
        "• 🎨 Оформление профилей\n"
        "• 🧑‍💻 Заказ скриптов\n\n"
        "💡 Для навигации используйте кнопки меню.\n"
        "🆘 При проблемах обращайтесь в поддержку."
    )
    
    await message.answer(help_text, parse_mode="HTML")


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message):
    """Handle unknown commands"""
    await message.answer(
        "❓ Неизвестная команда. Используйте /help для получения справки.",
        reply_markup=get_main_menu()
    )