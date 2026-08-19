from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean

from routers.auth import UserBase

class User(UserBase):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    username: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    reset_password: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    recipe_access: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    last_login: Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )