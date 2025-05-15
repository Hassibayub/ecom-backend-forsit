# E-commerce Admin API

A FastAPI-based backend for managing an e-commerce platform's admin operations, including product management, inventory tracking, and sales analytics.

## Features

- Product Management (CRUD operations)
- Inventory Management with low stock alerts
- Sales Tracking and Revenue Analytics
- Category Management
- RESTful API with OpenAPI documentation

## Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- MySQL
- Pydantic
- pytest (Testing)
- Faker (Data Generation)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce-admin-api
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database Schema

### Models

#### Product
- id: int (PK)
- name: str
- description: str
- price: float
- category_id: int (FK)
- created_at: datetime
- updated_at: datetime

#### Category
- id: int (PK)
- name: str
- description: str
- created_at: datetime
- updated_at: datetime

#### Inventory
- id: int (PK)
- product_id: int (FK)
- quantity: int
- low_stock_threshold: int
- created_at: datetime
- updated_at: datetime

#### Sale
- id: int (PK)
- product_id: int (FK)
- quantity: int
- unit_price: float
- total_amount: float
- sale_date: datetime
- created_at: datetime
- updated_at: datetime

## API Endpoints

### Products
- `POST /products/` - Create new product
- `GET /products/` - List all products
- `GET /products/{product_id}` - Get product details

### Categories
- `POST /categories/` - Create new category
- `GET /categories/` - List all categories
- `GET /categories/{category_id}` - Get category details

### Inventory
- `GET /inventory/` - List all inventory items
- `GET /inventory/low-stock` - List items below threshold
- `PATCH /inventory/{product_id}` - Update stock levels

### Sales
- `GET /sales/` - List sales with filters
- `GET /sales/revenue` - Get revenue by interval
- `GET /sales/compare` - Compare revenue between periods

## Seed Data

To populate the database with sample data:

```bash
python seed_data.py
```

This will create:
- 5 sample categories
- 20 sample products with inventory
- 50 sample sales records

## Testing

Run tests with:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run linting:
```bash
flake8 app tests
```

3. Run type checking:
```bash
mypy app
```