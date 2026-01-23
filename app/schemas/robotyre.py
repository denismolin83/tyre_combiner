from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List

class RobotyreXMLItem(BaseModel):
    """Схема для элемента из XML от Robotyre"""
    id: str
    name: str
    vendor: Optional[str] = None
    price: float
    count: int
    picture: List[HttpUrl] = Field(default_factory=list)
    params: Dict[str, str] = Field(default_factory=dict)