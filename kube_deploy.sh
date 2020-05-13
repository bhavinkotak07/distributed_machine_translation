#kubectl version
cd "/media/bhavin/New Volume1/mtech/sem4/project/vagrant/machine_translation/"

#touch te.txt
kubectl apply -f uploads/$1.yaml
kubectl expose deployment $1 --type=LoadBalancer --port=8080
sleep 3