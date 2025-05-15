from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

from app.db.session import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleResponse, RevenueResponse

router = APIRouter(
    prefix="/sales",
    tags=["sales"]
)

class IntervalType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

@router.get("/revenue", response_model=List[RevenueResponse])
def get_revenue_by_interval(
    interval: IntervalType = Query(..., description="Time interval for revenue aggregation"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        if interval == IntervalType.DAILY:
            start_date = end_date - timedelta(days=30)
        elif interval == IntervalType.WEEKLY:
            start_date = end_date - timedelta(weeks=12)
        elif interval == IntervalType.MONTHLY:
            start_date = end_date - timedelta(days=365)
        else:  # yearly
            start_date = end_date - timedelta(days=365*5)

    # Base query with date filter
    query = db.query(Sale).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    )

    # Group by interval
    if interval == IntervalType.DAILY:
        query = query.group_by(func.date(Sale.sale_date))
        date_format = "%Y-%m-%d"
    elif interval == IntervalType.WEEKLY:
        query = query.group_by(func.yearweek(Sale.sale_date))
        date_format = "%Y-%U"
    elif interval == IntervalType.MONTHLY:
        query = query.group_by(func.date_format(Sale.sale_date, "%Y-%m"))
        date_format = "%Y-%m"
    else:  # yearly
        query = query.group_by(func.year(Sale.sale_date))
        date_format = "%Y"

    # Calculate revenue
    revenue_data = query.with_entities(
        func.date_format(Sale.sale_date, date_format).label("interval"),
        func.sum(Sale.amount).label("revenue"),
        func.count(Sale.id).label("total_sales")
    ).all()

    return [
        RevenueResponse(
            interval=item.interval,
            revenue=item.revenue,
            total_sales=item.total_sales
        )
        for item in revenue_data
    ]

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