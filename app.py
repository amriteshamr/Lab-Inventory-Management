from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from models import SessionLocal, Item  # Import the session and Item model
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yoursecretkey'  # Needed for sessions

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Change the home route to redirect to login if user is not authenticated
@app.route('/')
def home():
    return redirect(url_for('login'))



# @app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
# def dashboard():
#     session = SessionLocal()
#     search_query = request.args.get('search', '')  # Get the search query from the URL parameters
#     if search_query:
#         # Query for items with names that contain the search query
#         items = session.query(Item).filter(Item.name.like(f'%{search_query}%')).all()
#     else:
#         # Fetch all items if no search query
#         items = session.query(Item).all()
#     session.close()
#     return render_template('dashboard.html', items=items, search_query=search_query)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    session = SessionLocal()
    search_query = request.args.get('search', '')  # Get the search query from the URL parameters
    
    if search_query:
        # Query for items with names that contain the search query, ordered by recently added
        items = session.query(Item).filter(Item.name.like(f'%{search_query}%')).order_by(Item.id.desc()).all()
    else:
        # Fetch all items ordered by recently added
        items = session.query(Item).order_by(Item.id.desc()).all()
    
    session.close()
    return render_template('dashboard.html', items=items, search_query=search_query)



# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    usernames = ['admin', 'tim', 'rene', 'anaz', 'asin', 'allan', 'preeta']
    if request.method == 'POST':
        # Handle login form submission (this is just a placeholder for real authentication)
        username = request.form['username']
        password = request.form['password']
        # Assuming there's only one lab in charge (hardcoded login)
        if username in usernames and password == 'password':
            login_user(User())  # A fake user object
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')

# Dummy user class to mock login behavior (Flask-Login requires a user object)
class User(UserMixin):
    id = 1

@login_manager.user_loader
def load_user(user_id):
    return User()

@app.route('/add_equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        location_stack = request.form['location_stack']
        location_row = request.form['location_row']
        location_box = request.form['location_box']
        min_quantity = int(request.form['min_quantity'])  # Get the minimum quantity
        
        session = SessionLocal()
        new_item = Item(name=name, quantity=quantity, location_stack=location_stack, location_row=location_row, location_box=location_box, min_quantity=min_quantity)
        session.add(new_item)
        session.commit()
        session.close()
        
        flash('New equipment added successfully!')
        return redirect(url_for('add_equipment'))
    
    return render_template('add_equipment.html')




@app.route('/view_inventory')
@login_required
def view_inventory():
    session = SessionLocal()

    # Get parameters
    sort_column = request.args.get('sort_column', 'id')
    sort_order = request.args.get('sort_order', 'asc')
    filter_column = request.args.get('filter_column', '')
    filter_value = request.args.get('filter_value', '')

    valid_columns = {
        'name': Item.name,
        'quantity': Item.quantity,
        'location_stack': Item.location_stack,
        'location_row': Item.location_row,
        'location_box': Item.location_box,
    }

    query = session.query(Item)

    # Filtering
    if filter_column in valid_columns and filter_value:
        query = query.filter(valid_columns[filter_column] == filter_value)

    # Sorting
    if sort_column in valid_columns:
        sort_attr = valid_columns[sort_column]
        if sort_order == 'desc':
            sort_attr = sort_attr.desc()
        query = query.order_by(sort_attr)

    # Fetch data
    items = query.all()

    # Get suggestions for the filter input
    suggestions = []
    if filter_column in valid_columns:
        suggestions_query = session.query(valid_columns[filter_column]).distinct()
        suggestions = [str(row[0]) for row in suggestions_query]

    session.close()

    return render_template(
        'view_inventory.html',
        items=items,
        sort_column=sort_column,
        sort_order=sort_order,
        filter_column=filter_column,
        filter_value=filter_value,
        suggestions=suggestions,
    )


@app.route('/update_item', methods=['GET', 'POST'])
@login_required
def update_item():
    session = SessionLocal()
    if request.method == 'POST':
        item_id = request.form['item_id']
        change_in_quantity = int(request.form['change_in_quantity'])
        change_type = request.form['change_type']
        
        # Fetch the item from the database
        item = session.query(Item).get(item_id)
        
        if item:
            # Update the quantity (increase or decrease)
            if change_type == 'increase':
                item.quantity += change_in_quantity
            elif change_type == 'decrease':
                item.quantity -= change_in_quantity
                if item.quantity < 0:
                    item.quantity = 0
            
            # Check if quantity falls below the minimum threshold
            if item.quantity < item.min_quantity:
                flash(f'Warning: The quantity of {item.name} is below the minimum threshold ({item.min_quantity}). Please reorder!')

            session.commit()
            flash(f'Quantity updated! New quantity of {item.name}: {item.quantity}')
        else:
            flash('Item not found!')
        
        session.close()
        return redirect(url_for('update_item'))
    
    # Fetch all items to display in the form
    items = session.query(Item).all()
    session.close()
    return render_template('update_item.html', items=items)



@app.route('/delete_item', methods=['GET', 'POST'])
@login_required
def delete_item():
    session = SessionLocal()
    if request.method == 'POST':
        item_id = request.form['item_id']
        item = session.query(Item).get(item_id)
        
        # If item exists, delete it
        if item:
            session.delete(item)
            session.commit()
            flash('Item deleted successfully!')
        else:
            flash('Item not found!')
        
        session.close()
        return redirect(url_for('delete_item'))
    
    # Get all items to select which one to delete
    items = session.query(Item).all()
    session.close()
    return render_template('delete_item.html', items=items)
    



# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)