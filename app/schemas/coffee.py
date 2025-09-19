from pydantic import BaseModel
from typing import Optional

class CoffeeBase(BaseModel):
    name: str
    price: int  # Preço em centavos
    water_ml: int
    milk_ml: int
    coffee_grounds_g: int

class CoffeeCreate(CoffeeBase):
    pass

class Coffee(CoffeeBase):
    id: int
    
    class Config:
        from_attributes = True

class CoffeeResponse(BaseModel):
    id: int
    name: str
    price: float  # Preço em reais para exibição
    water_ml: int
    milk_ml: int
    coffee_grounds_g: int
    
    class Config:
        from_attributes = True
