pipeline {
  environment {
//     registry = "devhodi/docker-test"
    registry = "devhodi/dockertest"
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
         bat 'echo IMAGE_TAG=${BUILD_NUMBER} > .env'
         bat 'docker-compose up -d'
         bat 'python docker_backend_testing.py'
         bat 'docker-compose down'
       }
    }
    stage('Remove Unused docker image') {
      steps{
        bat "docker rmi $registry:$BUILD_NUMBER"
      }
    }
//     stage('run helm k8s'){
//         steps{
//           bat 'helm install k8s_helm k8s_backend_test --set image.version="devhodi/docker-test:2"'
//           bat 'helm install k8s_helm k8s_backend_test --set image.version="devhodi/dockerTest:${BUILD_NUMBER}"'
//           bat 'minikube service k8s_helm --url > k8s_url.txt'
//           bat 'python k8s_backend_testing.py'
//           bat 'helm delete k8s_helm'
//         }
//     }
  }
}