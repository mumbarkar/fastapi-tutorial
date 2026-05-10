from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (using SQLite for simplicity)
db_url = "postgresql://postgres:Nayan%40308@localhost:5432/mahesh"

# Database connection setup
engine = create_engine(db_url)

# Create a configured "Session" class
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

