"""
Configuração global para testes
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.coffee import Coffee
from app.models.order import Order, OrderItem


# Database de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override da dependência de database para testes"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db_session():
    """Fixture para sessão de database de teste"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Fixture para cliente de teste da API"""
    return TestClient(app)


@pytest.fixture(scope="function")
def sample_coffees(db_session):
    """Fixture com cafés de exemplo para testes"""
    coffees = [
        Coffee(
            id=11,
            name="Expresso",
            price=200,  # R$ 2,00 em centavos
            water_ml=50,
            milk_ml=0,
            coffee_grounds_g=15
        ),
        Coffee(
            id=12,
            name="Expresso Duplo",
            price=300,  # R$ 3,00 em centavos
            water_ml=100,
            milk_ml=0,
            coffee_grounds_g=30
        ),
        Coffee(
            id=13,
            name="Cappuccino",
            price=450,  # R$ 4,50 em centavos
            water_ml=30,
            milk_ml=120,
            coffee_grounds_g=15
        ),
        Coffee(
            id=14,
            name="Flat White",
            price=550,  # R$ 5,50 em centavos
            water_ml=30,
            milk_ml=150,
            coffee_grounds_g=15
        ),
        Coffee(
            id=15,
            name="Americano",
            price=350,  # R$ 3,50 em centavos
            water_ml=100,
            milk_ml=0,
            coffee_grounds_g=15
        )
    ]
    
    for coffee in coffees:
        db_session.add(coffee)
    db_session.commit()
    
    return coffees


@pytest.fixture(scope="function")
def sample_order(db_session, sample_coffees):
    """Fixture com pedido de exemplo para testes"""
    order = Order(
        id=1,
        total_price=650,  # R$ 6,50 em centavos
        status="pending"
    )
    db_session.add(order)
    db_session.flush()  # Para obter o ID do pedido
    
    # Adicionar itens ao pedido
    order_items = [
        OrderItem(
            order_id=order.id,
            coffee_id=11,  # Expresso
            quantity=2
        ),
        OrderItem(
            order_id=order.id,
            coffee_id=13,  # Cappuccino
            quantity=1
        )
    ]
    
    for item in order_items:
        db_session.add(item)
    
    db_session.commit()
    return order
