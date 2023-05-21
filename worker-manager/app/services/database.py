from app import logger
from app.model import ValuesTable
from datetime import datetime
from sqlalchemy import text
from typing import List


def _get_list_of_unassigned_ids(session):
    """
    This function retrieves a list of unassigned ids from a database session.
    
    @param session - the database session
    @return a list of unassigned ids
    """
    try:
        unassigned_ids = session.query(ValuesTable).filter(
            ValuesTable.current_worker.is_(None))

        if unassigned_ids is None:
            return []
        else:
            list_of_unassigned_ids = []
            for value in unassigned_ids:
                list_of_unassigned_ids.append(value.id)
            return list_of_unassigned_ids

    except Exception as e:
        logger.error(
            f"Unable to fetch the list of unassigned ids : {str(e)}")
        session.rollback()
        return []


def _get_active_workers_with_low_load(session, workers_list):
    """
    Given a session and a list of workers, return a list of workers that have a low load.
    A worker is considered to have a low load if it has less than 20 assigned ids.
    
    @param session - the current session
    @param workers_list - the list of workers
    @return a list of workers with low load
    """
    low_load_workers = []
    for worker in workers_list:
        if _get_no_of_assigned_ids_to_worker(session, worker) < 20:
            low_load_workers.append(worker)
    return low_load_workers


def _get_no_of_assigned_ids_to_worker(session, worker_name):
    """
    This function queries a database to get the number of assigned values to a worker.
    
    @param session - the database session
    @param worker_name - the name of the worker
    @return the number of assigned values to the worker
    """
    try:
        assigned_values = session.query(ValuesTable).filter_by(
            current_worker=worker_name, is_active=1)

        values_count = assigned_values.count()
        return values_count
    except Exception as e:
        logger.error(f"Error querying : {str(e)}")
        session.rollback()
        return 0


def _get_available_ids_from_table(session):
    """
    This function retrieves all available IDs from a table in a database session.
    
    @param session - the database session
    @return a list of available IDs from the table. If there is an error, an empty list is returned.
    """
    try:
        fetched_ids = session.query(
            ValuesTable).filter_by(is_active=1)
        ids_list = []
        for current_id in fetched_ids:
            ids_list.append(current_id.id)
        return ids_list
    except Exception as e:
        logger.error(f'Error fetching ids from table: {str(e)}')
        return []


def _set_current_worker_to_null(session, current_id):
    """
    This function sets the current worker to null in the database for a given session and ID.
    
    @param session - the database session
    @param current_id - the ID of the current worker
    @return None
    """
    try:
        row = session.query(ValuesTable).filter_by(
            id=current_id, is_active=1).first()
        row.current_worker = None
        row.value = 0
        row.updated_ts = datetime.now()
        session.commit()
    except Exception as e:
        logger.error(
            f'Error setting current_worker to null : {str(e)}')
        session.rollback()


def _unassign_ids_for_deleted_workers(session, workers_list):
    """
    This function unassigns ids for deleted workers in a database session. 
    It does this by querying the database for all values that have a current_worker that is not in the provided workers_list. 
    It then retrieves the ids of these values and sets their current_worker to null.
    
    @param session - the database session
    @param workers_list - a list of workers to exclude from the query
    @return None
    """
    try:
        execlude_list = workers_list
        execlude_query = f"('{execlude_list.pop(0)}'"

        for worker in execlude_list:
            execlude_query += f", '{worker}'"
        execlude_query += ')'

        query = text(
            f"SELECT * FROM `values` WHERE `current_worker` NOT IN {execlude_query}")

        ids_to_unassign = session.execute(query).fetchall()

        ids_to_change = []
        for value in ids_to_unassign:
            ids_to_change.append(value[0])

        for current_id in ids_to_change:
            _set_current_worker_to_null(session, current_id)

    except Exception as e:
        logger.error(f'Error in unassigning the ids : {str(e)}')
        session.rollback()


def _assign_id_to_worker(session, worker_name, current_id):
    """
    Assign a worker to a specific ID in the database.
    
    @param session - the database session
    @param worker_name - the name of the worker
    @param current_id - the ID to assign the worker to
    @return None
    """
    try:
        rows = session.query(
            ValuesTable).filter_by(id=current_id, is_active=1)
        if rows:
            for row in rows:
                row.current_worker = worker_name
                row.updated_ts = datetime.now()
            session.commit()
    except Exception as e:
        logger.error(f'Error assigning id to worker : {str(e)}')
        session.rollback()


def _assign_ids_to_worker(session, worker_name, ids_list: List[str]):
    """
    Assign a list of ids to a worker in a session.
    
    @param session - the session we are working in
    @param worker_name - the name of the worker we are assigning the ids to
    @param ids_list - a list of ids to assign to the worker
    @return None, but logs an error if there is an exception.
    """
    try:
        for current_id in ids_list:
            _assign_id_to_worker(session, worker_name, current_id)
    except Exception as e:
        logger.error(f'Exception in assigning ids to worker : {str(e)}')
