"""
Telegram бот для управления подписками Hiddify VPN.

Точка входа приложения. Инициализирует бота, сервисы и запускает polling.
"""

import asyncio
import logging
import time

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

import config
import database as db

from handlers import commands, callbacks, messages, admin
from handlers.callbacks import init_services
from services.notification_service import NotificationService
from services.hiddify_service import HiddifyService


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Инициализация бота и диспетчера
bot = Bot(token=config.BotConfig.TOKEN)
dp = Dispatcher()

# Инициализация базы данных
db.init_db()


async def start_notification_scheduler():
    """Запустить фоновую задачу уведомлений об истечении подписки."""
    hiddify_service = HiddifyService()
    notification_service = NotificationService(bot, hiddify_service)
    await notification_service.start_scheduled_notifications()


async def watchdog_task():
    """Фоновая задача для Docker Healthcheck."""
    while True:
        try:
            with open("/tmp/bot_alive.txt", "w", encoding="utf-8") as alive_file:
                alive_file.write(str(time.time()))
        except Exception as exc:
            logger.error("Ошибка Watchdog: %s", exc)
        await asyncio.sleep(30 * 60)


async def on_startup():
    """Выполняется при запуске бота."""
    logger.info("Бот запускается...")
    
    # Инициализируем сервисы для обработчиков
    init_services(bot)
    
    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(messages.router)
    dp.include_router(admin.router)
    
    # Запускаем фоновую задачу уведомлений
    asyncio.create_task(start_notification_scheduler())

    # Запускаем watchdog для Docker Healthcheck
    asyncio.create_task(watchdog_task())
    
    # Удаляем вебхук и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен и готов к работе!")


async def on_shutdown():
    """Выполняется при остановке бота."""
    logger.info("Бот останавливается...")
    await bot.session.close()


async def main():
    """Основная функция запуска бота."""
    try:
        # Устанавливаем обработчики startup/shutdown
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        
        # Запускаем polling
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    asyncio.run(main())
