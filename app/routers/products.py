from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )
    return product

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {product.category_id} not found"
        )

    # Create new product
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id
    )
    db.add(db_product)
    db.flush()  # Flush to get the product ID
    
    # Create initial inventory record
    db_inventory = Inventory(
        product_id=db_product.id,
        quantity=0,
        low_stock_threshold=10
    )
    db.add(db_inventory)
    
    # Commit both product and inventory
    db.commit()
    db.refresh(db_product)
    
    return db_product 