# serializers/item_serializer.py
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Float, FLOAT


class ItemSerializer(BaseModel):
    name: Optional[str] =None
    description: Optional[str] = None
    price: Optional[float] =None

    class Config:
        from_attributes = True

class ItemResponse(BaseModel):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]

class AllItemsResponse(BaseModel):
    Items: List[ItemResponse]