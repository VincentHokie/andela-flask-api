pipeline {
    agent {
        docker {
            image 'python:3.5.5-alpine3.4'
            args '-p 5000:5000'
        }
    }
    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
        export DEBUG=True
        export CSRF_ENABLED=True
        export SQLALCHEMY_TRACK_MODIFICATIONS=False

        export DB='andela-flask-api'
        export USER='postgres'
        export PASSWORD='postgres'
        export HOST='localhost'
        export PORT=5432
        export HEROKU_POSTGRESQL_CRIMSON_URL="postgresql://postgres:postgres@127.0.0.1:5432/andela-flask-api"

        export WTF_CSRF_ENABLED=False
        export SECRET_KEY='youll-never-know-what-it-is-coz-its-secret'
        export MAIL_SERVER='smtp.googlemail.com'
        export MAIL_PORT=465
        export MAIL_USE_TLS=False
        export MAIL_USE_SSL=True
        export MAIL_USERNAME="andelatestmail"
        export MAIL_PASSWORD="andelatestmail1"
        export MAIL_DEFAULT_SENDER="andelatestmail@gmail.com"
    }
    stages {
        stage('Build') { 
            steps {
                checkout scm
                sh 'cd ~'
                sh 'git clone https://github.com/VincentHokie/andela-flask-api'
                sh '~/andela-flak-api'

                sh 'sudo apt-get install -y python python-pip python-virtualenv'
                sh 'sudo pip install virtualenv'

                sh 'virtualenv --python=python3 .'
                sh 'source bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test'){
            steps {
                echo 'testingggg...ggg'
                sh '~/andela-flak-api'
                sh 'source bin/activate'
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