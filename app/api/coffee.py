from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.coffee import CoffeeResponse
from app.services.coffee_service import get_all_coffees, get_menu_with_prices

router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=List[dict])
async def get_menu(db: Session = Depends(get_db)):
    """
    Lista o menu com todos os cafés e seus respectivos preços.
    
    Retorna uma lista com todos os cafés disponíveis, incluindo:
    - Nome do café
    - Preço em reais
    - Quantidade de ingredientes necessários
    
    **Request URL:**
    ```
    GET http://localhost:8000/menu/
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/menu/" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    [
      {
        "id": 11,
        "name": "Expresso",
        "price": 2.0,
        "water_ml": 50,
        "milk_ml": 0,
        "coffee_grounds_g": 15
      }
    ]
    ```
    """
    return get_menu_with_prices(db)

@router.get("/all", response_model=List[CoffeeResponse])
async def get_all_coffees_endpoint(db: Session = Depends(get_db)):
    """
    Lista todos os cafés (endpoint administrativo).
    
    Retorna todos os cafés com preços em centavos para uso administrativo
    e integração com sistemas de pagamento.
    
    **Request URL:**
    ```
    GET http://localhost:8000/menu/all
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/menu/all" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    [
      {
        "id": 11,
        "name": "Expresso",
        "price": 200,
        "water_ml": 50,
        "milk_ml": 0,
        "coffee_grounds_g": 15
      }
    ]
    ```
    
    **Note:** Preços retornados em centavos (200 = R$ 2,00)
    """
    return get_all_coffees(db)
