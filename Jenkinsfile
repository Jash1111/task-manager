pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'jashmakadia'
        IMAGE          = "${DOCKERHUB_USER}/task-manager"
        TAG            = "${BUILD_NUMBER}"
        // Jenkins credential of type "Username with password"
        // exposes DOCKERHUB_CREDS_USR and DOCKERHUB_CREDS_PSW
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet pytest -r requirements.txt
                    python -m py_compile app.py
                    python -m pytest -q tests
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDS_PSW" | docker login -u "$DOCKERHUB_CREDS_USR" --password-stdin
                    docker push $IMAGE:$TAG
                    docker push $IMAGE:latest
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl set image deployment/task-manager app=$IMAGE:$TAG
                    kubectl rollout status deployment/task-manager --timeout=120s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl get pods -l app=task-manager
                    kubectl get deployment task-manager
                    kubectl get svc task-manager
                    curl -sf http://$(minikube ip):30080/health && echo " <- app is healthy"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
    }
}
