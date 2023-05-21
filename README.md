# Steps to deploy the application using helm chart
### `helm install worker-system worker`

## There are four folders in this reposistory. Below is the brief introduction about this folder
### 1. mysql-deploy :
#### Here we have files related to the deployemtent of mysql-service in `worker-system` namespace. Also I have created a batch file for interacting with the cluster database locally using port forwadring on 3306 port

### 2. worker-app :
#### Here we have files related to deploy the worker pod. Also have created a batch file whcih is responsible for build the image, pushing the image to docker registyr and deploying the changes on kubernetes Cluster. The pod shows the logs for thw assigned Ids to the respective running pod in the cluster and increments the value of the assigned ids by 1 every second.

### 3. worker-manager :
#### Here we have code files for the worker-manager which acts as the master. Its main responsibility is for distributing the ids between active pods and performs scaling and de-scaling when the deployment size changes or wheen the ids are adeed or removed in the `values` table in the mysql-service database. Also have a batch file whuch oooms after image building, pushing the image to the docker repository and deploying the changes on cluster. The factor to decide where the pod is or not is deceided based on the amout of ids assigned to the pod. If the count is `20` then we can say that the pod is loaded and the further ids ara to be assigned to the orther running pods of added new pods if required.

### 4. flask-api :
#### Thsi application is developed for internal testing of the application by adding/ removing data from the database. Have used port forwarding inorder to the connect tomthe cluster database and perform necessay operations.

### 5. helm-chart :
#### This folder has all the necessary files which will be used for deploying the application on kubernetes cluster
