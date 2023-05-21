from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ValuesTable(Base):
    """
    This is a SQLAlchemy model for a table named "values". It has the following columns:
    - id: a string column with a maximum length of 50 characters, which is the primary key of the table.
    - value: an integer column with a default value of 0.
    - current_worker: a string column with a maximum length of 50 characters, which has a default value of None.
    - previous_worker: a string column with a maximum length of 50 characters, which has a default value of None.
    - is_active: an integer column with a default value of 1.
    - created_ts: a DateTime column with a default value of the current datetime.
    - updated_ts: a DateTime column with a default value of None.
    """
    # Define the table name
    __tablename__ = 'values'

    # Define the columns of the table
    id = Column(String(50), primary_key=True)  # Unique identifier for each value
    value = Column(Integer, default=0)  # The actual value
    current_worker = Column(String(50), default=None)  # Name of the worker currently processing the value
    previous_worker = Column(String(50), default=None)  # Name of the previous worker that processed the value
    is_active = Column(Integer, default=1)  # Flag indicating if the value is active or not
    created_ts = Column(DateTime, default=datetime.now())  # Timestamp of when the value was created
    updated_ts = Column(DateTime, default=None)  # Timestamp of when the value was last updated
