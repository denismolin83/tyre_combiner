import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey, JSON, Integer, String, Boolean, Float, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MasterProduct(Base):
    """Эталонный товар для витин МП"""

    __tablename__ = "master_products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    brand: Mapped[str] = mapped_column(String(100), index=True) # бренд товара
    model: Mapped[str] = mapped_column(String(255), index=True) # модель товара
    width: Mapped[Optional[int]] = mapped_column() # 205
    height: Mapped[Optional[int]] = mapped_column() # 55
    diameter: Mapped[Optional[str]] = mapped_column(String(10)) # 16
    season: Mapped[Optional[str]] = mapped_column(String(20)) # летняя, зимняя, всесезонная
    is_spaiked: Mapped[Optional[bool]] = mapped_column(Boolean, default=False) # шипованная

    full_name: Mapped[Optional[str]] = mapped_column(String(500)) # полное наименование товара
    description: Mapped[Optional[str]] = mapped_column(String()) # описание товара

    is_manual_edited: Mapped[bool] = mapped_column(Boolean, default=False, index=True) # признак ручного редактирования

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), 
                                                          onupdate=func.now())

    raw_items: Mapped[List["RawProduct"]] = relationship("RawProduct", back_populates="master_product")
    images: Mapped[List["ProductImage"]] = relationship("ProductImage", back_populates="master_product")


class RawProduct(Base):
    __tablename__ = "raw_products"
    __table_args__ = (
        # Уникальный индекс по source и external_id для предотвращения дубликатов
        UniqueConstraint('source', 'external_id', name='_source_external_id_uc'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(50), index=True)  # источник данных
    external_id: Mapped[str] = mapped_column(String(100), index=True)  # внешний идентификатор товара

    name: Mapped[Optional[str]] = mapped_column(String(500))  # наименование товара
    vendor: Mapped[Optional[str]] = mapped_column(String(100), index=True)  # производитель товара
    price: Mapped[float] = mapped_column(Float, default=0.0)  # цена товара

    stock: Mapped[int] = mapped_column(Integer, default=0) # остаток

    raw_data: Mapped[dict] = mapped_column(JSON, default=dict) # параметры

    master_id: Mapped[Optional[int]] = mapped_column(ForeignKey("master_products.id"), index=True)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(),
                                                          onupdate=func.now())
    master_product: Mapped["MasterProduct"] = relationship("MasterProduct", back_populates="raw_items")

    


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    master_id: Mapped[Optional[int]] = mapped_column(ForeignKey("master_products.id"), index=True)

    source: Mapped[str] = mapped_column(String(50), index=True)  # источник данных
    original_url: Mapped[str] = mapped_column(String(500))  # оригинальный URL изображения
    s3_key: Mapped[Optional[str]] = mapped_column(String(500))  # ключ в S3

    file_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True)  # хеш файла изображения
    status: Mapped[str] = mapped_column(String(20), default="pending")  # статус обработки изображения
    is_main: Mapped[bool] = mapped_column(Boolean, default=False)  # признак основного изображения

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(),
                                                          onupdate=func.now())
    
    master_product: Mapped["MasterProduct"] = relationship("MasterProduct", back_populates="images")