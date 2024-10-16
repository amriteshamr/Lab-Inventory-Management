from sqlalchemy.orm import Session
from models import Item, SessionLocal

# Function to add items to the database
def add_item(name: str, quantity: int, location_stack: str, location_row: str, location_box: str, min_quantity: int):
    # Get a database session
    db = SessionLocal()
    
    # Create a new Item object
    new_item = Item(name=name, quantity=quantity, location_stack=location_stack, location_row=location_row, location_box=location_box, min_quantity=min_quantity)
    
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
    location_stack = input("Enter the Stack")
    location_row = input("Enter the Row")
    location_box = input("Enter the Box ")
    min_quantity = location = input("Enter Minimum Quantity")

    # Add the item to the database
    add_item(name, quantity, location_stack, location_row, location_box, min_quantity)
    print(f"Item '{name}' added to the inventory.")
