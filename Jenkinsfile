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
                    // Usa la configuración de la credencial almacenada en Jenkins
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-credentials-id') {
                        // Construir la imagen Docker
                        def app = docker.build("${DOCKER_REPO}:${IMAGE_TAG}")
                        // Hacer push a Docker Hub
                        app.push()
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
