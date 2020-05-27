#!/usr/bin/env groovy

def dockerImage

pipeline {
  agent any

  options {
    timeout(time: 30, unit: 'MINUTES')
  }

  triggers {
    cron('H 4 * * *')
  }

  stages {
    stage('Build CTT server image') {
      steps {
        script {
          sh 'curl https://www.google.com'
          dir('./ctt-server') {
            dockerImage = docker.build("radonconsortium/radon-ctt")
          }
        }
      }
    }
    stage('Push CTT server image to DockerHub') {
      steps {
        script {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
            dockerImage.push("latest")
          }
        }
      }
    }
  }
}
