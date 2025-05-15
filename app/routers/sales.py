from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleResponse

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

@router.get("/", response_model=List[SaleResponse])
def list_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    product_id: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Sale)
    
    # Apply filters
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if min_amount:
        query = query.filter(Sale.amount >= min_amount)
    if max_amount:
        query = query.filter(Sale.amount <= max_amount)
    
    # Apply pagination
    sales = query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales 