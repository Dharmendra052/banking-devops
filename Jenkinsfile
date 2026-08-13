pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        ECR_REPOSITORY = 'banking-app'
        ECR_REGISTRY = '923093694371.dkr.ecr.ap-south-1.amazonaws.com'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Application Test') {
            steps {
                dir('application') {
                    sh '''
                        python3 --version
                        python3 -m py_compile app.py
                        echo "Application syntax test passed"
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                dir('application') {
                    sh '''
                        docker build \
                          -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG} .
                    '''
                }
            }
        }

        stage('Docker Test') {
            steps {
                sh '''
                    docker run -d \
                      --name banking-app-ci-${BUILD_NUMBER} \
                      -p 18080:8080 \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}

                    sleep 5

                    curl -f http://localhost:18080/health

                    docker rm -f banking-app-ci-${BUILD_NUMBER}
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password \
                      --region ${AWS_REGION} | \
                    docker login \
                      --username AWS \
                      --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    docker push \
                      ${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f banking-app-ci-${BUILD_NUMBER} 2>/dev/null || true
            '''
        }
    }
}
