#setup local VM Kubernetes cluster
minikube start --memory=4096
sleep 2
#Use minikube docker environment
eval $(minikube docker-env)
#Mount volume
minikube mount /media/bhavin/New\ Volume1/mtech/sem4/project/vagrant/machine_translation:/host &
sleep 3

#Deploy model
#kubectl apply -f mt-svc-deploy.yaml
#Expose ports outside container
#kubectl expose deployment mt2 --type=LoadBalancer --port=8080

#Create an external IP
#minikube service mt2 &


#Deploy UI
kubectl apply -f pyflask-svc-deploy.yaml
#Expose ports
kubectl expose deployment pyflask --type=LoadBalancer --port=5000
sleep 2
minikube service pyflask
sleep 2

