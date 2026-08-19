from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import os
from urllib.parse import quote_plus


def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.is_file():
        return

    for line in dotenv_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue

        value = value.strip().strip('"').strip("'")
        os.environ[key] = value


_load_dotenv(Path(__file__).resolve().parent / ".env")


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value or value.strip().lower() == "none":
        raise RuntimeError(
            f"Environment variable {name} is required and must be set to a valid value."
        )
    return value


_DB_HOST = _require_env("DB_HOST")
_DB_PORT = _require_env("DB_PORT")
_DB_USERNAME = _require_env("DB_USER")
_DB_PASSWORD = _require_env("DB_PASS")
_AUTH_DB_DATABASE = _require_env("AUTH_DB_DATABASE")

if not _DB_PORT.isdigit():
    raise RuntimeError(
        f"Environment variable DB_PORT must be a number, got {_DB_PORT!r}."
    )

_DATABASE_URL = (
    "mariadb+mariadbconnector://"
    f"{quote_plus(_DB_USERNAME)}:{quote_plus(_DB_PASSWORD)}@"
    f"{_DB_HOST}:{_DB_PORT}/{_AUTH_DB_DATABASE}"
)

authEngine = create_engine(
    _DATABASE_URL,
    pool_pre_ping=True,  # check connection is still alive before use
    pool_size=10,  # up to 10 idle/open connections
    max_overflow=20,  # 20 extra connections during spikes
)

SessionLocal = sessionmaker(
    bind=authEngine,
    autoflush=False,
    expire_on_commit=False,
)

class UserBase(DeclarativeBase):
    pass

def AuthGetDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()