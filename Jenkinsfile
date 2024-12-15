pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_SECRET = 'my-docker-credentials'
        DOCKER_REPO = 'jorgesm15/nodejs-app' // Ajusta el nombre del repositorio
        IMAGE_TAG = 'latest' // Ajusta según la etiqueta que quieras usar
        OPENSHIFT_TOKEN = credentials('openshift-token')  // 'openshift-token' es el ID del Secret que creaste
    }
    stages {
        stage('Login to OpenShift') {
            steps {
                script {
                    // Usamos 'oc' para loguearnos a OpenShift y hacer uso del Secret de Docker
                    sh 'oc login --server=https://api.sandbox-m3.1530.p1.openshiftapps.com:6443 --token=${OPENSHIFT_TOKEN}'
                    sh 'oc secrets link default my-docker-credentials --for=pull'
                }
            }
        }
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/jorgesm15/openshift-jenkins.git'
            }
        }
        stage('Build and Push Docker Image') {
            steps {
                script {
                    // Utilizamos Docker para construir y subir la imagen
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials-id') {
                        docker.image("${DOCKER_REPO}:${IMAGE_TAG}").build()
                        docker.image("${DOCKER_REPO}:${IMAGE_TAG}").push()
                    }
                }
            }
        }
        stage('Deploy to OpenShift') {
            steps {
                sh '''
                oc login --token=sha256~PQTldw15zMvnBTpX5QA0GZZI6LaOdvk2JOBI0gQ99Ps --server=https://api.sandbox-m3.1530.p1.openshiftapps.com:6443
                oc project jorgesm15-dev
                oc apply -f k8s/deployment.yml
                '''
            }
        }
    }
}
