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
    DOCKER_NAME = 'radonconsortium/radon-ctt'
    DOCKER_IMAGE = ''
  }

  stages {
    stage('Build CTT server image') {
      steps {
        script {
          if (env.BRANCH_NAME == 'master') {
            DOCKER_TAG = 'latest'
          }
          DOCKER_IMAGE = docker.build("${DOCKER_NAME}:${DOCKER_TAG}", "./ctt-server")
        }
      }
    }
    stage('Unit tests and coverage tests') {
      options {
        skipDefaultCheckout true
      }
      steps {
        script {
          sh "docker run -e 'CTT_TEST_MODE=True' -v '${WORKSPACE}:/output' --entrypoint '/bin/sh' ${DOCKER_NAME}:${DOCKER_TAG} -c 'coverage run -m xmlrunner discover openapi_server/test/ -o /output/unittest && sh 'coverage xml -o /output/coverage.xml'"
        }
      }
    }
    stage('Store test results') {
      steps {
        archiveArtifacts "unittest"
        archiveArtifacts "coverage.xml"
      }
    }
    stage('Push CTT server Docker image to DockerHub') {
      steps {
        script {
          withDockerRegistry(credentialsId: 'dockerhub-radonconsortium') {
            DOCKER_IMAGE.push("${DOCKER_NAME}:${DOCKER_TAG}")
          }
        }
      }
    }
  }
}

