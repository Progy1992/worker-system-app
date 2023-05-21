from app import api, logger, SessionObject
import time
import itertools
import math
from app.services import cluster, database


class WorkerManager:
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
        This function runs a worker manager that assigns and unassigns tasks to workers based on their availability and load. It continuously checks for available workers and tasks, and assigns tasks to workers with low load. If there are more available tasks than workers, it scales down the number of workers. 

        @return None
        """
        try:
            logger.info(f'Worker Manager : {self.name} is getting started')
            while True:
                logger.info(
                    'Fetching the changes and re-distributing the ids among available workers if required')
                
                self.session = SessionObject()
                # Logging the list of workers
                active_workers = cluster._list_workers()
                # logger.info(f'Active Workers : {active_workers}')

                available_ids = database._get_available_ids_from_table(
                    self.session)
                # logger.info(f'Available IDs : {available_ids}')

                replica_count_for_workers = cluster._get_replicas_count_for_workers()
                # logger.info(
                #     f'Replica count for workers : {replica_count_for_workers}')

                # logger.info(
                #     f'Is downscaling required : {len(available_ids) > 0 and len(active_workers) > replica_count_for_workers and self._needs_down_scaling(len(available_ids), len(active_workers))}')

                if len(available_ids) > 0 and len(active_workers) > replica_count_for_workers and self._needs_down_scaling(len(available_ids), len(active_workers)):

                    self._down_scaling_workers(active_workers, available_ids)

                else:
                    database._unassign_ids_for_deleted_workers(self.session,
                                                               active_workers)

                    unassigned_ids = database._get_list_of_unassigned_ids(
                        self.session)

                    # logger.info(f'Workers List Again : {self._list_workers()}')
                    self._assign_unassigned_ids_to_workers(
                        database._get_active_workers_with_low_load(self.session, cluster._list_workers()), unassigned_ids)

                logger.info('Sleeping for 20 secs')
                # 20 second delay
                time.sleep(20)
        except Exception as e:
            logger.error(f'Error running worker manager : {str(e)}')

    def _needs_down_scaling(self, no_of_ids, no_of_active_workers):
        """
        Determine if down scaling is needed based on the number of IDs and active workers.

        @param no_of_ids - the number of IDs
        @param no_of_active_workers - the number of active workers
        @return True if down scaling is needed, False otherwise.
        """
        if math.ceil(no_of_ids/20) < no_of_active_workers:
            return True
        else:
            return False

    def _down_scaling_workers(self, available_workers, available_ids):
        """
        This method is a part of a class and is used to downscale the number of workers in a cluster. It checks if the number of available workers is greater than the number of ids available to be processed. If it is, it calculates the expected number of workers required to process the available ids and selects that many workers from the available pool. It then assigns the ids to the selected workers and deletes the remaining workers. If there is an error, it logs the error message.

        @param self - the instance of the class
        @param available_workers - the list of available workers
        @param available_ids - the list of available ids to be processed
        @return None
        """
        try:
            if self._needs_down_scaling(len(available_ids), len(available_workers)):
                expected_workers_count = math.ceil(len(available_ids)/20)
                selected_workers_from_available_pool = available_workers[:expected_workers_count]
                self._assign_ids_to_active_workers(
                    selected_workers_from_available_pool, available_ids)

                cluster._delete_workers(
                    available_workers[expected_workers_count:])
        except Exception as e:
            logger.error(f'Error while downscaling : {str(e)}')

    def _assign_ids_to_active_workers(self, workers_list, ids_list):
        """
        Assigns ids to active workers by creating a hash ring of workers and iterating through them.

        @param self - the object instance
        @param workers_list - a list of active workers
        @param ids_list - a list of ids to be assigned to the workers
        @return None, but logs an error if there is an exception.
        """
        try:
            workers_hash_ring = self._create_hash_ring_of_workers(workers_list)
            while len(ids_list) > 0 and self._no_of_workers_in_ring(workers_list) > 0:
                iterating_worker = next(workers_hash_ring)
                unassigned_id = ids_list.pop(0)
                database._assign_id_to_worker(self.session,
                                              iterating_worker, unassigned_id)
        except Exception as e:
            logger.error(f'Error assigning ids to the workers : {str(e)}')

    def _assign_unassigned_ids_to_workers(self, workers_list, ids_list):
        """
        This function assigns unassigned ids to workers. It creates a hash ring of workers and iterates through them. If a worker has already been assigned 20 ids, it is removed from the hash ring. If there are still ids left to assign and there are still workers in the hash ring, the next unassigned id is assigned to the current worker. If there are still ids left to assign but no workers in the hash ring, new workers are created and the function is called recursively to assign the remaining ids to the new workers.

        @param self - the object instance
        @param workers_list - a list of workers
        @param ids_list - a list of ids to assign to workers
        @return None
        """
        try:
            workers_hash_ring = self._create_hash_ring_of_workers(workers_list)
            while ids_list and len(ids_list) > 0 and self._no_of_workers_in_ring(workers_list) > 0:
                iterating_worker = next(workers_hash_ring)
                if database._get_no_of_assigned_ids_to_worker(self.session, iterating_worker) == 20:
                    workers_hash_ring = self._remove_worker_from_hash_ring(
                        workers_list, iterating_worker)
                else:
                    unassigned_id = ids_list.pop(0)
                    database._assign_id_to_worker(self.session,
                                                  iterating_worker, unassigned_id)

            if ids_list and len(ids_list) > 0:
                no_of_workers_needed = math.ceil(len(ids_list) / 20)
                newly_created_workers = cluster._create_workers(
                    no_of_workers_needed)
                self._assign_unassigned_ids_to_workers(
                    newly_created_workers, ids_list)

        except Exception as e:
            logger.error(f'Error assigning ids to workers: {str(e)}')

    def _no_of_workers_in_ring(self, workers_list):
        """
        Given a list of workers, return the number of workers in the list.

        @param workers_list - the list of workers
        @return The number of workers in the list.
        """
        return len(workers_list)

    def _create_hash_ring_of_workers(self, workers_list):
        """
        Given a list of workers, create a hash ring of workers.

        @param self - the class instance
        @param workers_list - the list of workers
        @return An iterator that cycles through the workers in a hash ring.
        """
        return itertools.cycle(workers_list)

    def _remove_worker_from_hash_ring(self, workers_list, worker_name):
        """
        Remove a worker from the list of workers and return an iterator over the remaining workers.

        @param self - the object instance
        @param workers_list - the list of workers
        @param worker_name - the name of the worker to remove
        @return an iterator over the remaining workers
        """
        workers_list.remove(worker_name)
        return itertools.cycle(workers_list)
