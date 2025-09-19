"""
Testes unitários para o serviço de café
"""
import pytest
from unittest.mock import Mock, patch
from app.services.coffee_service import get_all_coffees, get_menu_with_prices
from app.models.coffee import Coffee


class TestCoffeeService:
    """Testes para o serviço de café"""
    
    def test_get_all_coffees_success(self, db_session, sample_coffees):
        """Testa busca de todos os cafés com sucesso"""
        coffees = get_all_coffees(db_session)
        
        assert len(coffees) == 5
        assert all(isinstance(coffee, Coffee) for coffee in coffees)
        
        # Verificar se os cafés estão corretos
        coffee_names = [coffee.name for coffee in coffees]
        assert "Expresso" in coffee_names
        assert "Cappuccino" in coffee_names
        assert "Americano" in coffee_names
    
    def test_get_all_coffees_empty_database(self, db_session):
        """Testa busca de cafés em database vazio"""
        coffees = get_all_coffees(db_session)
        assert len(coffees) == 0
        assert coffees == []
    
    def test_get_menu_with_prices_success(self, db_session, sample_coffees):
        """Testa busca do menu com preços formatados"""
        menu = get_menu_with_prices(db_session)
        
        assert len(menu) == 5
        assert all(isinstance(item, dict) for item in menu)
        
        # Verificar estrutura dos itens do menu
        for item in menu:
            assert "id" in item
            assert "name" in item
            assert "price" in item
            assert "water_ml" in item
            assert "milk_ml" in item
            assert "coffee_grounds_g" in item
            
            # Verificar se o preço está em reais (não centavos)
            assert isinstance(item["price"], float)
            assert item["price"] > 0
        
        # Verificar preços específicos
        expresso = next(item for item in menu if item["name"] == "Expresso")
        assert expresso["price"] == 2.0  # R$ 2,00
        
        cappuccino = next(item for item in menu if item["name"] == "Cappuccino")
        assert cappuccino["price"] == 4.5  # R$ 4,50
    
    def test_get_menu_with_prices_empty_database(self, db_session):
        """Testa busca do menu em database vazio"""
        menu = get_menu_with_prices(db_session)
        assert len(menu) == 0
        assert menu == []
    
    def test_get_menu_with_prices_conversion(self, db_session, sample_coffees):
        """Testa conversão correta de centavos para reais"""
        menu = get_menu_with_prices(db_session)
        
        # Verificar conversões específicas
        expresso = next(item for item in menu if item["name"] == "Expresso")
        assert expresso["price"] == 2.0  # 200 centavos = R$ 2,00
        
        expresso_duplo = next(item for item in menu if item["name"] == "Expresso Duplo")
        assert expresso_duplo["price"] == 3.0  # 300 centavos = R$ 3,00
        
        cappuccino = next(item for item in menu if item["name"] == "Cappuccino")
        assert cappuccino["price"] == 4.5  # 450 centavos = R$ 4,50
        
        flat_white = next(item for item in menu if item["name"] == "Flat White")
        assert flat_white["price"] == 5.5  # 550 centavos = R$ 5,50
        
        americano = next(item for item in menu if item["name"] == "Americano")
        assert americano["price"] == 3.5  # 350 centavos = R$ 3,50


