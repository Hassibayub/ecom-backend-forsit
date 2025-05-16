from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryResponse, InventoryUpdate

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

@router.patch("/{product_id}", response_model=InventoryResponse)
def update_inventory(
    product_id: int,
    inventory_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    # Get the inventory item
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(
            status_code=404,
            detail=f"Inventory for product id {product_id} not found"
        )
    
    # Update the inventory
    update_data = inventory_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inventory, field, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

@router.get("/low-stock", response_model=List[InventoryResponse])
def list_low_stock(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    low_stock_items = (
        db.query(Inventory)
        .filter(Inventory.quantity <= Inventory.low_stock_threshold)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return low_stock_items

@router.get("/", response_model=List[InventoryResponse])
def list_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    inventory = (
        db.query(Inventory)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return inventory 