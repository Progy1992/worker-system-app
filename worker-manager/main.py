from app.worker_manager import WorkerManager
import os

if __name__ == '__main__':
    worker_manager_name = os.environ.get('HOSTNAME')  # Get the hostname from environment variables
    worker_manager = WorkerManager(worker_manager_name)  # Create an instance of WorkerManager
    worker_manager.run()  # Run the worker manager