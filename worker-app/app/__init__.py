from app.model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import pymysql
import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

pymysql.install_as_MySQLdb()

# Configuring logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Create a FileHandler and set its level
file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

try:
    # Engine creation for connecting to database
    engine = create_engine(
        'mysql://root:root@mysql-service.worker-system.svc.cluster.local:3306/workers', pool_size=50, max_overflow=0)
except Exception as e:
    logger.error('Error connecting to database')
    sys.exit(1)

try:
    # Creating values table
    Base.metadata.create_all(engine)
except Exception as e:
    logger.error(f'Error creating values-table in database : {str(e)}')
    sys.exit(1)

try:
    # Creating session object
    SessionObject = sessionmaker(bind=engine)
    session = SessionObject()
except Exception as e:
    logger.error('Error initialising session object')
    sys.exit(1)
