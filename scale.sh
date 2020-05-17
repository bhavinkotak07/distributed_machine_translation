sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "kubectl scale --replicas=$2 deployment $1"

