pipeline {
    agent any
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '', daysToKeepStr: '5', numToKeepStr: '20')
    }
    stages {
        stage('get git') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('H/30 * * * *')])])
                }
                git 'git@github.com:Whitehawk2/DevOpsExperts-CI_Project.git'
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
                withCredentials([string(credentialsId: 'Mysql-access', variable: 'SECRET')]) {
                    Python_nohup("./rest_app.py")
                }
            }   
        }
        stage('run web_app') {
            steps {
                withCredentials([string(credentialsId: 'Mysql-access', variable: 'SECRET')]) {
                Python_nohup("./web_app.py")
            
                }
            }
        }
        stage('Backend tests') {
            steps {
                withCredentials([string(credentialsId: 'Mysql-access', variable: 'SECRET')]) {
                    Py_venv("./backend_testing.py")
                }
            }
        }
        stage('Frontend tests') {
            steps {
                Py_venv("./frontend_testing.py")
            }
        }
        stage('Combined tests') {
            steps {
                withCredentials([string(credentialsId: 'Mysql-access', variable: 'SECRET')]) {
                    Py_venv("./combined_testing.py")
                }
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
            echo 'Run failed! check logs.'
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
