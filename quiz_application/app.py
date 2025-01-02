from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from routes import *

# Initialize Flask app
app = Flask(__name__)

# App config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/quiz_app'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# Import routes
from routes import *

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
