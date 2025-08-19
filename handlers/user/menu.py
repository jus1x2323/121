from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.keyboards import (
    get_main_menu, get_stars_menu, get_premium_menu, 
    get_metro_menu, get_sets_menu
)
from database.models import DatabaseManager

router = Router(name="user_menu")


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback: CallbackQuery):
    """Handle main menu callback"""
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>\n\nВыберите интересующий вас раздел:",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "stars")
async def stars_menu_callback(callback: CallbackQuery):
    """Handle stars menu callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("stars")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    text = (
        "⭐ <b>Telegram Stars</b>\n\n"
        "💫 Stars — это внутренняя валюта Telegram для:\n"
        "• Покупки стикеров и эмодзи\n"
        "• Поддержки каналов\n"
        "• Покупки товаров в магазинах ботов\n"
        "• Отправки подарков\n\n"
        "Выберите количество звёзд:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_stars_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "premium")
async def premium_menu_callback(callback: CallbackQuery):
    """Handle premium menu callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("premium")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    text = (
        "👑 <b>Telegram Premium</b>\n\n"
        "🌟 Получите доступ к эксклюзивным функциям:\n"
        "• Увеличенные лимиты загрузки\n"
        "• Эксклюзивные стикеры и эмодзи\n"
        "• Голосовые сообщения в текст\n"
        "• Премиум-темы и многое другое\n\n"
        "Выберите подходящий тариф:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_premium_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "metro")
async def metro_menu_callback(callback: CallbackQuery):
    """Handle metro menu callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("metro")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    text = (
        "🚇 <b>METRO ROYALE</b>\n\n"
        "⚔️ Лучшее снаряжение для выживания в метро:\n"
        "• Оружие всех типов\n"
        "• Броня и шлемы 6 уровня\n"
        "• Готовые наборы экипировки\n"
        "• Расходники и аксессуары\n\n"
        "Выберите категорию товаров:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_metro_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "metro_sets")
async def metro_sets_callback(callback: CallbackQuery):
    """Handle metro sets menu callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("metro_sets")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    text = (
        "🛡️ <b>Сеты снаряжения</b>\n\n"
        "🎯 Готовые комплекты брони 6-го уровня:\n"
        "• Полная защита головы и тела\n"
        "• Увеличенная вместимость рюкзака\n"
        "• Различные модификации на выбор\n\n"
        "Выберите подходящий сет:"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=get_sets_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "tg_accounts")
async def tg_accounts_callback(callback: CallbackQuery):
    """Handle telegram accounts callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("tg_accounts")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    # Get available accounts
    accounts = db.get_items_by_category('tg_accounts')
    
    if not accounts:
        await callback.message.edit_text(
            "📱 <b>Telegram Аккаунты</b>\n\n❌ В данный момент аккаунты отсутствуют в наличии.",
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    text = "📱 <b>Telegram Аккаунты</b>\n\n🔥 Готовые к использованию аккаунты:\n\n"
    
    for account in accounts[:10]:  # Show max 10 accounts
        if account['quantity'] > 0:
            text += f"• <b>{account['name']}</b>\n"
            text += f"  💰 {account['price']} ₽\n"
            text += f"  📦 В наличии: {account['quantity']} шт.\n\n"
    
    text += "💡 Для заказа обратитесь в поддержку."
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "nft")
async def nft_callback(callback: CallbackQuery):
    """Handle NFT callback"""
    db = DatabaseManager()
    section_status = db.get_section_status("nft")
    
    if not section_status['is_open']:
        await callback.answer(
            f"❌ Раздел временно закрыт: {section_status['close_reason']}", 
            show_alert=True
        )
        return
    
    # Get available NFTs
    nfts = db.get_items_by_category('nft_items')
    
    if not nfts:
        await callback.message.edit_text(
            "🖼 <b>NFT Коллекции</b>\n\n❌ В данный момент NFT отсутствуют в наличии.",
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        await callback.answer()
        return
    
    text = "🖼 <b>NFT Коллекции</b>\n\n✨ Эксклюзивные цифровые активы:\n\n"
    
    for nft in nfts[:10]:  # Show max 10 NFTs
        if nft['quantity'] > 0:
            text += f"• <b>{nft['name']}</b>\n"
            text += f"  💰 {nft['price']} ₽\n"
            text += f"  📦 В наличии: {nft['quantity']} шт.\n\n"
    
    text += "💡 Для заказа обратитесь в поддержку."
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.in_({"support", "reviews", "other_services", "order_script", "description_design", "autospamming", "my_projects"}))
async def coming_soon_callback(callback: CallbackQuery):
    """Handle coming soon sections"""
    section_map = {
        "support": "🆘 Поддержка",
        "reviews": "⭐ Отзывы", 
        "other_services": "🛠 Прочие Услуги",
        "order_script": "🧑‍💻 Заказ Скрипта",
        "description_design": "🎨 Оформление профиля",
        "autospamming": "🤖 AUTOSPAMMING Бот",
        "my_projects": "🌟 Мои Проекты"
    }
    
    section_name = section_map.get(callback.data, "Раздел")
    
    await callback.message.edit_text(
        f"{section_name}\n\n🚧 Раздел находится в разработке.\nСкоро будет доступен!",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()