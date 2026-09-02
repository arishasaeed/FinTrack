import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Transaction
import io

# Simple categorization rules based on keywords
CATEGORY_RULES = {
    'groceries': ['walmart', 'kroger', 'safeway', 'whole foods', 'trader joe'],
    'dining': ['restaurant', 'mcdonalds', 'starbucks', 'uber eats', 'doordash', 'chipotle'],
    'utilities': ['electric', 'water', 'gas', 'internet', 'comcast', 'verizon'],
    'entertainment': ['netflix', 'spotify', 'hulu', 'amc', 'steam'],
    'transportation': ['uber', 'lyft', 'gas station', 'shell', 'chevron', 'transit'],
    'housing': ['rent', 'mortgage'],
    'income': ['payroll', 'salary', 'deposit', 'dividend'],
}

def categorize_transaction(description: str) -> str:
    desc_lower = description.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in desc_lower for keyword in keywords):
            return category
    return 'other'

def process_csv_and_store(db: Session, file_contents: bytes):
    # Read CSV using pandas
    df = pd.read_csv(io.BytesIO(file_contents))
    
    # Expected columns: Date, Description, Amount
    # We will derive transaction_type and category
    
    transactions_to_add = []
    
    # Calculate simple stats for anomaly detection (e.g., standard deviation by category)
    # For a real app, this would query historical data from the DB.
    # Here we just use a basic threshold for demonstration.
    ANOMALY_THRESHOLD = 1000.0 
    
    for _, row in df.iterrows():
        try:
            # Parse date assuming standard format, fallback to today if parsing fails
            date_obj = pd.to_datetime(row['Date']).date()
        except:
            date_obj = datetime.now().date()
            
        description = str(row['Description'])
        amount = float(row['Amount'])
        
        # Determine type based on amount
        transaction_type = 'income' if amount >= 0 else 'expense'
        abs_amount = abs(amount)
        
        # Categorize
        category = categorize_transaction(description)
        
        # Simple anomaly detection
        is_anomaly = abs_amount > ANOMALY_THRESHOLD
        
        db_transaction = Transaction(
            date=date_obj,
            description=description,
            amount=abs_amount,
            transaction_type=transaction_type,
            category=category,
            is_anomaly=is_anomaly
        )
        transactions_to_add.append(db_transaction)
        
    # Bulk save to DB
    db.add_all(transactions_to_add)
    db.commit()
    
    return len(transactions_to_add)
