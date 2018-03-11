pipeline { 
    agent any 
    stages {
        stage('Build') { 
            steps { 
                echo 'Building...'
                sh 'git clone https://github.com/VincentHokie/andela-flask-api'
            }
        }
        stage('Test'){
            steps {
                echo 'testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'deploying...'
            }
        }
    }
}