#setup local VM Kubernetes cluster
#minikube start --memory=4096
sleep 2
#Use minikube docker environment
#eval $(minikube docker-env)
#Mount volume
#minikube mount /media/bhavin/New\ Volume1/mtech/sem4/project/vagrant/machine_translation:/host &
#sleep 3
#Deploy model
UPLOAD_FOLDER="uploads/"
cp gen_yaml.py $UPLOAD_FOLDER/temp1.py
cd $UPLOAD_FOLDER

if [ ! -d "$1" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  unzip $1.zip -d $1

fi

apt-get update
apt-get install sshpass -y



#sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "echo `ifconfig | grep inet`"

#cd "/media/bhavin/New Volume1/mtech/sem4/project/vagrant/machine_translation/"



#pwd
#ls


sleep 2

echo 'hello'

python temp1.py $1 $2
echo 'world'
rm temp1.py
echo 'removed temp1.py'
cd ..

sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 'bash -s' < kube_deploy.sh $1
echo 'ssh done'
#sshpass -p "bkotak" ssh bhavin@192.168.1.15 'bash -s' < "kubectl apply -f uploads/"$1".yaml"
#kubectl apply -f /host/uploads/$1.yaml
#Expose ports outside container
#kubectl expose deployment $1 --type=LoadBalancer --port=8080
#Create an external IP
#minikube service mt2 &


#Deploy UI
#kubectl apply -f pyflask-svc-deploy.yaml
#Expose ports
#kubectl expose deployment pyflask --type=LoadBalancer --port=5000

#minikube service pyflask


