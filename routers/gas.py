from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from urllib.parse import quote_plus

import os

load_dotenv()

_DB_HOST = os.getenv("DB_HOST")
_DB_PORT = os.getenv("DB_PORT")
_DB_USERNAME = os.getenv("DB_USER")
_DB_PASSWORD = os.getenv("DB_PASS")
_GAS_DB_DATABASE = os.getenv("LOG_DB_DATABASE")

_DATABASE_URL = (
    "mariadb+mariadbconnector://"
    f"{quote_plus(_DB_USERNAME)}:{quote_plus(_DB_PASSWORD)}@"
    f"{_DB_HOST}:{_DB_PORT}/{_GAS_DB_DATABASE}"
)

gasEngine = create_engine(
    _DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker (
    bind=gasEngine,
    autoflush=False,
    expire_on_commit=False,
)

class GasBase(DeclarativeBase):
    pass

def GasGetDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()