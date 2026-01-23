from pydantic import Field
from typing import Optional, Dict, Any
from datetime import datetime
from .base import BaseSchema

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