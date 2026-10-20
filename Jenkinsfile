pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'jashmakadia'
        IMAGE = 'jashmakadia/task-manager'
        TAG = "${BUILD_NUMBER}"
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
                sh '''
                    docker build -t "$IMAGE:$TAG" -t "$IMAGE:latest" .
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDS_PSW" | docker login \
                        -u "$DOCKERHUB_CREDS_USR" --password-stdin
                    docker push "$IMAGE:$TAG"
                    docker push "$IMAGE:latest"
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                    kubectl set image deployment/task-manager app="$IMAGE:$TAG"
                    kubectl rollout status deployment/task-manager --timeout=180s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl get pods -l app=task-manager
                    kubectl get deployment task-manager
                    kubectl get svc task-manager

                    kubectl port-forward --address 127.0.0.1 \
                        svc/task-manager 5002:5000 \
                        >/tmp/task-manager-verify.log 2>&1 &
                    PF_PID=$!
                    trap 'kill "$PF_PID" 2>/dev/null || true' EXIT

                    for i in $(seq 1 15); do
                        if curl --connect-timeout 2 -fsS \
                            http://127.0.0.1:5002/health; then
                            echo
                            echo "Application health check passed"
                            exit 0
                        fi
                        sleep 2
                    done

                    cat /tmp/task-manager-verify.log
                    echo "Health check failed"
                    exit 1
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
