from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the SQLite database
DATABASE_URL = "sqlite:///./lab_inventory.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Define the Item model
class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, default=0)
    location = Column(String)
    min_quantity = Column(Integer, default=1)  # Default minimum quantity

# Create the database tables
Base.metadata.create_all(bind=engine)
