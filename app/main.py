import os
import time
import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine, get_db
from app.routers import categories, inventory, products, sales

load_dotenv()

app = FastAPI(
    title="E-commerce Admin API",
    description="Backend API for E-commerce Admin Dashboard",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    # Get database connection parameters from environment variables
    db_host = os.getenv("MYSQL_HOST", "db")
    db_user = os.getenv("MYSQL_USER", "root")
    db_password = os.getenv("MYSQL_PASSWORD", "password123")
    db_name = os.getenv("MYSQL_DATABASE", "ecommerce_admin")
    
    print(f"Connecting to database: {db_host}/{db_name} as user {db_user}")
    
    # Attempt to connect multiple times with a delay (useful for container startup)
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Create tables in the database
            print(f"Attempt {attempt + 1}/{max_retries} to create tables")
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully")
            return
        except Exception as e:
            print(f"Error during database initialization (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not initialize database.")
                raise e

# Include routers
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(inventory.router)
app.include_router(sales.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce Admin API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "environment": {
            "debug": DEBUG,
            "host": API_HOST,
            "port": API_PORT
        }
    } 