from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime

# Глобальные настройки Pydantic
class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


# Изображения
class ProductImageSchema(BaseSchema):
    id: Optional[int] = None
    source: str
    original_url: str
    s3_key: Optional[str] = None
    status: str = "pending"
    is_main: bool = False


# Сырые Данные (RawProduct)
class RawProductBase(BaseSchema):
    source: str
    external_id: str
    name: str
    vendor: Optional[str] = None
    price: float = 0.0
    stock: int = 0
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class RawProductCreate(RawProductBase):
    """Схема для создания сырого продукта"""
    pass


class RawProductRead(RawProductBase):
    """Схема для чтения сырого продукта"""
    id: int
    master_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


# Мастер Продукт (MasterProduct)
class MasterProductBase(BaseSchema):
    brand: str
    model: str
    width: Optional[int] = None
    height: Optional[int] = None
    diameter: Optional[str] = None
    season: Optional[str] = None
    is_spaiked: bool = False
    full_name: str
    description: Optional[str] = None
    is_manual_edited: bool = False


class MasterProductCreate(MasterProductBase):
    """Схема для создания мастер продукта"""
    pass


class MasterProductRead(MasterProductBase):
    """Схема для чтения мастер продукта"""
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[ProductImageSchema] = []


class RobotyreXMLItem(BaseModel):
    """Схема для элемента из XML от Robotyre"""
    id: str
    name: str
    vendor: Optional[str] = None
    price: float
    count: int
    picture: List[HttpUrl] = Field(default_factory=list)
    params: Dict[str, str] = Field(default_factory=dict)