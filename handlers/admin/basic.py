from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config.settings import ADMIN_ID
from utils.keyboards import get_admin_menu
from database.models import DatabaseManager

router = Router(name="admin_basic")

# Filter for admin only
router.message.filter(F.from_user.id == ADMIN_ID)
router.callback_query.filter(F.from_user.id == ADMIN_ID)


@router.message(Command("admin"))
async def admin_command(message: Message):
    """Handle /admin command"""
    await message.answer(
        "🛠️ <b>Административная панель</b>\n\n"
        "Добро пожаловать в панель администратора.",
        reply_markup=get_admin_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "admin_menu")
async def admin_menu_callback(callback: CallbackQuery):
    """Handle admin menu callback"""
    await callback.message.edit_text(
        "🛠️ <b>Административная панель</b>\n\n"
        "Выберите действие:",
        reply_markup=get_admin_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: CallbackQuery):
    """Handle admin statistics callback"""
    db = DatabaseManager()
    
    try:
        with db.get_connection() as conn:
            cur = conn.cursor()
            
            # Get various statistics
            cur.execute("SELECT COUNT(*) FROM orders")
            total_orders = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'Завершён'")
            completed_orders = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(DISTINCT user_id) FROM orders")
            unique_users = cur.fetchone()[0]
            
            cur.execute("SELECT SUM(price) FROM orders WHERE status = 'Завершён'")
            total_revenue = cur.fetchone()[0] or 0
            
            cur.execute("SELECT COUNT(*) FROM banned_users")
            banned_users = cur.fetchone()[0]
            
        text = (
            "📊 <b>Статистика бота</b>\n\n"
            f"📦 <b>Заказы:</b>\n"
            f"• Всего заказов: {total_orders}\n"
            f"• Завершённых: {completed_orders}\n\n"
            f"👥 <b>Пользователи:</b>\n"
            f"• Уникальных покупателей: {unique_users}\n"
            f"• Заблокированных: {banned_users}\n\n"
            f"💰 <b>Выручка:</b>\n"
            f"• Общая выручка: {total_revenue} ₽"
        )
        
    except Exception as e:
        text = f"❌ Ошибка получения статистики: {str(e)}"
    
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_admin_menu()
    )
    await callback.answer()


@router.callback_query(F.data.in_({"admin_users", "admin_items", "admin_orders", "admin_mass_send", "admin_export_import"}))
async def admin_coming_soon(callback: CallbackQuery):
    """Handle admin sections in development"""
    section_names = {
        "admin_users": "👥 Управление пользователями",
        "admin_items": "📦 Управление товарами", 
        "admin_orders": "📋 Управление заказами",
        "admin_mass_send": "📢 Массовая рассылка",
        "admin_export_import": "📂 Экспорт/Импорт"
    }
    
    section_name = section_names.get(callback.data, "Раздел")
    
    await callback.message.edit_text(
        f"{section_name}\n\n🚧 Раздел находится в разработке.\nСкоро будет доступен!",
        parse_mode="HTML",
        reply_markup=get_admin_menu()
    )
    await callback.answer()