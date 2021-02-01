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
    DOCKER_IMAGE_BASE = 'radonconsortium/radon-ctt'
  }

  stages {
    stage('Build and push CTT server image') {
      steps {
        script {
          if (env.BRANCH_NAME == 'master') {
            DOCKER_TAG = 'latest'
          }
          dockerImage = docker.build("${DOCKER_IMAGE_BASE}:${DOCKER_TAG}", "./ctt-server")
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium') {
            dockerImage.push(DOCKER_TAG)
          }
        }
      }
    }
    stage('Unit tests and coverage tests') {
      agent {
        docker {
          image "${DOCKER_IMAGE_BASE}:${DOCKER_TAG}"
          args "-v ${WORKSPACE}/test-results:/mnt/test-results -e 'CTT_TEST_MODE=True' --entrypoint='coverage run -m xmlrunner discover openapi_server/test/ -o /mnt/test-results/unittest && coverage xml -o /mnt/test-results/coverage/coverage.xml'"
        }
        steps {
          archiveArtifacts 'test-results'
        }
      }
    }
  }
}
