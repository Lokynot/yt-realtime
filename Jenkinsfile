pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME = 'yt-realtime'
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_PORT = '8000'
        SMOKE_TEST_PORT = '18000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code'
                checkout scm
            }
        }

        stage('Python Environment Setup') {
            steps {
                sh '''
                    set -e

                    python3 --version

                    python3 -m venv .venv

                    .venv/bin/python -m pip install --upgrade pip

                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Syntax Check') {
            steps {
                sh '''
                    set -e

                    .venv/bin/python -m py_compile app.py

                    echo "Python syntax check passed"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -e

                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -e

                    docker build \
                        -t ${APP_NAME}:${IMAGE_TAG} \
                        -t ${APP_NAME}:latest .

                    docker images ${APP_NAME}
                '''
            }
        }

        stage('Docker Smoke Test') {
            steps {
                sh '''
                    set -eu

                    CONTAINER_NAME="${APP_NAME}-test-${BUILD_NUMBER}"

                    cleanup() {
                        docker rm -f "$CONTAINER_NAME" \
                            >/dev/null 2>&1 || true
                    }

                    trap cleanup EXIT

                    docker run -d \
                        --name "$CONTAINER_NAME" \
                        -p 127.0.0.1:${SMOKE_TEST_PORT}:${CONTAINER_PORT} \
                        "${APP_NAME}:${IMAGE_TAG}"

                    echo "Waiting for application..."

                    for i in $(seq 1 15); do

                        if curl -fsS \
                            http://127.0.0.1:${SMOKE_TEST_PORT}/health; then

                            echo ""
                            echo "Docker smoke test PASSED"
                            exit 0
                        fi

                        sleep 2
                    done

                    echo "Docker smoke test FAILED"

                    docker logs "$CONTAINER_NAME"

                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: CI pipeline completed successfully!'
        }

        failure {
            echo 'FAILURE: Check the failed stage in Console Output.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
