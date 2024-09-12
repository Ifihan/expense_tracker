from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
    
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please log in.', 'error')
            return redirect(url_for('login'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['username'] = user.username
        flash('Logged in successfully!', 'success')
        
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        # Assume you have a form with fields for expense amount, category, etc.
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']

        # Create a new Expense object (assuming you have a model for Expense)
        new_expense = Expense(amount=amount, category=category, date=date, user_id=session['user_id'])

        # Save to the database
        db.session.add(new_expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_expense.html')

# from flask import render_template, redirect, url_for, flash, request, session
# from app import app, db
# from app.models import User
# from werkzeug.security import generate_password_hash, check_password_hash

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
    
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash('Email already exists. Please log in.', 'error')
#             return redirect(url_for('login'))
        
#         new_user = User(username=username, email=email)
#         new_user.set_password(password)

#         db.session.add(new_user)
#         db.session.commit()

#         flash('Account created successfully! Please log in.', 'success')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         user = User.query.filter_by(email=email).first()
        
#         if user is None or not user.check_password(password):
#             flash('Invalid email or password. Please try again.', 'error')
#             return redirect(url_for('login'))

#         session['user_id'] = user.id
#         session['username'] = user.username
#         flash('Logged in successfully!', 'success')
        
#         return redirect(url_for('index'))
    
#     return render_template('login.html')

# @app.route('/index')
# def home():
#     if 'user_id' not in session:
#         flash('Please log in to access the home page.', 'error')
#         return redirect(url_for('login'))
#     return render_template('index.html', username=session['username'])

# # @app.route('/logout')
# # def logout():
# #     session.pop('user_id', None)
# #     session.pop('username', None)
# #     flash('You have been logged out.', 'success')
# #     return redirect(url_for('index'))


# @app.route('/logout')
# def logout():
#     session.clear()  # Clear the session
#     flash('Logged out successfully.', 'success')
#     return redirect(url_for('login'))

# @app.route('/add_expense', methods=['GET', 'POST'])
# def add_expense():
#     if request.method == 'POST':
#         # Assume you have a form with fields for expense amount, category, etc.
#         amount = request.form['amount']
#         category = request.form['category']
#         date = request.form['date']

#         # Create a new Expense object (assuming you have a model for Expense)
#         new_expense = Expense(amount=amount, category=category, date=date)

#         # Save to the database
#         db.session.add(new_expense)
#         db.session.commit()

#         flash('Expense added successfully!', 'success')
#         return redirect(url_for('index'))

#     return render_template('add_expense.html')
