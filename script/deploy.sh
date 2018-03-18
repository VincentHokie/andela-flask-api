if gcloud auth activate-service-account --key-file=~/account.json; then
    timestamp=$( date +%T )
    source /etc/environment
    
    echo "Deleting existing image..."
    gcloud compute images delete "application-ubuntu-flask-api" --project "checkpoint-project"

    echo "Building new packer image..."
    git clone https://github.com/VincentHokie/cp-infrastructure ~/cp-infrastructure
    cd ~/cp-infrastructure/packer/api
    mv ~/account.json ~/cp-infrastructure/shared/
    packer build gcp-api.json

    echo "Creating fresh instance..."
    gcloud compute instances create NAME flask-api-${timestamp} \
        --image "application-ubuntu-flask-api" \
        --machine-type "n1-standard-1" \
        --zone "us-east1-b" \
        --tags="http-server","https-server"
        --project "checkpoint-project"
fi 
