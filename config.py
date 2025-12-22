from os import getenv
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


# Загружаем .env
load_dotenv()

# === Основные токены и ключи ===
TELEGRAM_TOKEN: str = getenv("TG_BOT_TOKEN", "")

# === База данных ===
# Корень проекта
BASE_DIR = Path(__file__).resolve().parent
DB_URL_ENV = getenv("DB_URL")

if DB_URL_ENV and DB_URL_ENV.startswith("sqlite"):
    # Парсим путь из URL
    parsed = urlparse(DB_URL_ENV)
    db_path = Path(parsed.path.lstrip("/"))

    # Если путь относительный → делаем абсолютным от BASE_DIR
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path

    # Собираем абсолютный URL
    DB_URL = f"sqlite+aiosqlite:///{db_path.as_posix()}"
else:
    # Например, PostgreSQL или не указан .env
    DB_URL = DB_URL_ENV or f"sqlite+aiosqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"

# === Администратор ===
USER_ID_FOR_ADMIN: int = int(getenv("USER_ID_FOR_ADMIN", 0))
