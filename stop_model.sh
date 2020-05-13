sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "kubectl delete deployment $1"
sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "kubectl delete service $1"

