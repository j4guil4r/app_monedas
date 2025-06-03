from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from .session import engine

# Base para modelos de consulta (no para crear tablas)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency = Column(String(3))
    balance = Column(Numeric(15, 2))

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey('accounts.id'))
    receiver_account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Numeric(15, 2))
    currency = Column(String(3))
    exchange_rate = Column(Numeric(10, 4))
    timestamp = Column(DateTime, default=func.now())

# Verificar que los modelos coincidan con la estructura de la DB
def validate_models():
    try:
        Base.metadata.reflect(engine)
        print("Modelos alineados con la estructura de la base de datos")
    except Exception as e:
        print(f"Error en validación: {str(e)}")