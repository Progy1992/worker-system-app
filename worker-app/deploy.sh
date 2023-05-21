docker build -t worker-app . 
docker login
docker tag worker-app:latest harshrocks/worker-app
docker push harshrocks/worker-app     
kubectl delete pods --selector=app=worker-app --namespace=worker-system