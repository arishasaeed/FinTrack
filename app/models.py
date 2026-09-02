from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from .database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    description = Column(String, index=True)
    amount = Column(Float)
    transaction_type = Column(String) # 'income' or 'expense'
    category = Column(String, index=True)
    is_anomaly = Column(Boolean, default=False)
