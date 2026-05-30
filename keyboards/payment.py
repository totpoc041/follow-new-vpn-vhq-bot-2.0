"""
Клавиатуры для платежей.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder


def confirm_payment_button(user_id: int) -> InlineKeyboardBuilder:
    """
    Кнопка подтверждения оплаты.
    
    Args:
        user_id: ID пользователя
        
    Returns:
        InlineKeyboardBuilder с кнопками
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="💵 Подтвердить оплату", callback_data="confirm_payment")
    builder.button(text="◀️ Назад", callback_data="reg_subscription")
    return builder


def confirm_payment_button_done(user_id: int) -> InlineKeyboardBuilder:
    """
    Кнопка после подтверждения оплаты.
    
    Args:
        user_id: ID пользователя
        
    Returns:
        InlineKeyboardBuilder с кнопкой назад
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад", callback_data="reg_subscription")
    return builder


def admin_payment_buttons(user_id: int) -> InlineKeyboardBuilder:
    """
    Админские кнопки для пополнения баланса пользователя.
    
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
