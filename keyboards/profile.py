"""
Клавиатуры для профиля пользователя.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder


V2BOX_IOS_URL = "https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690?l=ru"


def profile_type_keyboard() -> InlineKeyboardBuilder:
    """
    Выбор типа профиля (Hiddify или V2Ray).
    
    Returns:
        InlineKeyboardBuilder с кнопками выбора типа
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Hiddify профиль", callback_data="link_hiddify")
    builder.button(text="📱 V2Ray профиль", callback_data="link_v2ray")
    builder.button(text="◀️ Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder


def install_app_button_hiddify() -> InlineKeyboardBuilder:
    """
    Кнопки для скачивания приложения Hiddify.
    
    Returns:
        InlineKeyboardBuilder с кнопками платформ
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Установить V2Box", url=V2BOX_IOS_URL)
    builder.button(text="◀️ Назад", callback_data="download_app")
    builder.adjust(1)
    return builder


def install_app_button_v2ray() -> InlineKeyboardBuilder:
    """
    Кнопки для скачивания приложения V2Ray.
    
    Returns:
        InlineKeyboardBuilder с кнопками платформ
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Установить V2Box", url=V2BOX_IOS_URL)
    builder.button(text="◀️ Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder


def client_type_keyboard() -> InlineKeyboardBuilder:
    """
    Выбор клиента (Hiddify или V2Ray).
    
    Returns:
        InlineKeyboardBuilder с кнопками выбора
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Установить V2Box", url=V2BOX_IOS_URL)
    builder.button(text="◀️ Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder
