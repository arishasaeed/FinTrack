from fastapi import FastAPI
from app.database import engine, Base
from app.routers import transactions, analytics

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinTrack API",
    description="Personal Finance Analytics API",
    version="1.0.0"
)

# Include routers
app.include_router(transactions.router)
app.include_router(analytics.router)

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Enable CORS (if needed during local testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve the frontend on the root
app.mount("/", StaticFiles(directory="static", html=True), name="static")
