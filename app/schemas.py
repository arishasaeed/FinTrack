from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class TransactionBase(BaseModel):
    date: date
    description: str
    amount: float
    transaction_type: str
    category: str

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    is_anomaly: bool

    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float

class CategorySpending(BaseModel):
    category: str
    total_amount: float
