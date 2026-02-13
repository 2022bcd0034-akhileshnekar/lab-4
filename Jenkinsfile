pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "akhileshnekar/ml-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'git-creds',
                    url: 'https://github.com/2022bcd0034-akhileshnekar/lab-4'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . .venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    env.CURRENT_ACCURACY = sh(
                        script: "jq '.accuracy' artifacts/metrics.json",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    def best = credentials('best-accuracy')
                    env.IS_BETTER = sh(
                        script: "echo ${env.CURRENT_ACCURACY} '>' ${best} | bc",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build Docker Image') {
            when { expression { env.IS_BETTER == '1' } }
            steps {
                sh '''
                docker build -t $DOCKER_IMAGE:${BUILD_NUMBER} .
                docker tag $DOCKER_IMAGE:${BUILD_NUMBER} $DOCKER_IMAGE:latest
                '''
            }
        }

        stage('Push Docker Image') {
            when { expression { env.IS_BETTER == '1' } }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $DOCKER_IMAGE:${BUILD_NUMBER}
                    docker push $DOCKER_IMAGE:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**'
        }
    }
}
