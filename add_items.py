from sqlalchemy.orm import Session
from models import Item, SessionLocal

# Function to add items to the database
def add_item(name: str, quantity: int, location: str):
    # Get a database session
    db = SessionLocal()
    
    # Create a new Item object
    new_item = Item(name=name, quantity=quantity, location=location)
    
    # Add the new item to the session
    db.add(new_item)
    
    # Commit the transaction
    db.commit()
    
    # Close the session
    db.close()

# Script to collect user input and add items
if __name__ == "__main__":
    print("Add new item to the inventory.")
    
    # Collect item details from the user
    name = input("Enter the item name: ")
    quantity = int(input("Enter the quantity available: "))
    location = input("Enter the location (e.g., shelf number): ")
    
    # Add the item to the database
    add_item(name, quantity, location)
    print(f"Item '{name}' added to the inventory.")
