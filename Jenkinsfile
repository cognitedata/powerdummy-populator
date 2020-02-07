@Library('jenkins-helpers') _

def label = "powerdummy-populator-${UUID.randomUUID().toString()}"

podTemplate(
    label: label,
    annotations: [
            podAnnotation(key: "jenkins/build-url", value: env.BUILD_URL ?: ""),
            podAnnotation(key: "jenkins/github-pr-url", value: env.CHANGE_URL ?: ""),
    ],
    containers: [
        containerTemplate(name: 'docker',
            command: '/bin/cat -',
            image: 'docker:17.06.2-ce',
            resourceRequestCpu: '200m',
            resourceRequestMemory: '200Mi',
            resourceLimitCpu: '200m',
            resourceLimitMemory: '200Mi',
            ttyEnabled: true),
        containerTemplate(name: 'python',
            image: 'python:3.7-buster',
            command: '/bin/cat -',
            resourceRequestCpu: '2000m',
            resourceRequestMemory: '500Mi',
            resourceLimitCpu: '2000m',
            resourceLimitMemory: '500Mi',
            ttyEnabled: true
        )
    ],
    volumes: [
        hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock'),
        secretVolume(secretName: 'jenkins-docker-builder', mountPath: '/jenkins-docker-builder')
    ],
    envVars: [
        secretEnvVar(key: 'POWERDUMMY_API_KEY', secretName: 'powerdummy-apikey', secretKey: 'api-key'),
        envVar(key: 'COGNITE_BASE_URL', value: "https://greenfield.cognitedata.com"),
        envVar(key: 'COGNITE_CLIENT_NAME', value: "powerdummy-populator")
    ]) {
    node(label) {
        def isMaster = env.BRANCH_NAME == 'master'
        def dockerImageName = "eu.gcr.io/cognitedata/powerdummy-populator"
        container('jnlp') {
            stage('Checkout') {
                checkout(scm)
                dockerImageTag = sh(returnStdout: true, script: 'echo \$(date +%Y-%m-%d)-\$(git rev-parse --short HEAD)').trim()
            }
        }
        container('python') {
            stage('Install poetry') {
                sh("pip3 install --no-cache poetry")
            }
            stage('Install dependencies') {
                sh("poetry install -vvv")
            }
            stage('Check code') {
                sh("poetry run isort -rc --check-only .")
                sh("poetry run black --check .")
            }
            stage('Test') {
                sh("poetry run pytest")
            }
        }
        container('docker') {
            stage("Build Docker image") {
                sh('#!/bin/sh -e\n'
                + 'docker build -t $dockerImageName:$dockerImageTag --build-arg api_key=$POWERDUMMY_API_KEY .')
            }
            if (isMaster) {
                stage("Push Docker image") {
                    sh('#!/bin/sh -e\n' + 'docker login -u _json_key -p "$(cat /jenkins-docker-builder/credentials.json)" https://eu.gcr.io')
                    sh("docker push $dockerImageName:$dockerImageTag")
                }
            }
        }
    }
}