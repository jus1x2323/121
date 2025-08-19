from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.models import DatabaseManager
from utils.keyboards import get_main_menu
from utils.messages import format_order_message

router = Router(name="orders_history")


@router.callback_query(F.data == "history")
async def order_history_callback(callback: CallbackQuery):
    """Handle order history callback"""
    db = DatabaseManager()
    orders = db.get_user_orders(callback.from_user.id)
    
    if not orders:
        await callback.message.edit_text(
            "📋 <b>История заказов</b>\n\n"
            "📭 У вас пока нет заказов.\n"
            "🛍 Оформите первый заказ в главном меню!",
            parse_mode="HTML",
            reply_markup=get_main_menu()
        )
        await callback.answer()
        return
    
    # Show last 10 orders
    recent_orders = orders[:10]
    
    text = "📋 <b>История заказов</b>\n\n"
    
    for i, order in enumerate(recent_orders, 1):
        status_emoji = {
            'Ожидает проверки': '🔄',
            'Ожидает оплаты': '💳',
            'В обработке': '⏳',
            'Завершён': '✅',
            'Отменён': '❌'
        }.get(order['status'], '❓')
        
        text += f"{i}. <b>#{order['id']}</b>\n"
        text += f"   📦 {order['item']}\n"
        text += f"   💰 {order['price']} ₽\n"
        text += f"   {status_emoji} {order['status']}\n\n"
    
    if len(orders) > 10:
        text += f"📊 Показано {len(recent_orders)} из {len(orders)} заказов"
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_main_menu()
    )
    await callback.answer()