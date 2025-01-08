import os
from flask import Flask, render_template, request, redirect, url_for, flash
#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
#from models import *
from flask_supabase import Supabase
from supabase import create_client

#load_dotenv()

# Initialize Flask app
app = Flask(__name__)

#App coonfiguration
app.config['SUPABASE_URI'] = os.getenv('SUPABASE_URI',"https://zyeeugykuhzkgdacahww.supabase.co")
app.config['SUPABASE_ANON_KEY'] = os.getenv('SUPABASE_ANON_KEY',"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZWV1Z3lrdWh6a2dkYWNhaHd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzYxODI2NDksImV4cCI6MjA1MTc1ODY0OX0.Q2Qw-ywg8vJa3vkWqe-PNLGuRU1yGQydxJ86v7SOUlg")

app.secret_key = os.getenv('SECRET_KEY', ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5ZWV1Z3lrdWh6a2dkYWNhaHd3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNjE4MjY0OSwiZXhwIjoyMDUxNzU4NjQ5fQ.XWEjgRiDzF4YXWCWFBJfZdS7WgeFHEfQX7Njb4jWzbE'))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
supabase_extension = Supabase(app)

# App config
#app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz_app.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
#class User(db.Model, UserMixin):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(150), nullable=False, unique=True)
   # email = db.Column(db.String(150), nullable=False, unique=True)
   # password = db.Column(db.String(200), nullable=False)

@app.route('/test-db')
def tesT_db():
    try:
        result = db.session.execute('SELECT 1').scalar()
        return "Database connected!" if result == 1 else "Connection failed."
    except Exception as e:
        return f"Error: {e}"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes for user authentication
#######for sign-up

#@app.route('/signup', methods=['GET', 'POST'])
#def signup():
 #   username = request.form.get('username')
 #   email = request.form.get('email')
 #   password = request.form.get('password')
 #   quiz_mark = request.form.get('quiz_mark', 0)
 #   try:
      #  supabase.table('Users').insert({
        #    "Username": username,
       #     "Email_Address": email,
      #      "Password": password,
     #       "Quiz_Mark": quiz_mark
    #    }).execute()
    #    flash("User added successfully!", "success")
   # except Exception as e:
   #     flash(f"Error adding user: {str(e)}", "danger")
  #  return redirect(url_for('get_users'))



#######for login 
#@app.route('/login')
#def get_users():
 #   try:
  #      response = supabase.table('Users').select("*").execute()
   #     users = response.data
    #    return render_template('login.html', users=users)
   # except Exception as e:
    #    flash(f"Error fetching users: {str(e)}", "danger")
     #   return render_template('login.html', users=[])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        Username = request.form['username']
        Email_Address = request.form['email']
        Password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(Password).decode('utf-8')
        
        if not Username or not Email_Address or not Password:
            flash('Alll fields are required!', 'error')
            return redirect(url_for("signup"))
    
        #Save user to Supabase
        supabase = supabase_extension.client
        response = supabase.auth.sign_up({
            "email": Email_Address,
            "password": Password,
        }, {
            "username": Username
        })

        if response.get("error"):
            flash(response["error"]["message"], "error")
        else:
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Both email and password are required!", "error")
            return redirect(url_for("login"))

        # Authenticate user
        supabase = supabase_extension.client
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        if response.get("error"):
            flash(response["error"]["message"], "error")
        else:
            flash("Login successful!", "success")
            return redirect(url_for("home"))
    return render_template("login.html")



#@app.route('/login1', methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        email = request.form['email']
#        password = request.form['password']
#        user = User.query.filter_by(email=email).first()

#        if user and bcrypt.check_password_hash(user.password, password):
#            login_user(user)
#            flash('Login successful!', 'success')
#            return redirect(url_for('dashboard'))
#       else:
#            flash('Login failed. Check your credentials and try again.', 'danger')

#    return render_template('login.html')

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
