from os import getenv
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


# Load .env
load_dotenv()

# === Main tokens and keys ===
TELEGRAM_TOKEN: str = getenv("TG_BOT_TOKEN", "")

# === Database ===
# Project root
BASE_DIR = Path(__file__).resolve().parent
DB_URL_ENV = getenv("DB_URL")

if DB_URL_ENV and DB_URL_ENV.startswith("sqlite"):
    # Parse path from URL
    parsed = urlparse(DB_URL_ENV)
    db_path = Path(parsed.path.lstrip("/"))

    # If the path is relative → make it absolute from BASE_DIR
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path

    # Assemble the absolute URL
    DB_URL = f"sqlite+aiosqlite:///{db_path.as_posix()}"
else:
    # For example, PostgreSQL or not specified in .env
    DB_URL = DB_URL_ENV or f"sqlite+aiosqlite:///{(BASE_DIR / 'db.sqlite3').as_posix()}"

# === Administrator ===
USER_ID_FOR_ADMIN: int = int(getenv("USER_ID_FOR_ADMIN", 0))
