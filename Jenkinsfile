pipeline {
    // agent {
    //     docker {
    //         image 'python:3.5.5-alpine3.4'
    //         args '-p 5000:5000'
    //     }
    // }
    stages {
        stage('Build') { 
            steps {
                sh 'echo ${USER}'
                echo 'Buildinggggg...'
                sh 'git clone https://github.com/VincentHokie/andela-flask-api'
            }
        }
        stage('Test'){
            steps {
                echo 'testingggg...ggg'
                sh 'py.test --cov=app app/tests/'
            }
        }
        stage('Deploy') {
            steps {
                echo 'deploying...'
            }
        }
    }
}