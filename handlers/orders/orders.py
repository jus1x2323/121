from aiogram import Router, F
from aiogram.types import CallbackQuery
from utils.keyboards import get_requisites_kb
from database.models import DatabaseManager
from utils.helpers import generate_id
from utils.messages import format_order_message

router = Router(name="orders_main")

# Star prices mapping
STAR_PRICES = {
    "star_15": (15, 95),
    "star_25": (25, 155),
    "star_30": (30, 185),
    "star_45": (45, 275),
    "star_50": (50, 305),
    "star_100": (100, 599),
    "star_150": (150, 895),
    "star_300": (300, 1785),
    "star_500": (500, 2975),
    "star_750": (750, 4465),
    "star_1000": (1000, 5950)
}

# Premium prices mapping
PREMIUM_PRICES = {
    "prem_1m": ("1 месяц с заходом", 199),
    "prem_3m": ("3 месяца без захода", 459),
    "prem_6m": ("6 месяцев без захода", 899),
    "prem_12m": ("12 месяцев без захода", 1699),
    "prem_12m2": ("12 месяцев с заходом", 1999)
}


@router.callback_query(F.data.startswith("star_"))
async def handle_star_order(callback: CallbackQuery):
    """Handle star order callback"""
    if callback.data == "star_other":
        await callback.message.edit_text(
            "💫 <b>Другое количество звёзд</b>\n\n"
            "📝 Для заказа нестандартного количества звёзд обратитесь в поддержку:\n"
            "• Укажите желаемое количество\n"
            "• Мы рассчитаем стоимость\n"
            "• Предоставим реквизиты для оплаты",
            parse_mode="HTML",
            reply_markup=get_requisites_kb("stars")
        )
        await callback.answer()
        return
    
    if callback.data not in STAR_PRICES:
        await callback.answer("❌ Неверный выбор", show_alert=True)
        return
    
    stars_count, price = STAR_PRICES[callback.data]
    
    # Create order
    db = DatabaseManager()
    order_id = generate_id("STAR")
    
    order_data = {
        'id': order_id,
        'user_id': callback.from_user.id,
        'item': f"{stars_count} Telegram Stars",
        'price': price,
        'status': 'Ожидает оплаты'
    }
    
    db.create_order(order_data)
    
    text = (
        f"⭐ <b>Заказ создан</b>\n\n"
        f"🆔 <b>Номер заказа:</b> <code>{order_id}</code>\n"
        f"🌟 <b>Товар:</b> {stars_count} Telegram Stars\n"
        f"💰 <b>Цена:</b> {price} ₽\n\n"
        f"💳 Нажмите кнопку ниже для получения реквизитов оплаты."
    )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_requisites_kb("stars")
    )
    await callback.answer()


@router.callback_query(F.data.startswith("prem_"))
async def handle_premium_order(callback: CallbackQuery):
    """Handle premium order callback"""
    if callback.data not in PREMIUM_PRICES:
        await callback.answer("❌ Неверный выбор", show_alert=True)
        return
    
    period, price = PREMIUM_PRICES[callback.data]
    
    # Create order
    db = DatabaseManager()
    order_id = generate_id("PREM")
    
    order_data = {
        'id': order_id,
        'user_id': callback.from_user.id,
        'item': f"Telegram Premium - {period}",
        'price': price,
        'status': 'Ожидает оплаты'
    }
    
    db.create_order(order_data)
    
    text = (
        f"👑 <b>Заказ создан</b>\n\n"
        f"🆔 <b>Номер заказа:</b> <code>{order_id}</code>\n"
        f"📅 <b>Товар:</b> Telegram Premium - {period}\n"
        f"💰 <b>Цена:</b> {price} ₽\n\n"
        f"💳 Нажмите кнопку ниже для получения реквизитов оплаты."
    )
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_requisites_kb("premium")
    )
    await callback.answer()


@router.callback_query(F.data == "get_requisites")
async def get_requisites_callback(callback: CallbackQuery):
    """Handle get requisites callback"""
    requisites_text = (
        "💳 <b>Реквизиты для оплаты</b>\n\n"
        "🏦 <b>Способы оплаты:</b>\n"
        "• Сбербанк: <code>1234 5678 9012 3456</code>\n"
        "• Тинькофф: <code>2200 1234 5678 9012</code>\n"
        "• ЮMoney: <code>41001234567890</code>\n"
        "• QIWI: <code>+79123456789</code>\n\n"
        "💡 <b>Важно:</b>\n"
        "• Укажите в комментарии номер заказа\n"
        "• После оплаты отправьте скриншот чека\n"
        "• Обработка заявки до 24 часов\n\n"
        "❓ Вопросы? Обращайтесь в поддержку!"
    )
    
    await callback.message.edit_text(
        requisites_text,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "payment_sent")
async def payment_sent_callback(callback: CallbackQuery):
    """Handle payment sent callback"""
    await callback.message.edit_text(
        "✅ <b>Платёж принят</b>\n\n"
        "📝 Ваша заявка поставлена в очередь на обработку.\n"
        "⏰ Время обработки: до 24 часов\n\n"
        "📱 Вы получите уведомление о статусе заказа.\n"
        "📋 Проверить статус можно в разделе 'История заказов'.",
        parse_mode="HTML"
    )
    await callback.answer("Платёж зарегистрирован!")