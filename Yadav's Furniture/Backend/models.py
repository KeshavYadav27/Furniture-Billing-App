from database import Base, engine
from sqlalchemy import (Boolean, Column, Float, ForeignKey, Integer, Numeric,
                        String)
from sqlalchemy.orm import relationship


def create_tables():
    Base.metadata.create_all(engine)
    
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    contact_number = Column(String)
    address = Column(String)
    description = Column(String)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    name = Column(String)
    size = Column(String)
    quantity = Column(Integer)
    price_per_piece = Column(Float)

class Bill(Base):
    __tablename__ = "bills"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    bill = Column(String)
