from typing import Optional
from .base import BaseSchema

# Изображения
class ProductImageSchema(BaseSchema):
    id: Optional[int] = None
    source: str
    original_url: str
    s3_key: Optional[str] = None
    status: str = "pending"
    is_main: bool = False