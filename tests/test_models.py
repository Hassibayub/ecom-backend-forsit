import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.sale import Sale

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_product(db_session):
    # Create a category first
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    # Create a product
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        category_id=category.id
    )
    db_session.add(product)
    db_session.commit()
    
    # Verify product was created
    saved_product = db_session.query(Product).filter(Product.id == product.id).first()
    assert saved_product is not None
    assert saved_product.name == "Test Product"
    assert saved_product.price == 99.99
    assert saved_product.category_id == category.id

def test_create_inventory(db_session):
    # Create a category and product first
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        category_id=category.id
    )
    db_session.add(product)
    db_session.commit()
    
    # Create inventory
    inventory = Inventory(
        product_id=product.id,
        quantity=100,
        low_stock_threshold=10
    )
    db_session.add(inventory)
    db_session.commit()
    
    # Verify inventory was created
    saved_inventory = db_session.query(Inventory).filter(Inventory.product_id == product.id).first()
    assert saved_inventory is not None
    assert saved_inventory.quantity == 100
    assert saved_inventory.low_stock_threshold == 10

def test_create_sale(db_session):
    # Create a category and product first
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        category_id=category.id
    )
    db_session.add(product)
    db_session.commit()
    
    # Create a sale
    sale = Sale(
        product_id=product.id,
        quantity=2,
        unit_price=99.99,
        total_amount=199.98,
        sale_date=datetime.utcnow()
    )
    db_session.add(sale)
    db_session.commit()
    
    # Verify sale was created
    saved_sale = db_session.query(Sale).filter(Sale.id == sale.id).first()
    assert saved_sale is not None
    assert saved_sale.product_id == product.id
    assert saved_sale.quantity == 2
    assert saved_sale.unit_price == 99.99
    assert saved_sale.total_amount == 199.98

def test_product_category_relationship(db_session):
    # Create a category
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    # Create multiple products in the same category
    product1 = Product(
        name="Test Product 1",
        description="Test Description 1",
        price=99.99,
        category_id=category.id
    )
    product2 = Product(
        name="Test Product 2",
        description="Test Description 2",
        price=149.99,
        category_id=category.id
    )
    db_session.add_all([product1, product2])
    db_session.commit()
    
    # Verify relationship
    category_products = db_session.query(Product).filter(Product.category_id == category.id).all()
    assert len(category_products) == 2
    assert any(p.name == "Test Product 1" for p in category_products)
    assert any(p.name == "Test Product 2" for p in category_products)

def test_product_inventory_relationship(db_session):
    # Create a category and product
    category = Category(name="Test Category", description="Test Description")
    db_session.add(category)
    db_session.commit()
    
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        category_id=category.id
    )
    db_session.add(product)
    db_session.commit()
    
    # Create inventory
    inventory = Inventory(
        product_id=product.id,
        quantity=100,
        low_stock_threshold=10
    )
    db_session.add(inventory)
    db_session.commit()
    
    # Verify relationship
    product_inventory = db_session.query(Inventory).filter(Inventory.product_id == product.id).first()
    assert product_inventory is not None
    assert product_inventory.quantity == 100
    assert product_inventory.product_id == product.id 