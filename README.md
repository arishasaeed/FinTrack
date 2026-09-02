# FinTrack — Personal Finance Analytics API

A full-stack personal finance analytics platform built with **Python, FastAPI, SQLAlchemy, Pandas, and Docker**. Users upload CSV bank statements and the system automatically categorizes transactions, tracks income vs expenses, detects spending anomalies, and displays everything on a beautiful dark-themed dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- **CSV Upload & Processing** — Upload raw bank export files and the system processes them instantly using `pandas`
- **Auto-Categorization** — Transactions are automatically categorized (groceries, dining, utilities, entertainment, etc.) using keyword matching
- **Income vs Expense Tracking** — Get a clear summary of total income, total expenses, and net savings
- **Anomaly Detection** — Flags unusual transactions that are significantly above normal spending thresholds
- **Spending by Category** — Aggregated spending data per category, ready for chart visualization
- **Interactive Dashboard** — Beautiful Glassmorphism dark-themed frontend with Chart.js doughnut charts
- **REST API** — 5 clean, documented API endpoints with auto-generated Swagger UI
- **Docker Ready** — Fully containerized for easy deployment

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Data Processing | Pandas |
| Frontend | Vanilla HTML, CSS, JavaScript, Chart.js |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |

---

## Project Structure

```
FinTrack/
├── app/
│   ├── main.py                # FastAPI entry point, serves frontend
│   ├── database.py            # SQLAlchemy DB connection setup
│   ├── models.py              # ORM models (Transaction table)
│   ├── schemas.py             # Pydantic validation schemas
│   ├── routers/
│   │   ├── transactions.py    # Upload & retrieve transactions
│   │   └── analytics.py      # Summary, categories & anomaly endpoints
│   └── services/
│       └── processor.py      # CSV parsing & categorization logic
├── static/
│   ├── index.html             # Dashboard UI
│   ├── styles.css             # Dark Glassmorphism styles
│   └── script.js              # API integration & Chart.js charts
├── tests/
│   └── test_main.py           # Pytest unit tests
├── sample_transactions_full.csv  # Sample data to test the app
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Getting Started

### Option 1: Run with Python (Recommended for beginners)

**Prerequisites:** Python 3.9+

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/FinTrack.git
cd FinTrack

# 2. Create & activate a virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python -m uvicorn app.main:app --reload
```

Open your browser at **http://127.0.0.1:8000**

### Option 2: Run with Docker

**Prerequisites:** Docker Desktop

```bash
docker-compose up --build
```

Open your browser at **http://localhost:8000**

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/transactions/upload` | Upload a CSV file of transactions |
| `GET` | `/transactions/` | Retrieve all transactions (filter by category) |
| `GET` | `/analytics/summary` | Get total income, expenses & net savings |
| `GET` | `/analytics/spending-by-category` | Spending totals grouped by category |
| `GET` | `/analytics/anomalies` | List flagged unusual transactions |

📖 Full interactive API docs available at **http://127.0.0.1:8000/docs**

---

## Sample CSV Format

Your CSV file must have these three columns:

```csv
Date,Description,Amount
2026-08-01,Company Payroll Deposit,5500.00
2026-08-02,Walmart Supercenter,-125.50
2026-08-05,McDonalds Drive Thru,-12.75
```

> Positive amounts = income, Negative amounts = expenses

A sample file `sample_transactions_full.csv` is included in the repo.

---

## Running Tests

```bash
pytest tests/
```

---

## License

This project is licensed under the MIT License.
