from sqlalchemy import Column, Integer, String, JSON, DateTime, Float, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()
metadata = MetaData()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_message = Column(String)
    bot_response = Column(String)
    context_used = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    feedback_score = Column(Float, nullable=True)
    
class Memory(Base):
    __tablename__ = 'memories'
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    
class LearningPattern(Base):
    __tablename__ = 'learning_patterns'
    
    id = Column(Integer, primary_key=True)
    pattern_type = Column(String)
    pattern_data = Column(JSON)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
class MarketData(Base):
    __tablename__ = 'market_data'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    data_type = Column(String)  # price, volume, etc.
    value = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)  # yahoo_finance, etc.
    
class PortfolioOptimization(Base):
    __tablename__ = 'portfolio_optimizations'
    
    id = Column(Integer, primary_key=True)
    input_portfolio = Column(JSON)
    optimized_portfolio = Column(JSON)
    optimization_params = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    performance_metrics = Column(JSON)