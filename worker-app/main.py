from app.worker import Worker
import os

if __name__ == "__main__":
    pod_name = os.environ.get('HOSTNAME')  # Get the pod name from the 'HOSTNAME' environment variable
    worker = Worker(name=pod_name)  # Create a Worker instance with the pod name as the name parameter
    worker.run()  # Start the worker's execution