from models import SessionLocal, Item

# Function to display all items in the inventory
def display_items():
    # Get a database session
    db = SessionLocal()
    
    # Query all items
    items = db.query(Item).all()
    
    # Display the items
    for item in items:
        print(f"Item ID: {item.id}, Name: {item.name}, Quantity: {item.quantity}, Location: {item.location}")
    
    db.close()

if __name__ == "__main__":
    display_items()
