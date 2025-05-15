from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum

from app.db.session import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleResponse, RevenueResponse, ComparisonResponse, SaleCreate

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
    if not end_date:
        end_date = datetime.now()
    if not start_date:
        if interval == IntervalType.DAILY:
            start_date = end_date - timedelta(days=30)
        elif interval == IntervalType.WEEKLY:
            start_date = end_date - timedelta(weeks=12)
        elif interval == IntervalType.MONTHLY:
            start_date = end_date - timedelta(days=365)
        else:
            start_date = end_date - timedelta(days=365*5)

    query = db.query(Sale).filter(
        Sale.sale_date >= start_date,
        Sale.sale_date <= end_date
    )

    dialect = db.bind.dialect.name
    if interval == IntervalType.DAILY:
        group_expr = func.date(Sale.sale_date)
        if dialect == "sqlite":
            label_expr = func.strftime("%Y-%m-%d", Sale.sale_date)
        else:
            label_expr = func.date_format(Sale.sale_date, "%Y-%m-%d")
    elif interval == IntervalType.WEEKLY:
        if dialect == "sqlite":
            group_expr = func.strftime("%Y-%W", Sale.sale_date)
            label_expr = func.strftime("%Y-%W", Sale.sale_date)
        else:
            group_expr = func.yearweek(Sale.sale_date)
            label_expr = func.date_format(Sale.sale_date, "%Y-%U")
    elif interval == IntervalType.MONTHLY:
        if dialect == "sqlite":
            group_expr = func.strftime("%Y-%m", Sale.sale_date)
            label_expr = func.strftime("%Y-%m", Sale.sale_date)
        else:
            group_expr = func.date_format(Sale.sale_date, "%Y-%m")
            label_expr = func.date_format(Sale.sale_date, "%Y-%m")
    else:
        if dialect == "sqlite":
            group_expr = func.strftime("%Y", Sale.sale_date)
            label_expr = func.strftime("%Y", Sale.sale_date)
        else:
            group_expr = func.year(Sale.sale_date)
            label_expr = func.date_format(Sale.sale_date, "%Y")

    query = query.group_by(group_expr)
    revenue_data = query.with_entities(
        label_expr.label("interval"),
        func.sum(Sale.total_amount).label("revenue"),
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
        query = query.filter(Sale.total_amount >= min_amount)
    if max_amount:
        query = query.filter(Sale.total_amount <= max_amount)
    
    # Apply pagination
    sales = query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales

@router.get("/compare", response_model=ComparisonResponse)
def compare_revenue(
    current_start: datetime = Query(..., description="Start date of current period"),
    current_end: datetime = Query(..., description="End date of current period"),
    previous_start: Optional[datetime] = None,
    previous_end: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # Calculate previous period if not provided
    if not previous_start or not previous_end:
        period_days = (current_end - current_start).days
        previous_end = current_start - timedelta(days=1)
        previous_start = previous_end - timedelta(days=period_days)

    # Get current period revenue
    current_revenue = db.query(func.sum(Sale.total_amount)).filter(
        Sale.sale_date >= current_start,
        Sale.sale_date <= current_end
    ).scalar() or 0

    # Get previous period revenue
    previous_revenue = db.query(func.sum(Sale.total_amount)).filter(
        Sale.sale_date >= previous_start,
        Sale.sale_date <= previous_end
    ).scalar() or 0

    # Calculate percentage change
    if previous_revenue == 0:
        percentage_change = 100 if current_revenue > 0 else 0
    else:
        percentage_change = ((current_revenue - previous_revenue) / previous_revenue) * 100

    return ComparisonResponse(
        current_period={
            "start_date": current_start,
            "end_date": current_end,
            "revenue": current_revenue
        },
        previous_period={
            "start_date": previous_start,
            "end_date": previous_end,
            "revenue": previous_revenue
        },
        percentage_change=percentage_change
    )

@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale 