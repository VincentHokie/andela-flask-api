pipeline {
    agent { dockerfile true }
    environment {
        DEBUG=credentials("DEBUG")
        CSRF_ENABLED=credentials("CSRF_ENABLED")
        SQLALCHEMY_TRACK_MODIFICATIONS=credentials("SQLALCHEMY_TRACK_MODIFICATIONS")
        DB=credentials("DB")
        USER=credentials("USER")
        PASSWORD=credentials("PASSWORD")
        HOST=credentials("HOST")
        PORT=credentials("PORT")
        HEROKU_POSTGRESQL_CRIMSON_URL=credentials("HEROKU_POSTGRESQL_CRIMSON_URL")
        WTF_CSRF_ENABLED=credentials("WTF_CSRF_ENABLED")
        SECRET_KEY=credentials("SECRET_KEY")
        MAIL_SERVER=credentials("MAIL_SERVER")
        MAIL_PORT=credentials("MAIL_PORT")
        MAIL_USE_TLS=credentials("MAIL_USE_TLS")
        MAIL_USE_SSL=credentials("MAIL_USE_SSL")
        MAIL_USERNAME=credentials("MAIL_USERNAME")
        MAIL_PASSWORD=credentials("MAIL_PASSWORD")
        MAIL_DEFAULT_SENDER=credentials("MAIL_DEFAULT_SENDER")
        SERVICE_ACCOUNT=credentials("ACCOUNT_FILE")
    }
    stages {
        // stage('Build') { 
        //     steps {
        //         sh 'pip3 install --no-cache-dir -r requirements.txt'
        //     }
        // }
        // stage('Test'){
        //     steps {
        //         echo 'testingggg...ggg'
        //         sh 'chmod 777 ./script/pgfile.sh'
        //         sh './script/pgfile.sh'
        //         sh '#!/bin/bash \n '+
        //         'python3 -m pytest --cov=app app/tests/'
        //     }
        // }
        stage('Deploy') {
            steps {
                echo 'deploying...'
                sh 'chmod 777 ./script/deploy.sh'
                sh './script/deploy.sh'
            }
        }
    }
}