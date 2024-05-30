from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "337234"
app.config["MONGO_URI"] = "mongodb://mongo:27017/rc_recommunity"
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

@app.route('/admin')
def admin():
    if 'username' in session:
        return render_template('admin.html')  # Render the admin page
    return redirect(url_for('login'))

@app.route('/add_model', methods=['POST'])
def add_model():
    if 'username' in session:
        media_link = request.form.get('media_link')
        model_name = request.form.get('model_name')
        manufacture = request.form.get('manufacture')
        year_of_release = request.form.get('year_of_release')
        description = request.form.get('description')
        pros_cons = request.form.get('pros_cons')
        image_urls = [
            request.form.get(f'image_url_{i+1}') for i in range(3)
        ]  # Get up to 3 image URLs
        
        new_model = {
            'media_link': media_link,
            'model_name': model_name,
            'manufacture': manufacture,
            'year_of_release': year_of_release,
            'description': description,
            'pros_cons': pros_cons,
            'image_urls': image_urls,  # Add image URLs to the model data
            'created_by': session['username'],
            'created_at': datetime.utcnow()
        }
        
        mongo.db.models.insert_one(new_model)
        flash('Model added successfully!', 'success')
        return redirect(url_for('admin'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
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

            # Create a new user in DB
            new_user = {
                'username': username,
                'email': email,
                'password': hashed_password
            }

            # Insert the new user into the DB
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

    # If fails render to login again after GET request
    return render_template('login.html')

@app.route('/models')
def models():
    if 'username' in session:
        models = mongo.db.models.find()
        return render_template('models.html', models=models)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/search')
def search():
    if 'username' in session:
        query = request.args.get('query', '')
        if query:
            models = list(mongo.db.models.find({'model_name': {'$regex': query, '$options': 'i'}}))
        else:
            models = []
        return render_template('search_results.html', models=models, query=query)
    return redirect(url_for('login'))

@app.route('/model/<model_id>')
def model_detail(model_id):
    if 'username' in session:
        model = mongo.db.models.find_one({'_id': ObjectId(model_id)})
        comments = list(mongo.db.comments.find({'model_id': model_id}))

        # Transform YouTube URL if necessary
        if 'youtube.com/watch?v=' in model.get('video_url', ''):
            model['video_url'] = model['video_url'].replace('watch?v=', 'embed/')

        return render_template('model_detail.html', model=model, comments=comments)
    return redirect(url_for('login'))

@app.route('/model/<model_id>/comment', methods=['POST'])
def add_comment(model_id):
    if 'username' in session:
        username = session['username']
        comment_text = request.form.get('comment')
        rating = int(request.form.get('rating'))

        comment = {
            'model_id': model_id,
            'username': username,
            'text': comment_text,
            'rating': rating,
            'date': datetime.now()
        }

        mongo.db.comments.insert_one(comment)
        return redirect(url_for('model_detail', model_id=model_id))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
