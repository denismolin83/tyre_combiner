from sqlalchemy import JSON, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RawProduct(Base):
    __tablename__ = "raw_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str] = mapped_column(String(100), index=True)
    source: Mapped[str] = mapped_column(String(50), default="robotyre")

    name: Mapped[str] = mapped_column(String(500))
    vendor: Mapped[str] = mapped_column(String(100), index=True)
    price: Mapped[float] = mapped_column(Float)

    raw_params: Mapped[dict] = mapped_column(JSON, nullable=True)

    width: Mapped[int] = mapped_column(Integer, nullable=True)
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    diametr: Mapped[str] = mapped_column(String(10), nullable=True)
