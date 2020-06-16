#!/usr/bin/env groovy

pipeline {
  agent any

  environment {
    dockerImage
  }

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
          dockerImage = docker.build("radonconsortium/radon-ctt", "./ctt-server")
        }
      }
    }
    stage('Push CTT server image to DockerHub') {
      steps {
        script {
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium', url: 'https://registry.hub.docker.com') {
            dockerImage.push("latest")
          }
        }
      }
    }
  }
}
