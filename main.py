from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = "337234"
app.config["MONGO_URI"] = "mongodb://localhost:27017/rc_recommunity"
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))  # Redirect to home page if logged in
    return render_template('index.html')  # Render index page if not logged in

@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']  # Get username from session
        return render_template('home.html', username=username)  # Pass username to template
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'POST':
        username = request.form.get('username')  # Get username from form
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if email or username is already registered
        existing_user = mongo.db.users.find_one({'$or': [{'email': email}, {'username': username}]})
        if existing_user:
            flash('Email or username already registered.', 'error')
            return redirect(url_for('register'))

        try:
            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create a new user document
            new_user = {
                'username': username,
                'email': email,
                'password': hashed_password
            }

            # Insert the new user into the database
            mongo.db.users.insert_one(new_user)

            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred while registering. Please try again later.', 'error')
            print(f'Error: {e}')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        # Find user by username or email
        user = mongo.db.users.find_one({'$or': [{'username': username_or_email}, {'email': username_or_email}]})

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash('Invalid username/email or password combination.', 'error')
            return render_template('login.html')

    # If it's a GET request, simply render the login page
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
