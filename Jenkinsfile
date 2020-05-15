#!/usr/bin/env groovy

pipeline {
  environment {
  }

  agent none

  options {
    timeout(time: 30, unit: 'MINUTES')
  }

  triggers {
    cron('H 4 * * *')
  }

  def cttDockerImage

  stages {
    stage('Build CTT server image') {
      cttDockerImage = docker.build("radonconsortium/radon-ctt:latest", "./ctt-server")
    }
  }
}
