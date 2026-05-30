"""
Клавиатуры для профиля пользователя.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder


V2BOX_IOS_URL = "https://apps.apple.com/us/app/v2box-v2ray-client/id6446814690?l=ru"
HIDDIFY_IOS_URL = "https://apps.apple.com/us/app/hiddify-proxy-vpn/id6596777532?platform=iphone"
HIDDIFY_ANDROID_URL = "https://play.google.com/store/apps/details?id=app.hiddify.com"
HIDDIFY_WINDOWS_URL = "https://apps.microsoft.com/detail/9pdfnl3qv2s5?hl=ru-RU&gl=RU"
HIDDIFY_MACOS_URL = "https://github.com/hiddify/hiddify-app/releases/latest/download/Hiddify-MacOS.dmg"
V2RAY_IOS_URL = "https://apps.apple.com/en/app/v2raytun/id6476628951"
V2RAY_ANDROID_URL = "https://play.google.com/store/apps/details?id=com.v2raytun.android"
V2RAY_WINDOWS_URL = "https://apps.microsoft.com/detail/9pdfnl3qv2s5?hl=ru-RU&gl=RU"
V2RAY_MACOS_URL = "https://apps.apple.com/en/app/v2raytun/id6476628951"


def profile_type_keyboard() -> InlineKeyboardBuilder:
    """
    Выбор типа профиля (Hiddify или V2Ray).
    
    Returns:
        InlineKeyboardBuilder с кнопками выбора типа
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Hiddify профиль", callback_data="link_hiddify")
    builder.button(text="📱 V2Box профиль", callback_data="link_v2box")
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
    builder.button(text="📱 iOS", url=HIDDIFY_IOS_URL)
    builder.button(text="🤖 Android", url=HIDDIFY_ANDROID_URL)
    builder.button(text="💻 Windows", url=HIDDIFY_WINDOWS_URL)
    builder.button(text="🍏 MacOS", url=HIDDIFY_MACOS_URL)
    builder.button(text="◀️ Назад", callback_data="download_app")
    builder.adjust(2, 2, 1)
    return builder


def install_app_button_v2ray() -> InlineKeyboardBuilder:
    """
    Кнопки для скачивания приложения V2Ray.
    
    Returns:
        InlineKeyboardBuilder с кнопками платформ
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 iOS", url=V2RAY_IOS_URL)
    builder.button(text="🤖 Android", url=V2RAY_ANDROID_URL)
    builder.button(text="💻 Windows", url=V2RAY_WINDOWS_URL)
    builder.button(text="🍏 MacOS", url=V2RAY_MACOS_URL)
    builder.button(text="◀️ Назад", callback_data="download_app")
    builder.adjust(2, 2, 1)
    return builder


def install_app_button_v2box() -> InlineKeyboardBuilder:
    """
    Кнопки для скачивания приложения V2Box.

    Returns:
        InlineKeyboardBuilder с кнопками платформ
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 iOS", url=V2BOX_IOS_URL)
    builder.button(text="◀️ Назад", callback_data="download_app")
    builder.adjust(1)
    return builder


def client_type_keyboard() -> InlineKeyboardBuilder:
    """
    Выбор клиента (Hiddify или V2Ray).
    
    Returns:
        InlineKeyboardBuilder с кнопками выбора
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Hiddify", callback_data="download_app_hiddify")
    builder.button(text="📱 V2Box", callback_data="download_app_v2box")
    builder.button(text="📱 V2Ray", callback_data="download_app_v2ray")
    builder.button(text="◀️ Назад", callback_data="main_menu")
    builder.adjust(1)
    return builder
