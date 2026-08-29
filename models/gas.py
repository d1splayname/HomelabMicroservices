from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text

from routers.gas import GasBase

class Gas(GasBase):
    __tablename__ = "gas"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        nullable=False
    )

    timestamp: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP()")
    )