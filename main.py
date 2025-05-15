from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import products, inventory, sales

# Load environment variables
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

# Include routers
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
