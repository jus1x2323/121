import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def send_subscription_request(chat_id: int, bot, message_id: int = None):
    """Send subscription request message to user"""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Подписаться", url="https://t.me/MRoyaleSH0P")],
        [InlineKeyboardButton(text="✅ Проверить подписку", callback_data="check_subscription")]
    ])
    
    text = "📢 Для работы с ботом необходимо подписаться на канал."

    try:
        if message_id:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=kb
            )
        else:
            await bot.send_message(
                chat_id,
                text,
                reply_markup=kb
            )
    except Exception as e:
        logging.error(f"Error sending subscription request: {e}")


def format_order_message(order_data: dict) -> str:
    """Format order data into a readable message"""
    message = f"📦 <b>Заказ #{order_data['id']}</b>\n\n"
    message += f"🛍 <b>Товар:</b> {order_data['item']}\n"
    message += f"💰 <b>Цена:</b> {order_data['price']} ₽\n"
    message += f"📅 <b>Дата:</b> {order_data['timestamp']}\n"
    message += f"📊 <b>Статус:</b> {order_data['status']}\n"
    
    if order_data.get('username'):
        message += f"👤 <b>Никнейм:</b> {order_data['username']}\n"
    
    if order_data.get('game_id'):
        message += f"🎮 <b>Game ID:</b> {order_data['game_id']}\n"
    
    return message


def format_item_message(item_data: dict, show_quantity: bool = True) -> str:
    """Format item data into a readable message"""
    message = f"📦 <b>{item_data['name']}</b>\n\n"
    message += f"💰 <b>Цена:</b> {item_data['price']} ₽\n"
    
    if item_data.get('description'):
        message += f"📝 <b>Описание:</b> {item_data['description']}\n"
    
    if show_quantity and item_data.get('quantity') is not None:
        message += f"📦 <b>В наличии:</b> {item_data['quantity']} шт.\n"
    
    if item_data.get('gift_link'):
        message += f"🔗 <b>Ссылка:</b> {item_data['gift_link']}\n"
    
    return message


def format_cart_message(cart_items: list, total_price: float) -> str:
    """Format cart items into a readable message"""
    if not cart_items:
        return "🛒 Ваша корзина пуста"
    
    message = "🛒 <b>Ваша корзина:</b>\n\n"
    
    for i, item in enumerate(cart_items, 1):
        message += f"{i}. <b>{item['name']}</b>\n"
        message += f"   💰 {item['price']} ₽ × {item['quantity']} = {item['price'] * item['quantity']} ₽\n\n"
    
    message += f"💳 <b>Итого:</b> {total_price} ₽"
    
    return message