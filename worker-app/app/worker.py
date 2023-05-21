from app import logger, SessionObject
from app.model import ValuesTable
import time
import uuid
from datetime import datetime

class Worker:

    def __init__(self, name: str):
        """
        This is a constructor for a class that initializes the name and session object.
        
        @param name - a string representing the name of the object
        @return None
        """
        self.name = name
        self.session = SessionObject()

    def run(self):
        """
        This function runs a worker that increments values in a table. 
        It starts by logging that the worker is starting. 
        It then enters an infinite loop where it creates a new session object. 
        It then logs the assigned ids and if there are any assigned ids, it increments the values in the table. 
        It then logs that the values were successfully incremented by 1. 
        It then sleeps for 1 second. If there is an exception, it logs the error message. 
        
        @return None
        """
        try:
            logger.info(f'Worker : {self.name} is getting started')
            while True:
                self.session = SessionObject()
                # Logging attached values ids
                assigned_ids = self._logging_assigned_ids()

                if assigned_ids and len(assigned_ids) > 0:
                    # Incrementing attached values by 1
                    self.increment_values_in_table()
                    
                    #Logging increment activit
                    logger.info('Attached values successfully increment by 1')
                
                # 1 second delay
                time.sleep(1)
        except Exception as e:
            logger.error(f'Error running worker : {str(e)}')

    def _logging_assigned_ids(self):
        """
        This function logs the assigned IDs for the current worker. 
        It queries the database for all active IDs assigned to the current worker and logs them. 
        If there is an error fetching the assigned IDs, it logs the error message.
        
        @param self - the instance of the class
        @return A list of assigned IDs.
        """
        try:
            # Fetching ids assigned to this worker object and are active
            assigned_ids = self.session.query(ValuesTable).filter_by(
                current_worker=self.name, is_active=1)
            
            # Creating a list of Ids assigned to the worker
            ids_list = []
            for value in assigned_ids:
                ids_list.append(value.id)

            # logging the ids list attached to the worker
            logger.info(f'Assigned IDs : {ids_list}')
            return ids_list

        except Exception as e:
            logger.error(
                f'Error fetching assigned ids from table : {str(e)}')

    def increment_values_in_table(self):
        """
        This method increments the values in a table by 1 for the current worker.
        It first queries the table for all rows where the current worker is assigned and is active.
        If there are any such rows, it increments the value by 1 and updates the timestamp.
        Finally, it commits the changes to the database.
        
        @param self - the instance of the class
        @return None
        """
        try:
            # Fetching values assigned to this worker object and are active
            assigned_ids = self.session.query(ValuesTable).filter_by(
                current_worker=self.name, is_active=1)

            # Updating value by 1 and update_ts by current datetime
            if assigned_ids:
                for assigned_id in assigned_ids:
                    assigned_id.value += 1
                    assigned_id.updated_ts = datetime.now()

            #Commiting session for updating the changes in the table
            self.session.commit()

        except Exception as e:
            logger.error(f'Error incrementing values : {str(e)}')

    def add_values_in_table(self):
        """
        This method adds 20 new rows to a database table called `ValuesTable`. 
        Each row has a unique ID, a value of 0, and the name of the current worker. 
        If the operation is successful, a log message is printed. 
        If there is an error, an error message is printed.
        
        @param self - the instance of the class
        @return None
        """
        try:
            
            for _ in range(0, 20):
                new_worker_value = ValuesTable(
                    id=uuid.uuid4(), value=0, current_worker=self.name)
                self.session.add(new_worker_value)

            self.session.commit()

            logger.info('Data is successfully added in the table')
        except Exception as e:
            logger.error(str(e))
