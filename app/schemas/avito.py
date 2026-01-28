from pydantic import BaseModel, Field
from typing import Optional


class AvitoExcelItem(BaseModel):
    """Схема для элемента из Excel от Avito"""

    id: str = Field(alias="Уникальный идентификатор объявления")
    name: str = Field(alias="Название объявления")
    brand: Optional[str] = Field(None, alias="Производитель")
    price: float = Field(alias="Цена")
    stock: str = Field(alias="Количество")
    description: Optional[str] = Field(None, alias="Описание объявления")
