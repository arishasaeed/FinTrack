from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Transaction
from app.schemas import TransactionResponse
from app.services.processor import process_csv_and_store

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.post("/upload")
async def upload_transactions_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    try:
        num_added = process_csv_and_store(db, contents)
        return {"message": f"Successfully processed and added {num_added} transactions."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(skip: int = 0, limit: int = 100, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if category:
        query = query.filter(Transaction.category == category)
    transactions = query.offset(skip).limit(limit).all()
    return transactions
