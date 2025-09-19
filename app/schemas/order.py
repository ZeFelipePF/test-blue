from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    coffee_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    coffee_id: int
    quantity: int
    coffee_name: str = None
    item_price: float = None
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    created_at: datetime
    total_price: float
    status: str
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True

class OrderSummary(BaseModel):
    id: int
    created_at: datetime
    total_price: float
    status: str
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True
