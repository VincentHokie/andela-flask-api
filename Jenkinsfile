node {
    stage "Prepare environment"
        checkout scm
        def environment  = docker.build 'cloudbees-node'

        environment.inside {

            stage "Checkout and build deps"
                sh 'pip3 install -r requirements.txt'

            stage "Test"
                echo 'testingggg...ggg'
                sh 'py.test --cov=app app/tests/'

        }
}


// pipeline {
//     agent {
//         docker {
//             image 'python:3.5-onbuild'
//             args '-u root:root -p 5433:5433'
//         }
//     }
//     environment {
//         DEBUG='True'
//         CSRF_ENABLED='True'
//         SQLALCHEMY_TRACK_MODIFICATIONS='False'
//         DB='andela-flask-api'
//         USER='postgres'
//         PASSWORD='postgres'
//         HOST='172.17.0.1'
//         PORT=5432
//         HEROKU_POSTGRESQL_CRIMSON_URL="postgresql://${USER}:${PASSWORD}@${HOST}:5432/${DB}" 
//         WTF_CSRF_ENABLED='False'
//         SECRET_KEY='youll-never-know-what-it-is-coz-its-secret'
//         MAIL_SERVER='smtp.googlemail.com'
//         MAIL_PORT=465
//         MAIL_USE_TLS='False'
//         MAIL_USE_SSL='True'
//         MAIL_USERNAME="andelatestmail"
//         MAIL_PASSWORD="andelatestmail1"
//         MAIL_DEFAULT_SENDER="andelatestmail@gmail.com"
//     }
//     stages {

//         stage ("Prepare environment"){
//             checkout scm
//             def environment  = docker.build 'cloudbees-node'

//             environment.inside {
//                 stage "Checkout and build deps"
//                     sh "npm install"

//                 stage "Validate types"
//                     sh "./node_modules/.bin/flow"

//                 stage "Test and validate"
//                     sh "npm install gulp-cli && ./node_modules/.bin/gulp"
//                     junit 'reports/**/*.xml'
//             }
//         }

//         stage('Build') { 
//             steps {
//                 sh 'pip3 install -r requirements.txt'
//             }
//         }
//         stage('Test'){
//             steps {
//                 echo 'testingggg...ggg'
//                 sh 'py.test --cov=app app/tests/'
//             }
//         }
//         stage('Deploy') {
//             steps {
//                 echo 'deploying...'
//             }
//         }
//     }
// }