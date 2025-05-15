from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import products, categories, inventory, sales

app = FastAPI(
    title="E-commerce Admin API",
    description="API for managing e-commerce products, inventory, and sales",
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

# Include routers
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(inventory.router)
app.include_router(sales.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to E-commerce Admin API"} 