from app import db  # Import the db instance from the app module
from datetime import datetime  # Import datetime module

class ValuesTable(db.Model):
    """
    This is a SQLAlchemy model for a table called "values". It has the following columns:
    - id: a string primary key with a maximum length of 50 characters
    - value: an integer column with a default value of 0
    - current_worker: a string column with a maximum length of 50 characters and a default value of None
    - previous_worker: a string column with a maximum length of 50 characters and a default value of None
    - is_active: an integer column with a default value of 1
    - created_ts: a DateTime column with a default value of the current datetime
    - updated_ts: a DateTime column with a default value of None
    """
    __tablename__ = 'values'  # Set the table name for the model

    id = db.Column(db.String(50), primary_key=True)  # Define the 'id' column with a primary key constraint
    value = db.Column(db.Integer, default=0)  # Define the 'value' column as an integer with a default value of 0
    current_worker = db.Column(db.String(50), default=None)  # Define the 'current_worker' column as a string with a default value of None
    previous_worker = db.Column(db.String(50), default=None)  # Define the 'previous_worker' column as a string with a default value of None
    is_active = db.Column(db.Integer, default=1)  # Define the 'is_active' column as an integer with a default value of 1
    created_ts = db.Column(db.DateTime, default=datetime.now())  # Define the 'created_ts' column as a DateTime with a default value of the current timestamp
    updated_ts = db.Column(db.DateTime, default=None)  # Define the 'updated_ts' column as a DateTime with a default value of None
