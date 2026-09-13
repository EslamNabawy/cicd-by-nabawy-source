pipeline {
    agent any

    environment {
        IMAGE_NAME = "eslamnabawy/node-multi-branch"
        // BRANCH_NAME comes from Jenkins Git branch (env.BRANCH_NAME / env.GIT_BRANCH) — no hardcode
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
                    // Resolve branch: prefer BRANCH_NAME (multibranch), fallback to GIT_BRANCH or main
                    def rawBranch = env.BRANCH_NAME ?: env.GIT_BRANCH ?: 'main'
                    def branch = rawBranch.contains('/') ? rawBranch.tokenize('/').last() : rawBranch
                    def mapping = [
                        'main': [tag: 'main', env: 'production'],
                        'stg' : [tag: 'stg',  env: 'staging'],
                        'dev' : [tag: 'dev',  env: 'development']
                    ]
                    def cfg = mapping[branch] ?: [tag: 'dev', env: 'development']
                    env.RESOLVED_BRANCH = branch
                    env.IMAGE_TAG = cfg.tag
                    env.DEPLOY_ENV = cfg.env
                    env.DOCKER_TAG = "${env.IMAGE_NAME}:${cfg.tag}"
                    if (branch != env.BRANCH_NAME) {
                        echo "Normalized branch '${env.BRANCH_NAME}' -> '${branch}'"
                    }
                }
                echo "Branch=${env.RESOLVED_BRANCH} → Image=${env.DOCKER_TAG} → Env=${env.DEPLOY_ENV}"
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
                    set -e
                    echo "Cleaning any prior test container..."
                    /usr/local/bin/docker rm -f test-\${RESOLVED_BRANCH} 2>/dev/null || true
                    echo "Starting test container..."
                    /usr/local/bin/docker run -d --name test-\${RESOLVED_BRANCH} -p 3000:3000 -e BRANCH=\${RESOLVED_BRANCH} -e ENV=\${DEPLOY_ENV} \${DOCKER_TAG}
                    echo "Waiting for app..."
                    sleep 5
                    echo "Health check via host.docker.internal:3000..."
                    for i in 1 2 3 4 5 6; do
                      if curl -sf http://host.docker.internal:3000/health; then
                        echo "Health check PASSED (attempt \$i)"
                        break
                      fi
                      echo "Health check retry \$i/6..."
                      sleep 3
                      if [ \$i -eq 6 ]; then
                        echo "Health check FAILED after 6 attempts — dumping logs:"
                        /usr/local/bin/docker logs test-\${RESOLVED_BRANCH} || true
                        /usr/local/bin/docker rm -f test-\${RESOLVED_BRANCH} || true
                        exit 1
                      fi
                    done
                    echo "Stopping test container..."
                    /usr/local/bin/docker rm -f test-\${RESOLVED_BRANCH}
                """
            }
        }

        stage('Push Image') {
            steps {
                script {
                    try {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh "echo \$DOCKER_PASS | /usr/local/bin/docker login -u \$DOCKER_USER --password-stdin"
                            sh "/usr/local/bin/docker push ${env.DOCKER_TAG}"
                        }
                        echo "Pushed: ${env.DOCKER_TAG} (eslamnabawy/node-multi-branch:${env.IMAGE_TAG})"
                    } catch (e) {
                        echo "WARNING: Push skipped — 'dockerhub-credentials' not found or push failed: ${e.getMessage()}"
                        echo "Image built locally: ${env.DOCKER_TAG} — create Jenkins credential ID 'dockerhub-credentials' to enable push."
                    }
                }
            }
        }
    }

    post {
        always {
            sh "/usr/local/bin/docker rm -f test-\${RESOLVED_BRANCH} 2>/dev/null || true"
            echo "Pipeline finished for branch: \${RESOLVED_BRANCH} with tag \${IMAGE_TAG} — health: host.docker.internal:3000/health"
        }
    }
}
