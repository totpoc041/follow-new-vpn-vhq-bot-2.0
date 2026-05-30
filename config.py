import os
from pathlib import Path
from urllib.parse import urlsplit

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Environment variable {name} is required")
    return value


def _parse_int(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    return int(raw)


def _parse_admin_ids() -> tuple[int, ...]:
    raw = _require_env("ADMIN_IDS")
    ids = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            ids.append(int(item))
    if not ids:
        raise ValueError("ADMIN_IDS must contain at least one Telegram ID")
    return tuple(ids)


def _derive_root_url(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}"


_load_dotenv(ENV_PATH)


def is_admin(user_id: int) -> bool:
    if user_id in BotConfig.ADMIN_IDS:
        return True

    import database as db

    return user_id in db.get_admins()


class BotConfig:
    """Конфигурация Telegram бота."""

    TOKEN = _require_env("TELEGRAM_BOT_TOKEN")
    ADMIN_IDS = _parse_admin_ids()
    ADMIN_PAYMENTS = ADMIN_IDS[0]


class HiddifyConfig:
    """Конфигурация Hiddify API и сервера."""

    API_BASE_URL = _require_env("HIDDIFY_API_BASE_URL").rstrip("/")
    API_KEY = _require_env("HIDDIFY_API_KEY")
    API_KEY_HEADER = os.getenv("HIDDIFY_API_KEY_HEADER", "Hiddify-API-Key").strip() or "Hiddify-API-Key"
    API_KEY_PREFIX = os.getenv("HIDDIFY_API_KEY_PREFIX", "").strip()
    SUB_FALLBACK_TEMPLATE = os.getenv("HIDDIFY_SUB_FALLBACK_TEMPLATE", "").strip()

    @classmethod
    def get_api_url(cls) -> str:
        return cls.API_BASE_URL

    @classmethod
    def get_api_headers(cls) -> dict[str, str]:
        api_key_value = cls.API_KEY
        if cls.API_KEY_PREFIX:
            api_key_value = f"{cls.API_KEY_PREFIX} {api_key_value}".strip()
        return {
            "Accept": "application/json",
            cls.API_KEY_HEADER: api_key_value,
        }

    @classmethod
    def get_user_link(cls, uuid: str) -> str:
        if cls.SUB_FALLBACK_TEMPLATE:
            return cls.SUB_FALLBACK_TEMPLATE.format(uuid=uuid)
        return f"{_derive_root_url(cls.API_BASE_URL)}/{uuid}/"

    @classmethod
    def get_proxy_stats_url(cls) -> str:
        return f"{cls.API_BASE_URL}/proxy-stats/api"


class AppConfig:
    """Общие настройки приложения."""

    DATABASE_PATH = os.getenv("DATABASE_PATH", "users.db").strip() or "users.db"
    BRAND_TAG = os.getenv("BRAND_TAG", "hiddify-bot").strip() or "hiddify-bot"
    BANK_DETAILS = os.getenv(
        "BANK_DETAILS",
        "Переведите оплату администратору и отправьте чек для подтверждения."
    ).strip()
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "Europe/Moscow").strip() or "Europe/Moscow"
    DAILY_CHECK_HOUR = _parse_int("DAILY_CHECK_HOUR", 16)
    DAILY_CHECK_MINUTE = _parse_int("DAILY_CHECK_MINUTE", 20)


class TariffConfig:
    """Тарифные планы."""

    DEFAULT_PACKAGE_DAYS = _parse_int("DEFAULT_PACKAGE_DAYS", 30)
    DEFAULT_USAGE_LIMIT_GB = _parse_int("DEFAULT_USAGE_LIMIT_GB", 130)

    TARIFFS = {
        "30day": {
            "package_days": DEFAULT_PACKAGE_DAYS,
            "usage_limit_GB": DEFAULT_USAGE_LIMIT_GB,
            "price": 111,
            "emoji": "🤏",
        },
        "60day": {"package_days": 60, "usage_limit_GB": 370, "price": 222, "emoji": "👍"},
        "90day": {"package_days": 90, "usage_limit_GB": 690, "price": 333, "emoji": "🤘"},
    }
