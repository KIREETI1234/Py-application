pipeline {
    agent any
    environment {
        DOCKERHUB_USERNAME = 'akashchandran'
        DOCKER_IMAGE = "${DOCKERHUB_USERNAME}/py-application"
        DOCKERHUB_TOKEN = credentials('docker-hub-credential')
        SONARQUBE_TOKEN = credentials('SonarQb')
        SONARQUBE_URL = 'http://34.239.141.95:9000'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    # Ensure python3-venv is installed
                    if ! dpkg -l | grep -q python3-venv; then
                        sudo apt-get update
                        sudo apt-get install -y python3-venv
                    fi
                    # Create a virtual environment and install dependencies
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Unit Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest
                '''
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    script {
                        def scannerHome = tool 'sonarqube'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=py-application \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=$SONARQUBE_URL \
                                -Dsonar.login=$SONARQUBE_TOKEN
                        """
                    }
                }
            }
        }
        stage('Build and Push Docker Image') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    echo ${DOCKERHUB_TOKEN} | docker login -u ${DOCKERHUB_USERNAME} --password-stdin
                    docker build -t ${DOCKER_IMAGE} .
                    docker push ${DOCKER_IMAGE}
                """
            }
        }
        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }
    }
    post {
        always {
            sh 'docker logout || true'
        }
    }
}
