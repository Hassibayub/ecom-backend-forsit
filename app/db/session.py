import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Get database connection parameters from environment variables
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "password123")
DB_HOST = os.getenv("MYSQL_HOST", "db")
DB_NAME = os.getenv("MYSQL_DATABASE", "ecommerce_admin")

# Use the DATABASE_URL environment variable if set, otherwise build it from components
DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

print(f"Using database URL: {DATABASE_URL.replace(DB_PASSWORD, '********')}")


engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,  
    pool_pre_ping=True, 
    connect_args={
        "connect_timeout": 30,  # Longer timeout for initial connection
        "use_pure": True 
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 