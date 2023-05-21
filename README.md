### To deploy the application using a Helm chart, please follow these steps:

#### 1. Start by navigating to the root directory of the Helm chart repository.

#### 2. Open a terminal or command prompt and execute the following command to install the application using the Helm chart:
   ```
   helm install worker-system worker-system
   ```

   This command will deploy the application named "worker-system" in the "worker-system" namespace on kubernetes cluster

#### 3. Let's take a closer look at the four folders present in this repository:

   a. **mysql-deploy:** This folder contains files related to the deployment of the MySQL service in the "worker-system" namespace. Additionally, there is a batch file that allows local interaction with the cluster database using port forwarding on port 3306.

   b. **worker-app:** Here, you'll find files related to deploying the worker pod. There is also a batch file responsible for building the image, pushing it to the Docker registry, and deploying the changes on the Kubernetes cluster. The worker pod displays logs for the assigned IDs and increments their values by 1 every second.

   c. **worker-manager:** This folder contains code files for the worker manager, which acts as the master. Its main responsibility is to distribute IDs between active pods and perform scaling and de-scaling operations when the deployment size changes or when IDs are added or removed in the "values" table in the MySQL service database. There is also a batch file that handles image building, pushing it to the Docker repository, and deploying the changes on the cluster. The decision for scaling-up is based on the count of assigned IDs. For example, if the count is 20, we can consider the pod to be loaded, and further IDs will be assigned to other running pods or create new pods if required.

   d. **flask-api:** This application is developed for internal testing of the application by adding or removing data from the database. Port forwarding is used to connect to the cluster database and perform necessary operations.

   e. **helm-chart:** This folder contains all the necessary files required for deploying the application on a Kubernetes cluster using Helm.
