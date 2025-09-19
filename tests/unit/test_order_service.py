"""
Testes unitários para o serviço de pedidos
"""
import pytest
from datetime import datetime, timedelta
from app.services.order_service import (
    create_order, 
    get_pending_orders, 
    get_consumption_analysis
)
from app.schemas.order import OrderCreate, OrderItemCreate
from app.models.order import Order, OrderItem


class TestOrderService:
    """Testes para o serviço de pedidos"""
    
    def test_create_order_success(self, db_session, sample_coffees):
        """Testa criação de pedido com sucesso"""
        order_data = OrderCreate(
            items=[
                OrderItemCreate(coffee_id=11, quantity=2),  # Expresso
                OrderItemCreate(coffee_id=13, quantity=1)   # Cappuccino
            ]
        )
        
        order = create_order(db_session, order_data)
        
        assert order is not None
        assert order.id is not None
        assert order.status == "pending"
        assert order.total_price == 850  # (2 * 200) + (1 * 450) = 850 centavos
        assert len(order.items) == 2
        
        # Verificar itens do pedido
        item_1 = order.items[0]
        assert item_1.coffee_id == 11
        assert item_1.quantity == 2
        assert item_1.coffee_name == "Expresso"
        assert item_1.item_price == 4.0  # 2 * 2.00
        
        item_2 = order.items[1]
        assert item_2.coffee_id == 13
        assert item_2.quantity == 1
        assert item_2.coffee_name == "Cappuccino"
        assert item_2.item_price == 4.5  # 1 * 4.50
    
    def test_create_order_invalid_coffee_id(self, db_session, sample_coffees):
        """Testa criação de pedido com ID de café inválido"""
        order_data = OrderCreate(
            items=[
                OrderItemCreate(coffee_id=999, quantity=1)  # ID inexistente
            ]
        )
        
        with pytest.raises(ValueError, match="Café com ID 999 não encontrado"):
            create_order(db_session, order_data)
    
    def test_create_order_empty_items(self, db_session, sample_coffees):
        """Testa criação de pedido com lista vazia de itens"""
        order_data = OrderCreate(items=[])
        
        order = create_order(db_session, order_data)
        
        assert order is not None
        assert order.total_price == 0
        assert len(order.items) == 0
    
    def test_get_pending_orders_success(self, db_session, sample_coffees):
        """Testa busca de pedidos pendentes com sucesso"""
        # Criar pedidos de teste
        order1 = Order(total_price=400, status="pending")
        order2 = Order(total_price=600, status="pending")
        order3 = Order(total_price=300, status="completed")  # Não deve aparecer
        
        db_session.add_all([order1, order2, order3])
        db_session.flush()
        
        # Adicionar itens aos pedidos
        item1 = OrderItem(order_id=order1.id, coffee_id=11, quantity=2)
        item2 = OrderItem(order_id=order2.id, coffee_id=13, quantity=1)
        
        db_session.add_all([item1, item2])
        db_session.commit()
        
        pending_orders = get_pending_orders(db_session)
        
        assert len(pending_orders) == 2
        assert all(order.status == "pending" for order in pending_orders)
        
        # Verificar se os pedidos corretos foram retornados
        order_ids = [order.id for order in pending_orders]
        assert order1.id in order_ids
        assert order2.id in order_ids
        assert order3.id not in order_ids
    
    def test_get_pending_orders_empty(self, db_session):
        """Testa busca de pedidos pendentes quando não há pedidos"""
        pending_orders = get_pending_orders(db_session)
        assert len(pending_orders) == 0
        assert pending_orders == []
    
    def test_get_consumption_analysis_success(self, db_session, sample_coffees):
        """Testa análise de consumo com sucesso"""
        # Criar pedidos de teste com datas diferentes
        now = datetime.utcnow()
        
        # Pedido de hoje
        order1 = Order(
            total_price=400, 
            status="completed",
            created_at=now
        )
        
        # Pedido de ontem
        order2 = Order(
            total_price=600, 
            status="completed",
            created_at=now - timedelta(days=1)
        )
        
        # Pedido de 3 dias atrás (não deve ser considerado)
        order3 = Order(
            total_price=300, 
            status="completed",
            created_at=now - timedelta(days=3)
        )
        
        db_session.add_all([order1, order2, order3])
        db_session.flush()
        
        # Adicionar itens aos pedidos
        items = [
            OrderItem(order_id=order1.id, coffee_id=11, quantity=2),  # Expresso
            OrderItem(order_id=order2.id, coffee_id=13, quantity=1),  # Cappuccino
            OrderItem(order_id=order3.id, coffee_id=15, quantity=1),  # Americano
        ]
        
        db_session.add_all(items)
        db_session.commit()
        
        # Testar análise de consumo para 1 dia
        analysis = get_consumption_analysis(db_session, days=1)
        
        assert analysis is not None
        assert "total_coffees" in analysis
        assert "total_water_ml" in analysis
        assert "total_milk_ml" in analysis
        assert "total_coffee_grounds_g" in analysis
        assert "average_daily_consumption" in analysis
        assert "projected_consumption" in analysis
        
        # Verificar se os valores estão corretos
        assert analysis["total_coffees"] == 3  # 2 Expresso + 1 Cappuccino
        assert analysis["total_water_ml"] == 130  # (2 * 50) + (1 * 30)
        assert analysis["total_milk_ml"] == 120  # (2 * 0) + (1 * 120)
        assert analysis["total_coffee_grounds_g"] == 45  # (2 * 15) + (1 * 15)
    
    def test_get_consumption_analysis_no_orders(self, db_session, sample_coffees):
        """Testa análise de consumo quando não há pedidos"""
        analysis = get_consumption_analysis(db_session, days=1)
        
        assert analysis is not None
        assert analysis["total_coffees"] == 0
        assert analysis["total_water_ml"] == 0
        assert analysis["total_milk_ml"] == 0
        assert analysis["total_coffee_grounds_g"] == 0
        assert analysis["average_daily_consumption"] == 0
        assert analysis["projected_consumption"] == 0
    
    def test_get_consumption_analysis_different_days(self, db_session, sample_coffees):
        """Testa análise de consumo com diferentes períodos"""
        # Criar pedido de teste
        order = Order(
            total_price=400, 
            status="completed",
            created_at=datetime.utcnow()
        )
        
        db_session.add(order)
        db_session.flush()
        
        item = OrderItem(order_id=order.id, coffee_id=11, quantity=1)
        db_session.add(item)
        db_session.commit()
        
        # Testar com 1 dia
        analysis_1_day = get_consumption_analysis(db_session, days=1)
        assert analysis_1_day["projected_consumption"]["total_coffees"] == 1
        
        # Testar com 7 dias
        analysis_7_days = get_consumption_analysis(db_session, days=7)
        assert analysis_7_days["projected_consumption"]["total_coffees"] == 7

