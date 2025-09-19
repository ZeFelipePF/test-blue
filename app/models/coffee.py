from sqlalchemy import Integer, Column, String
from app.database import Base

class Coffee(Base):
    __tablename__ = 'coffees'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Integer, index=True, nullable=False)  # Preço em centavos
    water_ml = Column(Integer, nullable=False)
    milk_ml = Column(Integer, nullable=False)
    coffee_grounds_g = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Coffee(name='{self.name}', price={self.price})>"
