from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    """Get main menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌟 Мои Проекты", callback_data="my_projects")],
        [
            InlineKeyboardButton(text="💫 Telegram STARS", callback_data="stars"),
            InlineKeyboardButton(text="👑 Telegram PREMIUM", callback_data="premium")
        ],
        [InlineKeyboardButton(text="📱 Telegram Аккаунты", callback_data="tg_accounts")],
        [InlineKeyboardButton(text="🖼 NFT Коллекции", callback_data="nft")],
        [
            InlineKeyboardButton(text="🧑‍💻 Заказать Скрипт", callback_data="order_script"),
            InlineKeyboardButton(text="🎨 Оформление профиля", callback_data="description_design")
        ],
        [
            InlineKeyboardButton(text="🚇 METRO ROYALE", callback_data="metro"),
            InlineKeyboardButton(text="🤖 AUTOSPAMMING Бот", callback_data="autospamming")
        ],
        [InlineKeyboardButton(text="🛠 Прочие Услуги", callback_data="other_services")],
        [
            InlineKeyboardButton(text="📋 История заказов", callback_data="history"),
            InlineKeyboardButton(text="⭐ Отзывы", callback_data="reviews")
        ],
        [
            InlineKeyboardButton(text="🆘 Поддержка", callback_data="support"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        ]
    ])


def get_stars_menu():
    """Get stars menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="15 🌟", callback_data="star_15"),
         InlineKeyboardButton(text="25 🌟", callback_data="star_25")],
        [InlineKeyboardButton(text="30 🌟", callback_data="star_30"),
         InlineKeyboardButton(text="45 🌟", callback_data="star_45")],
        [InlineKeyboardButton(text="50 🌟", callback_data="star_50"),
         InlineKeyboardButton(text="100 🌟", callback_data="star_100")],
        [InlineKeyboardButton(text="150 🌟", callback_data="star_150"),
         InlineKeyboardButton(text="300 🌟", callback_data="star_300")],
        [InlineKeyboardButton(text="500 🌟", callback_data="star_500"),
         InlineKeyboardButton(text="750 🌟", callback_data="star_750")],
        [InlineKeyboardButton(text="1000 🌟", callback_data="star_1000"),
         InlineKeyboardButton(text="Другое количество🌟", callback_data="star_other")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="main_menu")]
    ])


def get_premium_menu():
    """Get premium menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 1 мес. с заходом", callback_data="prem_1m")],
        [InlineKeyboardButton(text="🎁 3 мес. без захода", callback_data="prem_3m")],
        [InlineKeyboardButton(text="🎁 6 мес. без захода", callback_data="prem_6m")],
        [InlineKeyboardButton(text="🎁 12 мес. без захода", callback_data="prem_12m")],
        [InlineKeyboardButton(text="🎁 12 мес. с заходом", callback_data="prem_12m2")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="main_menu")]
    ])


def get_metro_menu():
    """Get metro menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧰 Наборы", callback_data="metro_kits"),
         InlineKeyboardButton(text="🛡️ Сеты", callback_data="metro_sets"),
         InlineKeyboardButton(text="💊 Расходники", callback_data="metro_consumables")],
        [InlineKeyboardButton(text="🪖 Шлем", callback_data="metro_helmets"),
         InlineKeyboardButton(text="🧥 Бронь", callback_data="metro_armor"),
         InlineKeyboardButton(text="🎒 Рюкзак", callback_data="metro_backpacks")],
        [InlineKeyboardButton(text="🔫 Оружие", callback_data="metro_weapons"),
         InlineKeyboardButton(text="🎮 Услуги", callback_data="metro_services")],
        [InlineKeyboardButton(text="🌟 Золотые вещи", callback_data="gold_items")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="main_menu"),
         InlineKeyboardButton(text="🛒 Корзина", callback_data="cart")]
    ])


def get_sets_menu():
    """Get sets menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Обычный сет", callback_data="set_normal")],
        [InlineKeyboardButton(text="🐍 Сет Кобра", callback_data="set_cobra")],
        [InlineKeyboardButton(text="💎 Сет Стальной фронт", callback_data="set_steel")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="metro")]
    ])


def get_admin_menu():
    """Get admin menu keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Управление пользователями", callback_data="admin_users")],
        [InlineKeyboardButton(text="📦 Управление товарами", callback_data="admin_items")],
        [InlineKeyboardButton(text="📋 Управление заказами", callback_data="admin_orders")],
        [InlineKeyboardButton(text="🔧 Управление разделами", callback_data="admin_manage_sections")],
        [InlineKeyboardButton(text="📢 Массовая рассылка", callback_data="admin_mass_send")],
        [InlineKeyboardButton(text="📂 Экспорт/Импорт", callback_data="admin_export_import")]
    ])


def get_requisites_kb(back_to: str = "main_menu"):
    """Get requisites keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Получить реквизиты", callback_data="get_requisites")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data=back_to)]
    ])


def get_payment_sent_kb(back_to: str = "main_menu"):
    """Get payment sent keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Платёж отправлен", callback_data="payment_sent")],
        [InlineKeyboardButton(text="🔄 Новые реквизиты", callback_data="new_requisites")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data=back_to)]
    ])


def get_after_payment_kb():
    """Get after payment keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 История заказов", callback_data="history")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])


def get_account_class_menu():
    """Get account class selection keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 Низкий класс", callback_data="class_low")],
        [InlineKeyboardButton(text="📱 Средний класс", callback_data="class_medium")],
        [InlineKeyboardButton(text="📱 Высокий класс", callback_data="class_high")],
        [InlineKeyboardButton(text="❌ Отклонить", callback_data="class_reject")]
    ])


def get_back_button(callback_data: str = "main_menu"):
    """Get back button"""
    return InlineKeyboardButton(text="↩️ Назад", callback_data=callback_data)


def get_requisites_button():
    """Get requisites button"""
    return InlineKeyboardButton(text="💳 Получить реквизиты", callback_data="get_requisites")


def get_cart_keyboard():
    """Get cart management keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Посмотреть корзину", callback_data="view_cart")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_cart")],
        [InlineKeyboardButton(text="🗑 Очистить корзину", callback_data="clear_cart")],
        [InlineKeyboardButton(text="💳 Оформить заказ", callback_data="checkout_cart")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="metro")]
    ])