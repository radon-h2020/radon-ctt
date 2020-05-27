#!/usr/bin/env groovy

def dockerImage

pipeline {
  agent none

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
