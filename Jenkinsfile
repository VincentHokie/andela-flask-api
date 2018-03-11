pipeline {
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