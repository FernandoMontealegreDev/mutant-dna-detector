from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database connection configuration for MySQL
DB_USER = os.getenv("DB_USER")  # Database username
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Database password
DB_HOST = os.getenv("DB_HOST")  # Database host address
DB_PORT = os.getenv("DB_PORT")  # Database port number
DB_NAME = os.getenv("DB_NAME")  # Database name

# Form the SQLAlchemy connection URL
SQLALCHEMY_DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a SQLAlchemy engine for connecting to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,              # Maximum number of connections in the pool
    max_overflow=10,          # Additional connections allowed beyond the pool size
    pool_timeout=30,          # Time (in seconds) to wait for a connection from the pool
    pool_recycle=1800,        # Recycle connections every 1800 seconds to prevent timeout issues
    echo=False                # Set to True to log all SQL queries for debugging
)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declaring database models
Base = declarative_base()

def get_db():
    """
    Dependency function for retrieving a new database session.
    
    This function is typically used with FastAPI to manage database sessions 
    within request scopes. It yields a database session object and ensures the 
    connection is closed after the request is complete.
    
    Yields:
        db (Session): A SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure that the session is closed after usage