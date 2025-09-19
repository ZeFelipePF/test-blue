import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import create_tables, get_db
from app.models.coffee import Coffee

# Dados do menu conforme especificação
menu_data = [
    {
        "name": "Expresso",
        "price": 200,  # R$2,00 em centavos
        "water_ml": 50,
        "milk_ml": 0,
        "coffee_grounds_g": 15
    },
    {
        "name": "Expresso Duplo", 
        "price": 300,  # R$3,00 em centavos
        "water_ml": 100,
        "milk_ml": 0,
        "coffee_grounds_g": 30
    },
    {
        "name": "Cappuccino",
        "price": 450,  # R$4,50 em centavos
        "water_ml": 30,
        "milk_ml": 120,
        "coffee_grounds_g": 15
    },
    {
        "name": "Flat White",
        "price": 550,  # R$5,50 em centavos
        "water_ml": 30,
        "milk_ml": 150,
        "coffee_grounds_g": 15
    },
    {
        "name": "Americano",
        "price": 350,  # R$3,50 em centavos
        "water_ml": 100,
        "milk_ml": 0,
        "coffee_grounds_g": 15
    }
]

def populate_menu():
    """Popula o banco com os dados do menu"""
    print("Criando tabelas...")
    create_tables()
    
    print("Conectando ao banco...")
    db = next(get_db())
    
    try:
        # Limpar dados existentes (opcional)
        print("Limpando dados existentes...")
        db.query(Coffee).delete()
        db.commit()
        
        # Inserir novos dados
        print("Inserindo dados do menu...")
        for item in menu_data:
            coffee = Coffee(**item)
            db.add(coffee)
            print(f"Adicionado: {item['name']} - R${item['price']/100:.2f}")
        
        db.commit()
        print("✅ Menu populado com sucesso!")
        
        # Verificar dados inseridos
        print("\n📋 Menu atual:")
        coffees = db.query(Coffee).all()
        for coffee in coffees:
            print(f"- {coffee.name}: R${coffee.price/100:.2f} | Água: {coffee.water_ml}ml | Leite: {coffee.milk_ml}ml | Café: {coffee.coffee_grounds_g}g")
            
    except Exception as e:
        print(f"❌ Erro ao popular menu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_menu()
