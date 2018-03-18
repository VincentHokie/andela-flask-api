alias gcloud="/home/jenkins/google-cloud-sdk/bin/gcloud"
# alias packer="/usr/local/packer"

sudo chown jenkins:jenkins /usr/local/bin/packer
sudo ls -al /usr/local/bin | grep packer
sudo ls -al /usr/local/bin | grep cd

if gcloud auth activate-service-account --key-file=${SERVICE_ACCOUNT}; then
    timestamp=$(date +%s)

    echo "Building new packer image..."
    git clone https://github.com/VincentHokie/cp-infrastructure ~/cp-infrastructure
    cd ~/cp-infrastructure/packer/api
    mv ${SERVICE_ACCOUNT} ~/cp-infrastructure/shared/
    packer build gcp-api.json -force

fi 
