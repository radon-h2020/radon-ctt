#!/usr/bin/env groovy

pipeline {
  agent any

  options {
    timeout(time: 30, unit: 'MINUTES')
  }

  triggers {
    cron('H 4 * * *')
  }

  stages {
    stage('Build and push CTT server image') {
      steps {
        script {
          dockerImage = docker.build("radonconsortium/radon-ctt", "./ctt-server")
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium', url: 'https://registry.hub.docker.com') {
            dockerImage.push("latest")
          }
        }
      }
    }
  }
}
