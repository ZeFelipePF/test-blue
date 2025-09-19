"""
Testes de integração para endpoints de pedidos
"""
import pytest
from fastapi.testclient import TestClient


class TestOrderEndpoints:
    """Testes para endpoints de pedidos"""
    
    def test_create_order_success(self, client, sample_coffees):
        """Testa criação de pedido com sucesso"""
        order_data = {
            "items": [
                {"coffee_id": 11, "quantity": 2},  # Expresso
                {"coffee_id": 13, "quantity": 1}   # Cappuccino
            ]
        }
        
        response = client.post("/orders/", json=order_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estrutura da resposta
        assert "id" in data
        assert "created_at" in data
        assert "total_price" in data
        assert "status" in data
        assert "items" in data
        
        # Verificar valores
        assert data["status"] == "pending"
        assert data["total_price"] == 8.5  # (2 * 2.00) + (1 * 4.50)
        assert len(data["items"]) == 2
        
        # Verificar itens do pedido
        item_1 = data["items"][0]
        assert item_1["coffee_id"] == 11
        assert item_1["quantity"] == 2
        assert item_1["coffee_name"] == "Expresso"
        assert item_1["item_price"] == 4.0
        
        item_2 = data["items"][1]
        assert item_2["coffee_id"] == 13
        assert item_2["quantity"] == 1
        assert item_2["coffee_name"] == "Cappuccino"
        assert item_2["item_price"] == 4.5
    
    def test_create_order_invalid_coffee_id(self, client, sample_coffees):
        """Testa criação de pedido com ID de café inválido"""
        order_data = {
            "items": [
                {"coffee_id": 999, "quantity": 1}  # ID inexistente
            ]
        }
        
        response = client.post("/orders/", json=order_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Café com ID 999 não encontrado" in data["detail"]
    
    def test_create_order_empty_items(self, client, sample_coffees):
        """Testa criação de pedido com lista vazia de itens"""
        order_data = {"items": []}
        
        response = client.post("/orders/", json=order_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_price"] == 0.0
        assert data["status"] == "pending"
        assert len(data["items"]) == 0
    
    def test_create_order_missing_quantity(self, client, sample_coffees):
        """Testa criação de pedido sem campo quantity"""
        order_data = {
            "items": [
                {"coffee_id": 11}  # Falta quantity
            ]
        }
        
        response = client.post("/orders/", json=order_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_create_order_invalid_quantity(self, client, sample_coffees):
        """Testa criação de pedido com quantidade inválida"""
        order_data = {
            "items": [
                {"coffee_id": 11, "quantity": 0}  # Quantidade zero
            ]
        }
        
        response = client.post("/orders/", json=order_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
    
    def test_get_pending_orders_success(self, client, sample_coffees, sample_order):
        """Testa busca de pedidos pendentes com sucesso"""
        response = client.get("/orders/pending")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 1
        
        order = data[0]
        assert "id" in order
        assert "created_at" in order
        assert "total_price" in order
        assert "status" in order
        assert "items" in order
        
        assert order["status"] == "pending"
        assert order["total_price"] == 6.5  # (2 * 2.00) + (1 * 4.50)
        assert len(order["items"]) == 2
        
        # Verificar itens do pedido
        for item in order["items"]:
            assert "id" in item
            assert "coffee_id" in item
            assert "quantity" in item
            assert "coffee_name" in item
            assert "item_price" in item
    
    def test_get_pending_orders_empty(self, client, sample_coffees):
        """Testa busca de pedidos pendentes quando não há pedidos"""
        response = client.get("/orders/pending")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_get_consumption_analysis_success(self, client, sample_coffees, sample_order):
        """Testa análise de consumo com sucesso"""
        response = client.get("/orders/consumption?days=1")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar estrutura da resposta
        assert "total_coffees" in data
        assert "total_water_ml" in data
        assert "total_milk_ml" in data
        assert "total_coffee_grounds_g" in data
        assert "average_daily_consumption" in data
        assert "projected_consumption" in data
        
        # Verificar se os valores são números
        assert isinstance(data["total_coffees"], int)
        assert isinstance(data["total_water_ml"], int)
        assert isinstance(data["total_milk_ml"], int)
        assert isinstance(data["total_coffee_grounds_g"], int)
        
        # Verificar estrutura do consumo médio
        avg_consumption = data["average_daily_consumption"]
        assert "total_coffees" in avg_consumption
        assert "total_water_ml" in avg_consumption
        assert "total_milk_ml" in avg_consumption
        assert "total_coffee_grounds_g" in avg_consumption
        
        # Verificar estrutura do consumo projetado
        projected = data["projected_consumption"]
        assert "total_coffees" in projected
        assert "total_water_ml" in projected
        assert "total_milk_ml" in projected
        assert "total_coffee_grounds_g" in projected
    
    def test_get_consumption_analysis_different_days(self, client, sample_coffees, sample_order):
        """Testa análise de consumo com diferentes períodos"""
        # Testar com 1 dia
        response_1 = client.get("/orders/consumption?days=1")
        assert response_1.status_code == 200
        
        # Testar com 7 dias
        response_7 = client.get("/orders/consumption?days=7")
        assert response_7.status_code == 200
        
        # Testar com 30 dias
        response_30 = client.get("/orders/consumption?days=30")
        assert response_30.status_code == 200
        
        # Verificar se as respostas têm a mesma estrutura
        data_1 = response_1.json()
        data_7 = response_7.json()
        data_30 = response_30.json()
        
        for data in [data_1, data_7, data_30]:
            assert "total_coffees" in data
            assert "projected_consumption" in data
    
    def test_get_consumption_analysis_invalid_days(self, client, sample_coffees):
        """Testa análise de consumo com parâmetro inválido"""
        # Testar com valor negativo
        response = client.get("/orders/consumption?days=-1")
        assert response.status_code == 422
        
        # Testar com valor zero
        response = client.get("/orders/consumption?days=0")
        assert response.status_code == 422
        
        # Testar sem parâmetro
        response = client.get("/orders/consumption")
        assert response.status_code == 422
    
    def test_get_consumption_analysis_empty_database(self, client, sample_coffees):
        """Testa análise de consumo com database vazio"""
        response = client.get("/orders/consumption?days=1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_coffees"] == 0
        assert data["total_water_ml"] == 0
        assert data["total_milk_ml"] == 0
        assert data["total_coffee_grounds_g"] == 0
        assert data["average_daily_consumption"]["total_coffees"] == 0
        assert data["projected_consumption"]["total_coffees"] == 0
    
    def test_order_endpoints_consistency(self, client, sample_coffees):
        """Testa consistência entre endpoints de pedidos"""
        # Criar um pedido
        order_data = {
            "items": [
                {"coffee_id": 11, "quantity": 1}
            ]
        }
        
        create_response = client.post("/orders/", json=order_data)
        assert create_response.status_code == 200
        created_order = create_response.json()
        
        # Buscar pedidos pendentes
        pending_response = client.get("/orders/pending")
        assert pending_response.status_code == 200
        pending_orders = pending_response.json()
        
        # Verificar se o pedido criado está na lista de pendentes
        assert len(pending_orders) == 1
        assert pending_orders[0]["id"] == created_order["id"]
        assert pending_orders[0]["total_price"] == created_order["total_price"]
        assert pending_orders[0]["status"] == created_order["status"]

