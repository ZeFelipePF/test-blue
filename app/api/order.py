from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderSummary
from app.services.order_service import create_order, get_pending_orders, get_consumption_analysis

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
async def create_new_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """
    Registra um novo pedido de café.
    
    Cria um pedido com os itens especificados e retorna as informações completas
    incluindo ID do pedido, data/hora, preço total e lista detalhada dos itens.
    
    **Request URL:**
    ```
    POST http://localhost:8000/orders/
    ```
    
    **Headers:**
    ```
    Content-Type: application/json
    accept: application/json
    ```
    
    **Request Body:**
    ```json
    {
        "items": [
            {
                "coffee_id": 11,
                "quantity": 2
            },
            {
                "coffee_id": 13,
                "quantity": 1
            }
        ]
    }
    ```
    
    **CURL Example:**
    ```bash
    curl -X POST "http://localhost:8000/orders/" \
      -H "Content-Type: application/json" \
      -H "accept: application/json" \
      -d '{
        "items": [
          {
            "coffee_id": 11,
            "quantity": 2
          },
          {
            "coffee_id": 13,
            "quantity": 1
          }
        ]
      }'
    ```
    
    **Response Example:**
    ```json
    {
        "id": 1,
        "created_at": "2025-09-18T17:39:33.186615",
        "total_price": 8.5,
        "status": "pending",
        "items": [
            {
                "id": 1,
                "coffee_id": 11,
                "quantity": 2,
                "coffee_name": "Expresso",
                "item_price": 4.0
            },
            {
                "id": 2,
                "coffee_id": 13,
                "quantity": 1,
                "coffee_name": "Cappuccino",
                "item_price": 4.5
            }
        ]
    }
    ```
    
    **Informações dos itens retornados:**
    - `id`: ID único do item
    - `coffee_id`: ID do café no menu
    - `quantity`: Quantidade pedida
    - `coffee_name`: Nome do café (ex: "Expresso", "Cappuccino")
    - `item_price`: Preço total do item (preço × quantidade)
    
    **IDs dos cafés disponíveis:**
    - 11: Expresso (R$ 2,00)
    - 12: Expresso Duplo (R$ 3,00)
    - 13: Cappuccino (R$ 4,50)
    - 14: Flat White (R$ 5,50)
    - 15: Americano (R$ 3,50)
    """
    try:
        return create_order(db, order_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/pending", response_model=List[OrderSummary])
async def get_pending_orders_endpoint(db: Session = Depends(get_db)):
    """
    Lista todos os pedidos pendentes com informações detalhadas dos itens.
    
    Retorna uma lista de todos os pedidos que ainda não foram processados,
    incluindo informações completas sobre cada item do pedido.
    
    **Request URL:**
    ```
    GET http://localhost:8000/orders/pending
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/orders/pending" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    [
        {
            "id": 1,
            "created_at": "2025-09-18T17:39:33.186615",
            "total_price": 8.5,
            "status": "pending",
            "items": [
                {
                    "id": 1,
                    "coffee_id": 11,
                    "quantity": 2,
                    "coffee_name": "Expresso",
                    "item_price": 4.0
                },
                {
                    "id": 2,
                    "coffee_id": 13,
                    "quantity": 1,
                    "coffee_name": "Cappuccino",
                    "item_price": 4.5
                }
            ]
        }
    ]
    ```
    
    **Informações dos itens:**
    - `id`: ID único do item
    - `coffee_id`: ID do café no menu
    - `quantity`: Quantidade pedida
    - `coffee_name`: Nome do café (ex: "Expresso", "Cappuccino")
    - `item_price`: Preço total do item (preço × quantidade)
    """
    return get_pending_orders(db)

@router.get("/consumption")
async def get_consumption_analysis_endpoint(
    days: int = Query(1, description="Número de dias para análise (padrão: 1)"),
    db: Session = Depends(get_db)
):
    """
    Análise de consumo de insumos para baristas.
    
    Informa o balanço de consumo de cafés, litros de água e leite, 
    e quantidade de café moído consumido, baseado na média dos últimos dias.
    
    Considera a média de consumo dos últimos dias e pode ser usado para 
    previsão de consumo futuro.
    
    **Request URL:**
    ```
    GET http://localhost:8000/orders/consumption?days={days}
    ```
    
    **Headers:**
    ```
    accept: application/json
    ```
    
    **Query Parameters:**
    - `days` (int, optional): Número de dias para calcular a média (padrão: 1)
    
    **CURL Example:**
    ```bash
    curl -X GET "http://localhost:8000/orders/consumption?days=7" \
      -H "accept: application/json"
    ```
    
    **Response Example:**
    ```json
    {
        "period_days": 7,
        "total_coffees": 45,
        "total_water_ml": 2250,
        "total_milk_ml": 1800,
        "total_coffee_grounds_g": 675,
        "daily_averages": {
            "coffees": 6.43,
            "water_ml": 321.43,
            "milk_ml": 257.14,
            "coffee_grounds_g": 96.43
        }
    }
    ```
    
    **Response Fields:**
    - `period_days`: Número de dias analisados
    - `total_coffees`: Total de cafés vendidos no período
    - `total_water_ml`: Total de água consumida (ml)
    - `total_milk_ml`: Total de leite consumido (ml)
    - `total_coffee_grounds_g`: Total de café moído consumido (g)
    - `daily_averages`: Médias diárias de consumo
    """
    return get_consumption_analysis(db, days)
