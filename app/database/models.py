from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AnalyseHistorique(Base):
    __tablename__ = "analyse_historique"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    rsi = Column(Float)
    macd = Column(Float)
    variation_30d = Column(Float)
    score_ai = Column(Float)
    prediction = Column(String)
