"""
Testes de integração para endpoints de café
"""
import pytest
from fastapi.testclient import TestClient


class TestCoffeeEndpoints:
    """Testes para endpoints de café"""
    
    def test_get_menu_success(self, client, sample_coffees):
        """Testa endpoint GET /menu/ com sucesso"""
        response = client.get("/menu/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 5
        
        # Verificar estrutura dos itens
        for item in data:
            assert "id" in item
            assert "name" in item
            assert "price" in item
            assert "water_ml" in item
            assert "milk_ml" in item
            assert "coffee_grounds_g" in item
            
            # Verificar se o preço está em reais
            assert isinstance(item["price"], float)
            assert item["price"] > 0
        
        # Verificar se todos os cafés estão presentes
        coffee_names = [item["name"] for item in data]
        assert "Expresso" in coffee_names
        assert "Expresso Duplo" in coffee_names
        assert "Cappuccino" in coffee_names
        assert "Flat White" in coffee_names
        assert "Americano" in coffee_names
    
    def test_get_menu_empty_database(self, client):
        """Testa endpoint GET /menu/ com database vazio"""
        response = client.get("/menu/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_get_all_coffees_success(self, client, sample_coffees):
        """Testa endpoint GET /menu/all com sucesso"""
        response = client.get("/menu/all")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 5
        
        # Verificar estrutura dos itens
        for item in data:
            assert "id" in item
            assert "name" in item
            assert "price" in item
            assert "water_ml" in item
            assert "milk_ml" in item
            assert "coffee_grounds_g" in item
            
            # Verificar se o preço está em centavos
            assert isinstance(item["price"], int)
            assert item["price"] > 0
        
        # Verificar preços específicos em centavos
        expresso = next(item for item in data if item["name"] == "Expresso")
        assert expresso["price"] == 200  # R$ 2,00 em centavos
        
        cappuccino = next(item for item in data if item["name"] == "Cappuccino")
        assert cappuccino["price"] == 450  # R$ 4,50 em centavos
    
    def test_get_all_coffees_empty_database(self, client):
        """Testa endpoint GET /menu/all com database vazio"""
        response = client.get("/menu/all")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    def test_menu_endpoints_consistency(self, client, sample_coffees):
        """Testa consistência entre endpoints /menu/ e /menu/all"""
        # Buscar dados de ambos os endpoints
        menu_response = client.get("/menu/")
        all_response = client.get("/menu/all")
        
        assert menu_response.status_code == 200
        assert all_response.status_code == 200
        
        menu_data = menu_response.json()
        all_data = all_response.json()
        
        # Verificar se têm o mesmo número de itens
        assert len(menu_data) == len(all_data)
        
        # Verificar se os IDs e nomes são consistentes
        for menu_item in menu_data:
            all_item = next(
                item for item in all_data 
                if item["id"] == menu_item["id"]
            )
            
            assert menu_item["id"] == all_item["id"]
            assert menu_item["name"] == all_item["name"]
            assert menu_item["water_ml"] == all_item["water_ml"]
            assert menu_item["milk_ml"] == all_item["milk_ml"]
            assert menu_item["coffee_grounds_g"] == all_item["coffee_grounds_g"]
            
            # Verificar conversão de preço
            assert menu_item["price"] == all_item["price"] / 100
    
    def test_menu_response_format(self, client, sample_coffees):
        """Testa formato da resposta do endpoint /menu/"""
        response = client.get("/menu/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar se é uma lista
        assert isinstance(data, list)
        
        # Verificar estrutura de cada item
        for item in data:
            assert isinstance(item, dict)
            
            # Verificar tipos dos campos
            assert isinstance(item["id"], int)
            assert isinstance(item["name"], str)
            assert isinstance(item["price"], float)
            assert isinstance(item["water_ml"], int)
            assert isinstance(item["milk_ml"], int)
            assert isinstance(item["coffee_grounds_g"], int)
            
            # Verificar se os valores são positivos
            assert item["id"] > 0
            assert item["name"] != ""
            assert item["price"] > 0
            assert item["water_ml"] >= 0
            assert item["milk_ml"] >= 0
            assert item["coffee_grounds_g"] > 0


