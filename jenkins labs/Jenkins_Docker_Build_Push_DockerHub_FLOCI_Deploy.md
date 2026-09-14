# Task: Jenkins CI/CD Pipeline — Build, Tag, and Push a Docker Image to Docker Hub (with Simulated AWS Deployment via FLOCI)

## Objective
Build a Jenkins pipeline that pulls source code from a Git repository, builds a Docker image from it, authenticates to Docker Hub using credentials stored in Jenkins, tags the image with a build-specific tag, pushes it to Docker Hub, and (per the extended version of this workflow) deploys/runs the resulting application inside a simulated AWS environment (FLOCI) rather than a real cloud target.

## Goal
By the end of this task, the environment should have:
1. A Git repository containing `hello.py`, `requirements.txt`, a `Dockerfile`, and a `Jenkinsfile`.
2. A Jenkins pipeline that: pulls the code → builds a Docker image → logs in to Docker Hub using stored Jenkins credentials → tags the image (`myusername/app:build-<BUILD_NUMBER>`) → pushes it to Docker Hub.
3. (Extended flow) The pipeline additionally runs an authentication step, an image-tagging step keyed to the Jenkins build number, and an application-deployment step that runs the app inside FLOCI's simulated AWS infrastructure.

## Architecture Overview (from diagrams)

### Core build-and-push flow (Image 2)
```
Git Source Repository            Jenkins CI/CD Pipeline Orchestrator                    Docker Hub Registry
(e.g., GitHub)                   -----------------------------------------------------  --------------------
hello.py                         Pull Code (git clone [repo_url])
requirements.txt      --git      Build Setup (tool configure: docker, build-env)
Dockerfile             clone-->  Docker Build (docker build -t app:local)
Jenkinsfile                      Login & Tag (docker login using fetched creds;
                                              docker tag app:local myusername/app:build-123)
                                  Docker Push (docker push myusername/app:build-123)  --upload-->  User Repositories
                                                                                                    Image Tiers
Jenkins Credentials Store  --fetch Docker Hub credentials-->  (feeds into Login & Tag step)
```

### Extended flow with numbered stages and simulated deployment (Image 3)
```
GitHub Repository [Repo Name]      Jenkins CI/CD Server                  Simulated AWS Environment (using FLOCI)
------------------------------    ------------------------------------  -----------------------------------------
hello.py                          1. Environment Setup (Load Env)        FLOCI AWS Infrastructure Simulation
requirements.txt      --trigger   2. Code Checkout (Retrieve Repo)        Provider: aws -> floci simulation
Dockerfile             (webhook)  3. Docker Build (v${BUILD_NUMBER})
Jenkinsfile           -------->   4. Authentication (Login to Registry)
                                   5. Image Tagging (Apply Build Tag)
                                   6. Image Push (to Registry)     ------------------->  (chip/container icon)
                                   7. Application Deployment (Run App)                    running hello.py
```

## Prerequisites
- A Git repository (e.g. on GitHub) containing `hello.py`, `requirements.txt`, a `Dockerfile`, and a `Jenkinsfile`.
- A running Jenkins server with Docker available to the Jenkins agent (Docker CLI/daemon accessible from wherever the pipeline executes).
- A Docker Hub account to push images to.
- Access to FLOCI (or equivalent AWS simulation environment) if the deployment stage is in scope.

## Step 0: Pre-Flight Check — Verify Tools, Credentials, and Data Before Executing Anything
Do this entire section before Step 1, so the pipeline can be built end-to-end without stalling mid-setup.

### 0.1 Check tools/environment
- Jenkins reachable: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` (or check the relevant service/container).
- Docker available on the Jenkins agent/host: `docker --version` and confirm the Jenkins user/agent can actually run `docker` commands (e.g. is in the `docker` group, or the Jenkins Docker plugin is configured).
- Git available: `git --version`.
- Confirm the Jenkins **Docker Pipeline plugin** (or equivalent) and **Credentials Binding plugin** are installed (**Manage Jenkins → Plugins**), since the pipeline needs to both run `docker` commands and pull credentials securely.

### 0.2 Check credentials and account data
- Whether Docker Hub credentials already exist in Jenkins (**Manage Jenkins → Credentials**) — look for a credential ID intended for Docker Hub login before creating a duplicate.
- If none exist: a Docker Hub username and a Docker Hub access token (preferred over the account password — Docker Hub supports generating scoped access tokens under **Account Settings → Security → New Access Token**).
- Whether FLOCI access details (endpoint, credentials, or simulation config) are already documented, if the deployment stage (Image 3, step 7) is in scope.

### 0.3 Check existing repo/config state
- Whether the target repo already contains `hello.py`, `requirements.txt`, `Dockerfile`, and `Jenkinsfile`, or whether these need to be created.
- Whether a Jenkins pipeline job already exists for this project.
- What Docker Hub repository name/namespace (`myusername/app` or otherwise) the images should be pushed to, and whether that Docker Hub repo already exists (Docker Hub will auto-create it on first push if the account allows, but confirm expected visibility — public vs private).
- Whether the GitHub webhook trigger for this repo is already configured (see the companion webhook setup task file if not).

### 0.4 Ask the user for anything missing — before proceeding
Compile everything unresolved after the checks above into one batch, asked upfront:
- Docker Hub username and access token, if no valid Jenkins credential for Docker Hub already exists.
- The Docker Hub image name/namespace to push to (e.g. `myusername/app`) and desired tagging convention (the diagrams use `build-${BUILD_NUMBER}`).
- Whether the Application Deployment stage (running the app inside FLOCI) is in scope for this run, or whether the task should stop after the Docker Push stage.
- If deployment is in scope: the FLOCI provider/connection details needed to run a container/app inside the simulation.
- The Git repository URL/branch, if not already known.

Only proceed to Step 1 once every required input is confirmed present or supplied by the user.

## Steps

### 1. Prepare the Repository (skip/reuse pieces already present)
- Ensure the repo contains:
  - `hello.py` — the sample application.
  - `requirements.txt` — Python dependencies.
  - `Dockerfile` — build instructions for the image.
  - `Jenkinsfile` — pipeline definition (built in Step 2).
- Commit and push any missing pieces.

### 2. Add Docker Hub Credentials to Jenkins (skip if already present, per Step 0.2)
- In Jenkins, go to **Manage Jenkins → Credentials**.
- Add a credential of type **Username with password**:
  - **Username**: Docker Hub username.
  - **Password**: Docker Hub access token (not the account password).
  - **ID**: a descriptive ID, e.g. `dockerhub-creds`.

### 3. Write the Jenkinsfile (Declarative Pipeline)
Structure the pipeline stages to match the numbered flow in Image 3:
```groovy
pipeline {
    agent any
    environment {
        IMAGE_NAME = "myusername/app"
        IMAGE_TAG  = "build-${env.BUILD_NUMBER}"
    }
    stages {
        stage('Environment Setup') {
            steps {
                echo 'Loading environment/config...'
            }
        }
        stage('Code Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Docker Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:local ."
            }
        }
        stage('Authentication') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                   usernameVariable: 'DOCKER_USER',
                                                   passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }
        stage('Image Tagging') {
            steps {
                sh "docker tag ${IMAGE_NAME}:local ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Image Push') {
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
        stage('Application Deployment') {
            when {
                expression { return params.DEPLOY_TO_FLOCI == true }
            }
            steps {
                // Deployment command(s) depend on FLOCI's specific interface —
                // fill in per the details gathered in Step 0.4.
                echo "Deploying ${IMAGE_NAME}:${IMAGE_TAG} into FLOCI simulation..."
            }
        }
    }
}
```
- Adjust `IMAGE_NAME` to the namespace confirmed in Step 0.4.
- The `Application Deployment` stage is conditional/optional — only include and run it if Step 0.4 confirmed it's in scope.

### 4. Configure the Pipeline Job in Jenkins
- Create (or reuse, per Step 0.3) a Jenkins Pipeline job pointing at the Git repo, using "Pipeline script from SCM" so it reads the `Jenkinsfile` directly from the repo.
- Set up the GitHub webhook trigger (see the companion webhook setup task file for full webhook steps) so pushes to the repo trigger this pipeline automatically.

### 5. Run and Validate End-to-End
- Trigger the pipeline (via webhook push or manually).
- Confirm each stage completes: Environment Setup → Code Checkout → Docker Build → Authentication → Image Tagging → Image Push.
- Confirm on Docker Hub that the new image tag (`myusername/app:build-<N>`) appears under the expected repository.
- If deployment is in scope, confirm FLOCI reflects the running/deployed application.
- Push a second commit and confirm the pipeline runs again automatically with an incremented `BUILD_NUMBER` tag.

## Notes for the AI Agent Executing This Task
- **Never hardcode the Docker Hub password/token directly in the Jenkinsfile** — always reference it via the Jenkins credentials store (`withCredentials`), as shown above.
- Prefer a Docker Hub **access token** over the account password for the stored credential — tokens can be scoped and revoked independently of the account login.
- If the Jenkins agent runs Docker-in-Docker or via a mounted socket, confirm the specific setup already in use on this machine (`docker info`) rather than assuming a particular Docker execution model.
- The **Application Deployment** stage is FLOCI-specific and not a standard Docker/AWS deployment target — get the actual FLOCI interface/command needed from the user in Step 0.4 rather than guessing at deployment syntax.
- If this task is combined with the companion GitHub webhook setup task or the Terraform/FLOCI provisioning task, do Step 0 pre-flight checks jointly rather than duplicating them across files.
