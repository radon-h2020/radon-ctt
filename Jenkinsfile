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
          dockerTag = env.BRANCH_NAME
          if (env.BRANCH_NAME == 'master') {
            dockerTag = 'latest'
          }
          dockerImage = docker.build("radonconsortium/radon-ctt:${dockerTag}", "./ctt-server")
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium') {
            dockerImage.push(dockerTag)
          }
        }
      }
    }
  }
}
