from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import DatabaseManager
from utils.keyboards import get_cart_keyboard, get_metro_menu
from utils.messages import format_cart_message
from utils.helpers import generate_id

router = Router(name="cart_main")


@router.callback_query(F.data == "cart")
async def view_cart_callback(callback: CallbackQuery):
    """Handle view cart callback"""
    db = DatabaseManager()
    cart_items = db.get_user_cart(callback.from_user.id)
    
    if not cart_items:
        await callback.message.edit_text(
            "🛒 <b>Корзина</b>\n\n📭 Ваша корзина пуста.\n🛍 Добавьте товары из каталога!",
            parse_mode="HTML",
            reply_markup=get_metro_menu()
        )
        await callback.answer()
        return
    
    # Calculate total
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    text = format_cart_message(cart_items, total_price)
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_cart_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "view_cart")
async def view_cart_details_callback(callback: CallbackQuery):
    """Handle detailed cart view callback"""
    await view_cart_callback(callback)


@router.callback_query(F.data == "clear_cart")
async def clear_cart_callback(callback: CallbackQuery):
    """Handle clear cart callback"""
    db = DatabaseManager()
    db.clear_user_cart(callback.from_user.id)
    
    await callback.message.edit_text(
        "🗑 <b>Корзина очищена</b>\n\n✅ Все товары удалены из корзины.",
        parse_mode="HTML",
        reply_markup=get_metro_menu()
    )
    await callback.answer("Корзина очищена!")


@router.callback_query(F.data == "checkout_cart")  
async def checkout_cart_callback(callback: CallbackQuery):
    """Handle cart checkout callback"""
    db = DatabaseManager()
    cart_items = db.get_user_cart(callback.from_user.id)
    
    if not cart_items:
        await callback.answer("❌ Корзина пуста!", show_alert=True)
        return
    
    # Calculate total
    total_price = sum(item['price'] * item['quantity'] for item in cart_items)
    
    # Create order
    order_id = generate_id("CART")
    
    # Prepare order item description
    items_text = ", ".join([f"{item['name']} x{item['quantity']}" for item in cart_items])
    
    order_data = {
        'id': order_id,
        'user_id': callback.from_user.id,
        'item': f"Заказ корзины: {items_text}",
        'price': total_price,
        'status': 'Ожидает оплаты'
    }
    
    db.create_order(order_data)
    
    # Clear cart after creating order
    db.clear_user_cart(callback.from_user.id)
    
    text = (
        f"🛒 <b>Заказ оформлен</b>\n\n"
        f"🆔 <b>Номер заказа:</b> <code>{order_id}</code>\n"
        f"📦 <b>Товары:</b>\n"
    )
    
    for item in cart_items:
        text += f"• {item['name']} × {item['quantity']} = {item['price'] * item['quantity']} ₽\n"
    
    text += f"\n💰 <b>Итого:</b> {total_price} ₽\n\n"
    text += "💳 Для завершения заказа обратитесь в поддержку с номером заказа."
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML"
    )
    await callback.answer("Заказ создан!")


@router.callback_query(F.data == "edit_cart")
async def edit_cart_callback(callback: CallbackQuery):
    """Handle edit cart callback"""
    await callback.message.edit_text(
        "✏️ <b>Редактирование корзины</b>\n\n🚧 Функция в разработке.\nПока можно только очистить корзину полностью.",
        parse_mode="HTML",
        reply_markup=get_cart_keyboard()
    )
    await callback.answer()