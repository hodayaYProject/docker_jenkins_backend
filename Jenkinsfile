pipeline {
  environment {
    registry = "devhodi/docker-test"
    registryCredential = 'docker_hub'
    dockerImage = ''
  }
  agent any
  options {buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '20'))}
  stages {
    stage('Cloning Git') {
      steps {
        script {
            properties([pipelineTriggers([pollSCM('30 * * * *')])])
        }
        git 'https://github.com/hodayaYProject/docker_jenkins_backend.git'
      }
    }
    stage('run backend'){
      steps{
        bat 'start /min python rest_app.py'
        bat 'python backend_testing.py'
        bat 'python clean_environment.py'
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build registry + ":$BUILD_NUMBER"
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
     stage('run'){
       steps{
         bat "echo IMAGE_TAG=${BUILD_NUMBER} > .env"
         bat 'docker-compose up -d'
         bat 'python docker_backend_testing.py'
         bat 'docker-compose down'
//          bat 'helm install k8s_helm k8s_ –set image.version=”devhodi/docker-test”:${BUILD_NUMBER}'
       }
    }
    stage('Remove Unused docker image') {
      steps{
        bat "docker rmi $registry:$BUILD_NUMBER"
      }
    }
  }
}