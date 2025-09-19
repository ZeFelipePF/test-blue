from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.coffee import Coffee
from app.schemas.order import OrderCreate
from typing import List

def create_order(db: Session, order_data: OrderCreate):
    """Cria um novo pedido"""
    # Calcular preço total
    total_price = 0
    order_items = []
    
    for item in order_data.items:
        coffee = db.query(Coffee).filter(Coffee.id == item.coffee_id).first()
        if not coffee:
            raise ValueError(f"Café com ID {item.coffee_id} não encontrado")
        
        item_price = (coffee.price * item.quantity) / 100  # Converte centavos para reais
        total_price += item_price
        
        order_items.append({
            "coffee_id": item.coffee_id,
            "quantity": item.quantity
        })
    
    # Criar pedido
    db_order = Order(total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Criar itens do pedido
    for item_data in order_items:
        order_item = OrderItem(
            order_id=db_order.id,
            coffee_id=item_data["coffee_id"],
            quantity=item_data["quantity"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    
    # Recarregar o pedido com os itens para garantir que os relacionamentos estejam carregados
    db_order = db.query(Order).filter(Order.id == db_order.id).first()
    return db_order

def get_pending_orders(db: Session):
    """Busca todos os pedidos pendentes com seus itens e informações do café"""
    from sqlalchemy.orm import joinedload
    return db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.coffee)
    ).filter(Order.status == 'pending').all()

def get_order_by_id(db: Session, order_id: int):
    """Busca um pedido por ID"""
    return db.query(Order).filter(Order.id == order_id).first()

def get_consumption_analysis(db: Session, days: int = 1):
    """Analisa o consumo de insumos baseado nos pedidos dos últimos dias"""
    from datetime import datetime, timedelta
    
    # Calcular data de início
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Buscar pedidos dos últimos dias
    orders = db.query(Order).filter(Order.created_at >= start_date).all()
    
    total_water = 0
    total_milk = 0
    total_coffee_grounds = 0
    total_coffees = 0
    
    for order in orders:
        for item in order.items:
            coffee = item.coffee
            quantity = item.quantity
            
            total_water += coffee.water_ml * quantity
            total_milk += coffee.milk_ml * quantity
            total_coffee_grounds += coffee.coffee_grounds_g * quantity
            total_coffees += quantity
    
    # Calcular médias
    avg_water_per_day = total_water / days if days > 0 else 0
    avg_milk_per_day = total_milk / days if days > 0 else 0
    avg_coffee_grounds_per_day = total_coffee_grounds / days if days > 0 else 0
    avg_coffees_per_day = total_coffees / days if days > 0 else 0
    
    return {
        "period_days": days,
        "total_coffees": total_coffees,
        "total_water_ml": total_water,
        "total_milk_ml": total_milk,
        "total_coffee_grounds_g": total_coffee_grounds,
        "daily_averages": {
            "coffees": avg_coffees_per_day,
            "water_ml": avg_water_per_day,
            "milk_ml": avg_milk_per_day,
            "coffee_grounds_g": avg_coffee_grounds_per_day
        }
    }
