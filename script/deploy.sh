touch /home/jenkins/account.json
sudo find / -name packer

alias gcloud="/home/jenkins/google-cloud-sdk/bin/gcloud"
alias packer="/usr/local/packer"

if gcloud auth activate-service-account --key-file=${SERVICE_ACCOUNT}; then
    timestamp=$( date +%T )

    # echo "Deleting existing image..."
    # gcloud compute images delete "application-ubuntu-flask-api" --project "checkpoint-project"

    echo "Building new packer image..."
    git clone https://github.com/VincentHokie/cp-infrastructure ~/cp-infrastructure
    cd ~/cp-infrastructure/packer/api
    mv ${SERVICE_ACCOUNT} ~/cp-infrastructure/shared/
    packer build gcp-api.json -force

    echo "Creating fresh instance..."
    gcloud compute instances create NAME flask-api-${timestamp} \
        --image "application-ubuntu-flask-api" \
        --machine-type "n1-standard-1" \
        --zone "us-east1-b" \
        --tags="http-server","https-server" \
        --project "checkpoint-project"
fi 
