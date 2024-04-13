from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from gridfs import GridFS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app.filter import extract_skills
import tempfile
import os

app = Flask(__name__)
app.secret_key = 'a2V0YW5fbWVocmFfaXNfZ3JlYXQ=' # Add a secret key here

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['resume']
fs = GridFS(db)

# Collection for user management
users_collection = db['users']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    # Check if user is logged in
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        try:
            if 'pdf_file' not in request.files:
                return "No file part"
            file = request.files['pdf_file']
            if file.filename == '':
                return "No selected file"
            if file:
                filename = file.filename
                # Get user's current upload (if any)
                if 'username' in session:
                    username = session['username']
                    user = users_collection.find_one({'username': username})
                    if user and 'upload_id' in user:
                        # Delete the user's current upload
                        fs.delete(user['upload_id'])
                    # Save new file to MongoDB GridFS
                    file_id = fs.put(file.stream, filename=filename)
                    # Update user's upload_id
                    users_collection.update_one({'username': username}, {'$set': {'upload_id': file_id}})
                    print(f"File uploaded successfully with id: {file_id}")
                    return redirect(url_for('index'))
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred while uploading the file"
    return render_template('upload.html', username=session['username'])

@app.route('/parser')
@login_required
def parser():
    # Get user's current upload (if any)
    if 'username' in session:
        username = session['username']
        user = users_collection.find_one({'username': username})
        if user and 'upload_id' in user:
            # Retrieve the file from MongoDB GridFS
            file = fs.get(user['upload_id'])
            # Create a temporary file to store the content
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name
            # Pass the file path to the extract_skills function
            skills = extract_skills(temp_file_path)
            # Clean up temporary file
            os.unlink(temp_file_path)
            return render_template('parser.html', skills=skills)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = users_collection.find_one({'username': username})
        if existing_user:
            return 'Username already exists'
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({'username': username, 'password': hashed_password, 'upload_id': None})
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
