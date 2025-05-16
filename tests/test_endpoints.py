from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_category(client):
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"}
    )
    return response.json()

@pytest.fixture
def test_product(client, test_category):
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "category_id": test_category["id"]
        }
    )
    return response.json()

# Product Endpoints Tests
def test_create_product(client, test_category):
    response = client.post(
        "/products/",
        json={
            "name": "New Product",
            "description": "New Description",
            "price": 149.99,
            "category_id": test_category["id"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price"] == 149.99
    assert data["category_id"] == test_category["id"]

def test_get_product(client, test_product):
    response = client.get(f"/products/{test_product['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_product["name"]
    assert data["price"] == test_product["price"]

def test_list_products(client, test_product):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(p["name"] == test_product["name"] for p in data)

# Inventory Endpoints Tests
def test_list_inventory(client, test_product):
    response = client.get("/inventory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(i["product_id"] == test_product["id"] for i in data)

def test_list_low_stock(client, test_product):
    # First update inventory to low stock
    client.patch(
        f"/inventory/{test_product['id']}",
        json={"quantity": 5, "low_stock_threshold": 10}
    )
    
    response = client.get("/inventory/low-stock")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(i["product_id"] == test_product["id"] for i in data)

def test_update_inventory(client, test_product):
    response = client.patch(
        f"/inventory/{test_product['id']}",
        json={"quantity": 50, "low_stock_threshold": 10}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 50
    assert data["low_stock_threshold"] == 10

# Sales Endpoints Tests
def test_list_sales(client, test_product):
    # Create a sale first
    sale_date = datetime.utcnow()
    response = client.post(
        "/sales/",
        json={
            "product_id": test_product["id"],
            "quantity": 2,
            "unit_price": 99.99,
            "total_amount": 199.98,
            "sale_date": sale_date.isoformat()
        }
    )
    assert response.status_code == 200
    
    # Test listing sales
    response = client.get("/sales/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(s["product_id"] == test_product["id"] for s in data)

def test_get_revenue_by_interval(client, test_product):
    # Create a sale first
    sale_date = datetime.utcnow()
    client.post(
        "/sales/",
        json={
            "product_id": test_product["id"],
            "quantity": 2,
            "unit_price": 99.99,
            "total_amount": 199.98,
            "sale_date": sale_date.isoformat()
        }
    )
    
    # Test revenue by interval
    response = client.get("/sales/revenue?interval=daily")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(r["revenue"] > 0 for r in data)

def test_compare_revenue(client, test_product):
    # Create sales in different periods
    current_date = datetime.utcnow()
    # Set current period to 1 day
    current_start = current_date - timedelta(days=1)
    current_end = current_date
    # Set previous period to 1 day before current period
    previous_start = current_start - timedelta(days=1)
    previous_end = current_start

    # Create current period sale
    client.post(
        "/sales/",
        json={
            "product_id": test_product["id"],
            "quantity": 2,
            "unit_price": 99.99,
            "total_amount": 199.98,
            "sale_date": current_end.isoformat()
        }
    )

    # Create previous period sale
    client.post(
        "/sales/",
        json={
            "product_id": test_product["id"],
            "quantity": 1,
            "unit_price": 99.99,
            "total_amount": 99.99,
            "sale_date": previous_end.isoformat()
        }
    )

    # Test revenue comparison
    response = client.get(
        f"/sales/compare?current_start={current_start.isoformat()}&current_end={current_end.isoformat()}&previous_start={previous_start.isoformat()}&previous_end={previous_end.isoformat()}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_period"]["revenue"] > 0
    assert data["previous_period"]["revenue"] > 0
    assert "percentage_change" in data 