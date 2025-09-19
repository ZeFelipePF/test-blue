from sqlalchemy.orm import Session
from app.models.coffee import Coffee
from app.schemas.coffee import CoffeeCreate

def get_all_coffees(db: Session):
    """Busca todos os cafés do menu"""
    return db.query(Coffee).all()

def get_coffee_by_id(db: Session, coffee_id: int):
    """Busca um café por ID"""
    return db.query(Coffee).filter(Coffee.id == coffee_id).first()

def create_coffee(db: Session, coffee: CoffeeCreate):
    """Cria um novo café no menu"""
    db_coffee = Coffee(**coffee.model_dump())
    db.add(db_coffee)
    db.commit()
    db.refresh(db_coffee)
    return db_coffee

def get_menu_with_prices(db: Session):
    """Retorna o menu com preços formatados em reais"""
    coffees = db.query(Coffee).all()
    menu = []
    for coffee in coffees:
        menu.append({
            "id": coffee.id,
            "name": coffee.name,
            "price": coffee.price / 100,  # Converte centavos para reais
            "water_ml": coffee.water_ml,
            "milk_ml": coffee.milk_ml,
            "coffee_grounds_g": coffee.coffee_grounds_g
        })
    return menu
