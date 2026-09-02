from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Transaction
from app.schemas import SummaryResponse, CategorySpending, TransactionResponse
from typing import List

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.get("/summary", response_model=SummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    income = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'income').scalar() or 0.0
    expenses = db.query(func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'expense').scalar() or 0.0
    
    return SummaryResponse(
        total_income=income,
        total_expenses=expenses,
        net_savings=income - expenses
    )

@router.get("/spending-by-category", response_model=List[CategorySpending])
def get_spending_by_category(db: Session = Depends(get_db)):
    results = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total_amount')
    ).filter(Transaction.transaction_type == 'expense').group_by(Transaction.category).all()
    
    return [CategorySpending(category=r.category, total_amount=r.total_amount) for r in results]

@router.get("/anomalies", response_model=List[TransactionResponse])
def get_anomalies(db: Session = Depends(get_db)):
    anomalies = db.query(Transaction).filter(Transaction.is_anomaly == True).all()
    return anomalies
