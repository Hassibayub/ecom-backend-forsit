from app.db.session import engine
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale
from app.models.inventory import Inventory
from app.db.session import Base

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!") 