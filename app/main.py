import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine
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
    try:
        # Extract database name from DATABASE_URL
        db_url = os.getenv("DATABASE_URL")
        db_name = db_url.split("/")[-1]
        print("Database url: ", db_url)
        print("Database name: ", db_name)
        
        # Create connection without database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password123"
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists")
        
        cursor.close()
        conn.close()
        
        # Now create tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error during database initialization: {e}")
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