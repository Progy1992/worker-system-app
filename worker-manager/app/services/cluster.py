from app import logger, api, v1
import os
import uuid
import yaml


def _list_workers():
    """
    This function lists the names of all the running worker nodes in the worker-system namespace.

    @return A list of the names of all the running worker nodes.
    """
    try:
        workers = api.list_namespaced_pod(
            namespace='worker-system', label_selector='app=worker-app').items

        workers_list = []

        for worker in workers:
            if worker.status.phase == 'Running':
                workers_list.append(worker.metadata.name)

        return workers_list
    except Exception as e:
        logger.error(f'Error in listing worker nodes : {str(e)}')


def _get_replicas_count_for_workers():
    """
    This function attempts to read the number of replicas for a Kubernetes deployment named 'worker-app' in the 'worker-system' namespace. 
    If successful, it returns the number of replicas. If it fails, it logs an error message and returns None.

    @return The number of replicas for the Kubernetes deployment named 'worker-app' in the 'worker-system' namespace. If it fails, it logs an error message and returns None.
    """
    try:
        worker_deployment = v1.read_namespaced_deployment(
            'worker-app', 'worker-system')
        replica_count = worker_deployment.spec.replicas
        return replica_count
    except Exception as e:
        logger.error(f'Error getting replicas : {str(e)}')


def _get_uid_of_worker_deployment():
    """
    This function attempts to retrieve the unique identifier (UID) of a Kubernetes deployment named 'worker-app' in the 'worker-system' namespace. 
    If successful, it returns the UID. If an error occurs, it logs the error and returns None.

    @return The UID of the worker deployment, or None if an error occurs.
    """
    try:
        worker_deployment = v1.read_namespaced_deployment(
            'worker-app', 'worker-system')
        uid = worker_deployment.metadata.uid
        return uid
    except Exception as e:
        logger.error(f'Error getting uid of deployment : {str(e)}')


def _delete_worker(name):
    """
    This function deletes a worker pod from the Kubernetes cluster.

    @param name - the name of the worker pod to be deleted
    @return None. If the worker pod cannot be deleted, an error message is logged.
    """
    try:
        api.delete_namespaced_pod(name=name, namespace='worker-system')
        logger.info(f'Terminating {name}')
    except Exception as e:
        logger.error(f'Error in deleting worker : {name}')


def _delete_workers(workers_list):
    """
    Given a list of workers, delete each worker.

    @param workers_list - the list of workers to delete
    @return None. If there is an error, log the error.
    """
    try:
        for worker in workers_list:
            _delete_worker(worker)
    except Exception as e:
        logger.error(f'Error in deleting worker : {str(e)}')


def _add_worker():
    """
    This function creates a new worker pod by calling the Kubernetes API. 
    It reads the worker pod manifest and creates a new pod in the 'worker-system' namespace. 
    If the pod is created successfully, it returns the name of the pod. 
    If there is an error, it logs the error and returns None.

    @return The name of the created worker pod if successful, None otherwise.
    """
    try:
        created_worker_pod = api.create_namespaced_pod(
            body=_read_worker_app_pod_manifest(), namespace='worker-system')
        logger.info(
            f'New worker-app pod : {created_worker_pod.metadata.name} is successfully created')
        return created_worker_pod.metadata.name
    except Exception as e:
        logger.error(f'Error in creating a new worker-app pod')


def _read_worker_app_pod_manifest():
    """
    This function reads a YAML file containing the manifest for a Kubernetes pod that will run a worker application. 
    It then modifies the manifest to include the UID of the worker deployment and a unique name for the pod. 

    @return The modified worker pod manifest.
    """
    try:
        worker_pod_yaml_file = os.path.join(os.path.dirname(os.path.dirname(
            __file__)), '..', 'kube', 'worker-app-pod.yaml')
        with open(worker_pod_yaml_file, 'r') as file:
            worker_pod_manifest = yaml.safe_load(file)
        
        replicate_set_name, replicate_set_uid = _get_replicaset_details()
        worker_pod_manifest['metadata']['ownerReferences'][0]['name'] = replicate_set_name
        worker_pod_manifest['metadata']['ownerReferences'][0]['uid'] = replicate_set_uid
        
        worker_pod_manifest['metadata']['name'] = 'worker-app-' + \
            str(uuid.uuid4())
        return worker_pod_manifest
    except Exception as e:
        logger.error(
            f'Error in reading worker-app pod yaml file : {str(e)}')


def _create_workers(no_of_workers):
    """
    Create a specified number of workers and add them to a list.

    @param no_of_workers - the number of workers to create
    @return a list of newly created workers
    """
    try:
        newly_created_workers_list = []
        for _ in range(0, no_of_workers):
            newly_created_workers_list.append(_add_worker())
    except Exception as e:
        logger.error(f'Error creating new workers : {str(e)}')
        return []


def _get_replicaset_details():
    """
    This function retrieves the details of a replica set in the "worker-system" namespace.
    It first lists all the replica sets in the namespace and then searches for the one with the name "worker-app".
    If found, it returns the name and UID of the replica set, otherwise it returns None.
    
    @return A tuple containing the name and UID of the replica set, or None if not found.
    """
    try:
        replica_sets = v1.list_namespaced_replica_set(
            namespace="worker-system")
        for replica_set in replica_sets.items:
            if 'worker-app' in replica_set.metadata.name:
                return replica_set.metadata.name, replica_set.metadata.uid
        return None, None
    except Exception as e:
        logger.error(f'Error reading replica set details : {str(e)}')
