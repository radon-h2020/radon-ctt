#!/usr/bin/env groovy

pipeline {
  agent any

  options {
    timeout(time: 30, unit: 'MINUTES')
  }

  triggers {
    cron('H 4 * * *')
  }

  environment {
    DOCKER_TAG = "${env.BRANCH_NAME}"
    DOCKER_IMAGE = 'radonconsortium/radon-ctt'
  }

  stages {
    stage('Build CTT server image') {
      steps {
        script {
          if (env.BRANCH_NAME == 'master') {
            DOCKER_TAG = 'latest'
          }
          DOCKER_IMAGE = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}", "./ctt-server")
        }
      }
    }
    stage('Unit tests and coverage tests') {
      agent {
        docker {
          image DOCKER_IMAGE
          label DOCKER_TAG
          args "-e 'CTT_TEST_MODE=True' -v '$WORKSPACE:/output' --entrypoint='coverage run -m xmlrunner discover openapi_server/test/ -o /output/unittest && coverage xml -o /output/coverage.xml'"
        }
      }
      steps {
        archiveArtifacts "unittest"
        archiveArtifacts "coverage.xml"
      }
    }
    stage('Push CTT server Docker image to DockerHub') {
      steps {
        script {
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium') {
            dockerImage.push("${DOCKER_IMAGE}:${DOCKER_TAG}")
          }
        }
      }
    }
  }
}

