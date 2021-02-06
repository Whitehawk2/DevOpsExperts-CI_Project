pipeline {
    agent any
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '5', numToKeepStr: '20')
    }
    environment {
        // use the password as a global env var
        SECRET = credentials('Mysql-access')
        EMAIL_TO = "a_responsible_person@company.org"
    }
    stages {
        stage('Checkout SCM') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                }
            }
        }
        stage('prepare python environment') {
            // making sure we have a working python venv with
            // all needed packages thru pip
            steps {
                script{
                    sh 'python3 -m venv pyenv'
                    PYTHON_PATH =  sh(script: 'echo ${WORKSPACE}/pyenv/bin/', returnStdout: true).trim()

                    Py_venv("-m pip install -r ./requirements.txt")
                }
            }
        }
        stage('run rest_app') {
            steps {
                Python_nohup("./rest_app.py")
            }
        }
        stage('run web_app') {
            steps {
                Python_nohup("./web_app.py")
            }
        }
        stage('Backend tests') {
            steps {
                Py_venv("./backend_testing.py")
            }
        }
        stage('Frontend tests') {
            steps {
                Py_venv("./frontend_testing.py")
            }
        }
        stage('Combined tests') {
            steps {
                Py_venv("./combined_testing.py")
            }
        }
        stage('Shut down') {
            steps {
                sh 'python3 ./clean_enviornment.py'
            }
        }
    }
    post {
        success {
            echo 'Run finished with 100% success'
        }
        failure {
            emailext body: 'Check console output at $BUILD_URL to view the results. \n\n ${CHANGES} \n\n -------------------------------------------------- \n${BUILD_LOG, maxLines=100, escapeHtml=false}',
                    to: "${EMAIL_TO}",
                    subject: 'Jenkins build failed: $PROJECT_NAME - #$BUILD_NUMBER'
        }
        changed {
            echo 'Run state has changed from last runs...'
        }
    }

}
def Py_venv(String command) {
    // an alias to using the python venv
    sh script:". ./pyenv/bin/activate && python3 ${command}", label: "py ${command}"
}
def Python_nohup(String command) {
    // as above, but for live servers with nohup
    sh script:". ./pyenv/bin/activate && nohup python3 ${command} &", label:"python_nohup ${command}"
}
