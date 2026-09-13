pipeline {
    agent any

    environment {
        // Multi-branch config: image tag and env derived from Git branch
        IMAGE_NAME = "eslamnabawy/node-multi-branch"
        BRANCH_NAME = 'main'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Building branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Setup Env') {
            steps {
                script {
                    // Map branch to image tag and environment
                    def mapping = [
                        'main': [tag: 'main', env: 'production'],
                        'stg' : [tag: 'stg',  env: 'staging'],
                        'dev' : [tag: 'dev',  env: 'development']
                    ]
                    def cfg = mapping[env.BRANCH_NAME] ?: [tag: 'dev', env: 'development']
                    env.IMAGE_TAG = cfg.tag
                    env.DEPLOY_ENV = cfg.env
                    env.DOCKER_TAG = "${env.IMAGE_NAME}:${cfg.tag}"
                }
                echo "Branch=${env.BRANCH_NAME} → Image=${env.DOCKER_TAG} → Env=${env.DEPLOY_ENV}"
            }
        }

        stage('Build Image') {
            steps {
                    sh "/usr/local/bin/docker build -t ${env.DOCKER_TAG} ."
            }
        }

        stage('Test Image') {
            steps {
                sh """
                    /usr/local/bin/docker run -d --name test-${env.BRANCH_NAME} -p 3000:3000 -e BRANCH=${env.BRANCH_NAME} -e ENV=${env.DEPLOY_ENV} ${env.DOCKER_TAG}
                    sleep 3
                    curl -sf http://localhost:3000/health || exit 1
                    /usr/local/bin/docker stop test-${env.BRANCH_NAME}
                    /usr/local/bin/docker rm test-${env.BRANCH_NAME}
                """
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh "echo \$DOCKER_PASS | /usr/local/bin/docker login -u \$DOCKER_USER --password-stdin"
                    sh "/usr/local/bin/docker push ${env.DOCKER_TAG}"
                }
                echo "Pushed: ${env.DOCKER_TAG} (eslamnabawy/node-multi-branch:${env.IMAGE_TAG})"
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for branch: ${env.BRANCH_NAME} with tag ${env.IMAGE_TAG}"
        }
    }
}
