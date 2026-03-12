from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
import datetime

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True) # crypto, survival, etc.
    source = Column(String)
    url = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, unique=True, index=True)
    price_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class WhaleTransfer(Base):
    __tablename__ = "whales"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    symbol = Column(String)
    blockchain = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
