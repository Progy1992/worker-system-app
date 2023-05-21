docker build -t worker-manager . 
docker login
docker tag worker-manager:latest harshrocks/worker-manager
docker push harshrocks/worker-manager     
kubectl delete pods --selector=app=worker-manager --namespace=worker-system