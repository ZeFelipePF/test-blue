from sqlalchemy import Integer, Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_price = Column(Float, nullable=False)  # Preço total em reais
    status = Column(String, default='pending', nullable=False)  # pending, completed
    
    # Relacionamento com itens do pedido
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, total_price={self.total_price}, status='{self.status}')>"

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    coffee_id = Column(Integer, ForeignKey('coffees.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    
    # Relacionamentos
    order = relationship("Order", back_populates="items")
    coffee = relationship("Coffee")
    
    @property
    def coffee_name(self):
        """Retorna o nome do café"""
        return self.coffee.name if self.coffee else None
    
    @property
    def item_price(self):
        """Calcula o preço total do item (preço do café * quantidade)"""
        if self.coffee:
            return (self.coffee.price * self.quantity) / 100  # Converte centavos para reais
        return 0.0
    
    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, coffee_id={self.coffee_id}, quantity={self.quantity})>"
