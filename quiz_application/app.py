import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask app
app = Flask(__name__)

# App config
app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz_app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes for user authentication
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add new user to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('landing-page_index.html')

# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# Quiz creation route
@app.route('/create-quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        questions = request.form.getlist('questions')

        # Process quiz creation logic here
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_quiz.html')

# Quiz attempt route
@app.route('/attempt-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def attempt_quiz(quiz_id):
    if request.method == 'POST':
        answers = request.form.getlist('answers')

        # Process quiz attempt logic here
        flash('Quiz submitted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('attempt_quiz.html', quiz_id=quiz_id)
# Topic routes
@app.route('/python')
def python_page():
    return render_template('python.html', title="Python")

@app.route('/javascript')
def javascript_page():
    return render_template('javascript.html', title="JavaScript")

@app.route('/c')
def c_page():
    return render_template('c.html', title="C Programming")

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
