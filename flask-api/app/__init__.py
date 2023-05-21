from flask import Flask  # Import the Flask module
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database operations
import pymysql  # Import pymysql for MySQL database connection

app = Flask(__name__)  # Create a Flask application

pymysql.install_as_MySQLdb()  # Install pymysql as the MySQLdb driver

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/workers'  # Set the database URI for SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Enable track modifications for SQLAlchemy

db = SQLAlchemy(app)  # Create a SQLAlchemy instance using the Flask application

with app.app_context():
    db.create_all()  # Create all database tables defined in the models
