from sqlalchemy import Column, Integer, String, Float, Date
from datetime import date
from app.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    total_amount = Column(Float)
    date = Column(Date, default=date.today)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
