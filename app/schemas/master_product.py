from typing import Optional, List
from datetime import datetime
from .base import BaseSchema
from .product_image import ProductImageSchema

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