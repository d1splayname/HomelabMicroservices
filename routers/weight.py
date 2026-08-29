from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

import os
from urllib.parse import quote_plus

load_dotenv()

_DB_HOST = os.getenv("DB_HOST")
_DB_PORT = os.getenv("DB_PORT")
_DB_USERNAME = os.getenv("DB_USER")
_DB_PASSWORD = os.getenv("DB_PASS")
_WEIGHT_DB_DATABASE = os.getenv("LOG_DB_DATABASE")

_DATABASE_URL = (
    "mariadb+mariadbconnector://"
    f"{quote_plus(_DB_USERNAME)}:{quote_plus(_DB_PASSWORD)}@"
    f"{_DB_HOST}:{_DB_PORT}/{_WEIGHT_DB_DATABASE}"
)

weightEngine = create_engine(
    _DATABASE_URL,
    pool_pre_ping=True,  # check connection is still alive before use
    pool_size=10,  # up to 10 idle/open connections
    max_overflow=20,  # 20 extra connections during spikes
)

SessionLocal = sessionmaker(
    bind=weightEngine,
    autoflush=False,
    expire_on_commit=False,
)

class WeightBase(DeclarativeBase):
    pass

def WeightGetDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()