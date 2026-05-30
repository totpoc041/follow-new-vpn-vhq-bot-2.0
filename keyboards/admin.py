"""
Админские клавиатуры.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_payment_confirm_buttons(user_id: int) -> InlineKeyboardBuilder:
    """
    Кнопки для подтверждения платежа админом.
    
    Args:
        user_id: ID пользователя
        
    Returns:
        InlineKeyboardBuilder с кнопками сумм
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="Пополнить на 111 руб.", callback_data=f"admin_balance_{user_id}_111")
    builder.button(text="Пополнить на 222 руб.", callback_data=f"admin_balance_{user_id}_222")
    builder.button(text="Пополнить на 333 руб.", callback_data=f"admin_balance_{user_id}_333")
    builder.button(text="Отменить", callback_data="cancel_payment")
    builder.adjust(2, 2)
    return builder


def admin_payment_done_buttons(user_id: int, duration: str) -> InlineKeyboardBuilder:
    """
    Кнопки подтверждения оплаты для админа (после получения чека).
    
    Args:
        user_id: ID пользователя
        duration: Длительность подписки
        
    Returns:
        InlineKeyboardBuilder с кнопкой подтверждения
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить оплату", callback_data=f"confirm_payment_to_admin-{user_id}-{duration}")
    return builder
