from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# Определяем модель Customers
class Customers(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Для удобства можно добавить отношение к трафику
    traffic_records = relationship('Traffic', back_populates='customer')

# Определяем модель Traffic
class Traffic(Base):
    __tablename__ = 'traffic'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    ip = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    received_traffic = Column(Float, nullable=False)

    # Связываем с моделью Customers
    customer = relationship('Customers', back_populates='traffic_records')

