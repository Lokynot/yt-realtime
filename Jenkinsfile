pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out project source code'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m pip --version
                    python3 -m pip install --user pytest
                '''
            }
        }

        stage('Syntax Check') {
            steps {
                sh 'python3 -m py_compile app.py'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    sudo docker build \
                      -t yt-realtime:${BUILD_NUMBER} \
                      -t yt-realtime:latest .
                '''
            }
        }

        stage('Docker Smoke Test') {
            steps {
                sh '''
                    set -eu

                    CONTAINER_NAME="yt-realtime-test-${BUILD_NUMBER}"

                    cleanup() {
                        sudo docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    }

                    trap cleanup EXIT

                    sudo docker run -d \
                      --name "$CONTAINER_NAME" \
                      -p 127.0.0.1:18000:8000 \
                      "yt-realtime:${BUILD_NUMBER}"

                    for i in $(seq 1 15); do
                        if curl -fsS http://127.0.0.1:18000/health; then
                            echo "Smoke test passed"
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Smoke test failed"
                    sudo docker logs "$CONTAINER_NAME"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed. Check the stage logs.'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
