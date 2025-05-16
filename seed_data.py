import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.sale import Sale

fake = Faker()

def create_sample_categories(db: Session, num_categories: int = 5):
    """Create sample categories."""
    categories = []
    for _ in range(num_categories):
        category = Category(
            name=fake.word().capitalize(),
            description=fake.sentence()
        )
        db.add(category)
        categories.append(category)
    db.commit()
    return categories

def create_sample_products(db: Session, categories: list[Category], num_products: int = 20):
    """Create sample products with inventory."""
    products = []
    for _ in range(num_products):
        product = Product(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10.0, 1000.0), 2),
            category_id=random.choice(categories).id
        )
        db.add(product)
        db.flush()  # Flush to get the product ID
        
        # Create inventory for the product
        inventory = Inventory(
            product_id=product.id,
            quantity=random.randint(0, 100),
            low_stock_threshold=random.randint(5, 20)
        )
        db.add(inventory)
        products.append(product)
    db.commit()
    return products

def create_sample_sales(db: Session, products: list[Product], num_sales: int = 50):
    """Create sample sales records."""
    sales = []
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    for _ in range(num_sales):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product.price
        total_amount = round(quantity * unit_price, 2)
        sale_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        
        sale = Sale(
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            sale_date=sale_date
        )
        db.add(sale)
        sales.append(sale)
    db.commit()
    return sales

def seed_database():
    """Main function to seed the database with sample data."""
    db = SessionLocal()
    try:
        print("Creating sample categories...")
        categories = create_sample_categories(db)
        print(f"Created {len(categories)} categories")
        
        print("\nCreating sample products with inventory...")
        products = create_sample_products(db, categories)
        print(f"Created {len(products)} products with inventory")
        
        print("\nCreating sample sales records...")
        sales = create_sample_sales(db, products)
        print(f"Created {len(sales)} sales records")
        
        print("\nDatabase seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
