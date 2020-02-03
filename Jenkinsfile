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
        secretVolume(secretName: 'jenkins-docker-builder', mountPath: '/jenkins-docker-builder'),
        secretVolume(secretName: 'anubis-pubsub-sa', mountPath: '/secrets/anubis/'),
    ],
    envVars: [
        secretEnvVar(key: 'POWERDUMMY_API_KEY', secretName: 'powerdummy-apikey', secretKey: 'api-key'),
        envVar(key: 'COGNITE_BASE_URL', value: "https://greenfield.cognitedata.com"),
        envVar(key: 'COGNITE_CLIENT_NAME', value: "powerdummy-populator")
        envVar(key: 'GOOGLE_APPLICATION_CREDENTIALS', value: '/secrets/anubis/credentials.json'),
    ]) {
    node(label) {
        def isMaster = env.BRANCH_NAME == 'master'
        def dockerImageName = "eu.gcr.io/cognitedata/powerdummy-populator"
        container('jnlp') {
            stage('Checkout') {
                checkout(scm)
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
                sh("docker build -t $dockerImageName:latest --build-arg api_key=$POWERDUMMY_API_KEY .")
            }
            if (isMaster) {
                stage("Push Docker image") {
                    sh("docker push $dockerImageName:latest")
                }
            }
        }
    }
}