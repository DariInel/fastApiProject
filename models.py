from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, index=True)
    sum = Column(Integer, index=True, unique=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.now, server_default=func.now())



class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    surname = Column(String, index=True, unique=True)
    number = Column(String, index=True, unique=True)
    purchases = relationship('Purchase', backref='buyer')

'''
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True, unique=True)
    count = Column(Integer, index=True, unique=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
'''