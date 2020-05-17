sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "kubectl delete deployment $1"
sshpass -p "bkotak" ssh -o StrictHostKeyChecking=no bhavin@192.168.1.15 "kubectl delete service $1"

#UPLOAD_FOLDER="uploads/"
#cd $UPLOAD_FOLDER
#if [ -d "$1" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
#  rm -rf $1*

#fi
