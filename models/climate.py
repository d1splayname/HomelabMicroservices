from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, text, Float

from routers.climate import ClimateBase

class Climate(ClimateBase):
    __tablename__ = "climate"

    type: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
        nullable=False
    )

    data: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    timestamp: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP()")
    )