---
title: Jenkins_Labs_Handbook
status: complete
merged_from:
  - jenkins labs/GitHub_Jenkins_Webhook_CICD_Trigger_Setup.md
  - jenkins labs/Jenkins_Docker_Build_Push_DockerHub_FLOCI_Deploy.md
  - jenkins labs/Jenkins_Multibranch_Pipeline_With_Git.md
  - jenkins labs/Jenkins_Shared_Library_Example_with_GitHub.md
  - jenkins labs/Terraform_Jenkins_FLOCI_CICD_Pipeline.md
---

# Jenkins_Labs_Handbook

> Merged handbook. Sources: jenkins labs/GitHub_Jenkins_Webhook_CICD_Trigger_Setup.md, jenkins labs/Jenkins_Docker_Build_Push_DockerHub_FLOCI_Deploy.md, jenkins labs/Jenkins_Multibranch_Pipeline_With_Git.md, jenkins labs/Jenkins_Shared_Library_Example_with_GitHub.md, jenkins labs/Terraform_Jenkins_FLOCI_CICD_Pipeline.md.


---

<!-- merged-part-1-from: jenkins labs/GitHub_Jenkins_Webhook_CICD_Trigger_Setup.md -->

## Part 1: Task: Configure GitHub Webhook to Automatically Trigger a Jenkins CI/CD Pipeline

## Objective
Set up a Jenkins pipeline that checks out code from a (private) GitHub repository using authenticated Git access, and configure a GitHub webhook so that every `git push` to the repository automatically triggers the Jenkins pipeline build — with no manual intervention.

## Goal
By the end of this task, the environment should have:
1. A Jenkins pipeline job that successfully checks out a specific branch of a GitHub repo using stored credentials.
2. A GitHub webhook pointing at the Jenkins server.
3. Jenkins configured to react to that webhook (GitHub hook trigger for GITScm polling).
4. Confirmation that a new commit to the repo automatically starts a new Jenkins build.

## Prerequisites
- A GitHub account with a repository to use (can be private).
- A running Jenkins server, reachable from GitHub (if Jenkins is local/behind NAT or in WSL, it must be reachable via a public URL, tunnel, or the GitHub webhook target must be able to reach it — see Notes at the end).
- Basic Jenkins job creation permissions.

## Step 0: Pre-Flight Check — Verify Tools, Credentials, and Data Before Executing Anything
Do this entire section **before** starting Step 1. Gather every dependency and piece of input data up front so the task can run start-to-finish without stalling partway through to ask for something (especially important here, since webhook delivery and reachability issues are hard to debug mid-flow).

### 0.1 Check tools/environment
- Jenkins reachable: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` (or `systemctl status jenkins`, or check the relevant container/process).
- GitHub CLI available (optional, useful for repo/webhook checks): `gh --version`. Not required — if absent, fall back to the GitHub web UI steps and note this to the user rather than silently installing it.
- GitHub CLI authenticated, if present: `gh auth status`.
- If Jenkins is only reachable on `localhost`/inside WSL: check whether a tunneling tool is already installed and running (e.g. `ngrok --version`, or check for an active `ngrok`/reverse-proxy process) — a public URL is required for GitHub to deliver webhooks.

### 0.2 Check credentials and account data
- Whether a usable, non-expired GitHub Personal Access Token (PAT) with `repo` scope already exists (GitHub → **Settings → Developer settings → Personal access tokens**). PAT creation cannot be scripted/automated — it requires the user acting in a browser — so this must be resolved in this pre-flight step, not mid-task.
- Whether matching Jenkins credentials already exist (**Manage Jenkins → Credentials**) for this GitHub account/repo.
- Jenkins admin access confirmed (can reach job configuration and **Manage Jenkins → Credentials**).

### 0.3 Check existing repo/config state
- Whether a Jenkins job already exists for this pipeline (browse the Jenkins dashboard, or query the Jenkins API).
- Whether a webhook already exists on the target GitHub repo (**Repo → Settings → Webhooks**) pointing at the right Jenkins URL.
- The repository's actual default branch name (`main`, `master`, or other) — get this from the repo itself rather than assuming.
- Whether Jenkins is publicly reachable already, or needs a tunnel set up (see 0.1).

### 0.4 Ask the user for anything missing — before proceeding
Compile a single list of everything genuinely missing or ambiguous after the checks above (don't re-ask about things already confirmed present), then ask it all **in one batch** before Step 1. Typical items:
- The target GitHub repository (name/URL) and its branch, if not already known.
- A GitHub Personal Access Token — if none valid exists, ask the user to generate one (Settings → Developer settings → Personal access tokens → Generate new token (classic), `repo` scope) and paste it in, since this step cannot be done non-interactively.
- The Jenkins base URL to use, and confirmation of how it should be exposed publicly if it's only on `localhost`/WSL (e.g. "should I set up an ngrok tunnel, or do you already have a public URL/reverse proxy for Jenkins?").
- Desired job name, if different from the example.

Only proceed to Step 1 once every required input is either confirmed present on the machine or supplied by the user — this avoids stopping mid-setup (e.g. after creating the Jenkins job) to ask for a token or a tunnel decision.


## Steps

### 1. Create or Reuse a Basic Pipeline Job in Jenkins
- Check whether a suitable pipeline job already exists; if so, reuse it and skip to Step 2.
- Otherwise, in Jenkins, click **New Item**, choose **Pipeline**, and name it (e.g. `github-webhook-pipeline`).
- Under the **Pipeline** section, choose **Pipeline script**, and paste in a minimal sample pipeline script (any simple placeholder script, e.g. one that just echoes a message) to confirm the job runs successfully first.
- Save and run the job once to confirm it completes successfully before adding GitHub integration.

### 2. Get the GitHub Repository URL
- Go to the target GitHub repository.
- Copy the repository's clone URL (HTTPS form), e.g. `https://github.com/<username>/<repo>.git`.

### 3. Confirm the GitHub Personal Access Token (PAT) for Authentication
- This should already be resolved in Step 0.4 (either an existing valid token was found, or the user supplied one). Do not attempt to generate a token programmatically here — proceed straight to using the token already in hand.

### 4. Add or Reuse GitHub Credentials in Jenkins
- Check **Manage Jenkins → Credentials** for an existing credential tied to this GitHub account/repo; if one exists and is valid, select it and skip credential creation below.
- Otherwise, in the Jenkins job configuration, use **Pipeline Syntax** (the "Pipeline Syntax" link/generator available in the pipeline job config page).
- Select the **checkout: Check out from version control** sample step.
- Set **SCM** to **Git**.
- Paste the GitHub repository URL into **Repository URL**.
- Under **Credentials**, click **Add → Jenkins**, and create credentials of type **Username with password**:
  - **Username**: the GitHub username confirmed in Step 0.
  - **Password**: the Personal Access Token confirmed/supplied in Step 0.4 (NOT the actual GitHub account password).
  - **ID**: a descriptive ID, e.g. `github-token`.
  - Click **Add** to save the credential.
- Select the credential from the dropdown.
- Set the **Branch to build** field to the branch name confirmed in Step 0.3.
- Click **Generate Pipeline Script** to produce the equivalent `checkout` Groovy snippet.
- Copy the generated snippet and paste it into the pipeline script, replacing the placeholder sample code from Step 1.
- Save the job and run it to confirm the checkout succeeds and pulls the repository into the Jenkins workspace.

### 5. Configure or Verify the Webhook on the GitHub Side
- Check the repo's **Settings → Webhooks** for an existing webhook pointing at this Jenkins instance's `/github-webhook/` endpoint. If one exists, confirm it shows a green checkmark (successful delivery) and skip to Step 6.
- Otherwise, click **Add webhook**.
- Set the **Payload URL** to the Jenkins GitHub webhook endpoint:
  ```
  http://<your-jenkins-url>/github-webhook/
  ```
  (Note the trailing slash — it matters.)
- Set **Content type** as appropriate (typically `application/json`).
- Leave trigger events at the default (`push` events) unless a different trigger scope is needed.
- Save the webhook.
- Confirm GitHub shows a green checkmark next to the newly created webhook, indicating a successful initial ping/delivery.

### 6. Configure or Verify the Trigger on the Jenkins Side
- In the Jenkins job configuration, under **Build Triggers**, check whether **GitHub hook trigger for GITScm polling** is already enabled.
- If not, enable it and save the job configuration.

### 7. Test the End-to-End Automatic Trigger
- Make a small change in the GitHub repository (e.g. edit `index.html` or any tracked file).
- Commit and push the change to the branch configured in Step 4.
- Confirm in the Jenkins job's build history that a **new build starts automatically** shortly after the push, without manually clicking "Build Now."
- Check the console output of the new automatic build to confirm the checkout step pulled the latest commit.

## Notes for the AI Agent Executing This Task
- **Resolve everything in Step 0 before starting** — token generation, tunnel setup decisions, and branch/repo confirmation should never come up as a surprise after work has already begun (e.g. after a job or webhook has been half-configured).
- **Never store the raw GitHub password as a Jenkins credential** — always use a Personal Access Token in place of the password, as GitHub has deprecated basic password authentication for Git operations.
- **Local/WSL reachability**: GitHub's webhook delivery requires it to reach the Jenkins URL over the internet. If Jenkins is running only on `localhost` inside WSL or behind a home network/NAT, a tunneling tool (e.g. `ngrok`, `localhost.run`, or a reverse proxy with a public domain) will be needed to expose Jenkins publicly so GitHub's webhook can deliver events. This decision belongs in Step 0, not after the webhook is already being configured.
- Double-check the branch name matches the repository's actual default branch (`main` vs `master` vs others) — a mismatch will cause checkout failures.
- If the webhook delivery fails, GitHub's webhook settings page shows delivery attempts and response codes under **Recent Deliveries** — use that for debugging connectivity/auth issues.


---

<!-- merged-part-2-from: jenkins labs/Jenkins_Docker_Build_Push_DockerHub_FLOCI_Deploy.md -->

## Part 2: Task: Jenkins CI/CD Pipeline — Build, Tag, and Push a Docker Image to Docker Hub (with Simulated AWS Deployment via FLOCI)

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


---

<!-- merged-part-3-from: jenkins labs/Jenkins_Multibranch_Pipeline_With_Git.md -->

## Part 3: Task: Set Up a Jenkins Multibranch Pipeline Using Git

## Objective
Configure a Jenkins **Multibranch Pipeline** job that automatically discovers branches in a Git repository and builds each one using a `Jenkinsfile` committed to that branch — eliminating the need to manually create a separate Jenkins pipeline job per branch. The repository will use a fixed three-branch model — **`main`**, **`dev`**, and **`stg`** — all built by the same job, with per-branch pipeline behavior demonstrated via `when` conditionals.

## Goal
By the end of this task, the environment should have:
1. A Jenkins **Multibranch Pipeline** job connected to a Git repository (plain Git branch source — not GitHub-specific integration).
2. Automatic branch scanning that creates a sub-job (folder item) for each matching branch, driven by a `Jenkinsfile` present in that branch.
3. A repository with exactly three branches — **`main`**, **`dev`**, and **`stg`** — all included/built by the Multibranch Pipeline job (no exclusion filter needed since all three are wanted).
4. A `Jenkinsfile` with a conditional (`when`) stage that only runs on the `stg` branch (or another branch-specific variation, per your convention), demonstrating per-branch pipeline behavior from a single shared file.
5. Confirmation that deleting a branch upstream causes Jenkins to remove ("orphan") the corresponding job after a rescan.

## Key Concept
A Multibranch Pipeline job is, structurally, **a folder of individual pipeline jobs** — one per discovered branch. Jenkins scans the repository, finds branches matching the configured filter, and for each one looks for a `Jenkinsfile` (by default) to build with. Branches without a `Jenkinsfile` are skipped/reported as such in the scan log. Individual branch jobs (e.g. `main`, `dev`, `stg`) cannot be configured directly — only the parent Multibranch Pipeline job's configuration controls behavior for all branches.

## Prerequisites
- A running Jenkins server with the **Git** and **Multibranch Pipeline** (Pipeline: Multibranch) plugins installed.
- A Git repository (can be hosted anywhere reachable via a plain `https://` or `git://` clone URL — this task deliberately uses the plain Git branch source, not the GitHub-specific integration, even if the repo happens to be hosted on GitHub).
- Local Git command-line access to the repository, with push permissions.
- No webhook/inbound connectivity is assumed in this task (e.g. an air-gapped or firewalled Jenkins) — branch discovery is done via periodic/manual scans instead of webhook-triggered scans. If webhooks are available in this environment, that can be layered on separately (see the companion GitHub webhook setup task file).

## Step 0: Pre-Flight Check — Verify Tools, Credentials, and Data Before Executing Anything
Do this entire section before Step 1, so the job can be built end-to-end without stalling mid-setup.

### 0.1 Check tools/environment
- Jenkins reachable: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` (or check the relevant service/container).
- Git available: `git --version`.
- Confirm the **Git plugin** and **Pipeline: Multibranch** plugin (and **Pipeline: Basic Steps**) are installed in Jenkins (**Manage Jenkins → Plugins**).
- Confirm whether Jenkins has outbound-only or fully air-gapped network access — this determines whether periodic scanning (rather than webhook-triggered scanning) is the right approach for this task.

### 0.2 Check credentials and account data
- Whether the target Git repository is public or private.
  - If public: no Jenkins credentials are needed for the branch source.
  - If private: check **Manage Jenkins → Credentials** for an existing usable Git credential (SSH key or username/token) before creating a new one.
- Confirm local Git push access is already authenticated (e.g. `git ls-remote <repo-url>` succeeds, or an SSH key / stored credential helper is already configured) — this is needed to push new branches and Jenkinsfile changes during the task.

### 0.3 Check existing repo/config state
- Whether the target repository already has `main`, `dev`, and `stg` branches, or whether any of them still need to be created.
- Whether a `Jenkinsfile` already exists on any of those branches.
- Whether a Multibranch Pipeline job with a similar name already exists in Jenkins.
- What the repository's default branch is named (`main`, `master`, etc.) — confirm rather than assume.

### 0.4 Ask the user for anything missing — before proceeding
Compile everything unresolved after the checks above into one batch, asked upfront:
- The Git repository URL to use, and whether it's public or private.
- If private: the credential (SSH key, or username + token/password) to store in Jenkins for this branch source.
- The desired name for the Multibranch Pipeline job (the original tutorial names it identically to the repository name for clarity).
- Confirmation that the branch set should be exactly `main`, `dev`, `stg` (create any that don't already exist).
- What per-branch behavior is wanted in the `Jenkinsfile` (e.g. should `stg` run extra verification steps, should `dev` behave differently from `main`, etc.) — this task defaults to a single extra stage that only runs on `stg`, but adjust if a different convention is wanted.
- Confirmation of which "Additional Behaviors" to enable under the Git branch source (this task defaults to: **Check out to matching local branch**, **Clean before checkout**, **Clean after checkout**) — adjust if different behavior is wanted.

Only proceed to Step 1 once every required input is confirmed present or supplied by the user.

## Steps

### 1. Create the Multibranch Pipeline Job in Jenkins (skip/reuse if one already exists, per Step 0.3)
- In Jenkins, click **New Item**.
- Name the job to match the repository name (for clarity of mapping between repo and job).
- Select **Multibranch Pipeline**, then click **OK**.

### 2. Add a Git Branch Source
- Under **Branch Sources**, click **Add source → Git** (not the GitHub-specific source — this task uses the generic Git source even if the repo happens to be hosted on GitHub).
- **Project Repository**: paste the repository's clone URL (HTTPS, or SSH if using key-based auth).
- **Credentials**: leave as **None** if the repo is public; otherwise select/add the credential confirmed in Step 0.4.
- Leave other branch source defaults as-is for the initial setup.

### 3. Configure Branch Filtering (Include All Three Target Branches)
- Still in the job configuration, under the Git branch source's **Behaviors**, add **Filter by name (with wildcards)**.
- Set:
  - **Include**: `main dev stg` (space-separated exact names — no wildcard needed since all three are known, fixed branch names)
  - **Exclude**: (leave blank — anything not in the include list is automatically excluded)
- Add these additional behaviors:
  - **Check out to matching local branch** — ensures the build checks out the actual branch HEAD rather than a detached commit.
  - **Clean before checkout**
  - **Clean after checkout**
- Leave **Build strategies** and other sections at their defaults unless a specific need arises.

### 4. Save and Observe the Initial Scan
- Click **Save**. This triggers an automatic scan of the repository.
- Check the scan log (**Scan Multibranch Pipeline Log** in the job's left nav): it will report which branches were found and whether a `Jenkinsfile` was present on each.
- At this point, if no `Jenkinsfile` exists yet on any branch, the job folder will show as empty ("Jenkinsfile not found").

### 5. Add a Jenkinsfile to the Repository
- Locally, on the default branch, create a `Jenkinsfile` with a minimal pipeline, e.g.:
```groovy
pipeline {
    agent { label 'linux' }
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }
    stages {
        stage('Hello') {
            steps {
                echo 'hello'
            }
        }
    }
}
```
- Commit and push the `Jenkinsfile` to the default branch.

### 6. Trigger a Rescan (No Webhooks in This Setup)
- Since this task assumes no inbound webhook connectivity, Jenkins will not automatically know about the new commit.
- Manually trigger a scan: go to the Multibranch Pipeline job and click **Scan Multibranch Pipeline Now**.
- Confirm in the scan log that the default branch now shows **Jenkinsfile found**, and that a build was automatically triggered for it.
- Optionally, under the job's periodic scan configuration, set a scan interval (e.g. every few minutes) so this happens automatically without manual triggering, appropriate for air-gapped/no-webhook environments.

### 7. Create the `dev` and `stg` Branches
- Locally, create the two additional branches from the default branch (skip creating any that already exist, per Step 0.3):
  - `dev`
  - `stg`
- Push both branches to the remote repository.
- Trigger another manual scan (or wait for the periodic scan).
- Confirm the scan log reports all three branches (`main`, `dev`, `stg`) were found and each shows **Jenkinsfile found** (since they were branched from a commit that already has the `Jenkinsfile`), and that all three now appear as buildable jobs in the Multibranch Pipeline folder.

### 8. Add Branch-Specific Pipeline Behavior
- On the `stg` branch, modify the `Jenkinsfile` to add a stage that only runs on `stg`, e.g.:
```groovy
stage('Staging Verification (stg only)') {
    when {
        expression { return env.BRANCH_NAME == 'stg' }
    }
    steps {
        sh 'cat README.md'
    }
}
```
- Also make an unrelated content change (e.g. edit `README.md`) to have something visible to confirm per-branch checkout behavior.
- Commit both changes on `stg` and push.
- Trigger a scan/build for `stg` and confirm:
  - The build checks out the `stg` branch specifically (visible in the build log as a branch checkout, not a detached commit checkout).
  - The new "Staging Verification" stage runs and prints the branch's `README.md` content.
- Run the `main` and `dev` branch jobs again and confirm the "Staging Verification" stage does **not** run on either (the `when` condition correctly restricts it to `stg` only).

### 9. Merge Changes Back to Main and Observe Orphan Cleanup (Optional)
- Locally, check out the default branch, merge in the changes from `stg` (Jenkinsfile + README changes) if that fits your workflow — this repo does not use pull requests in this workflow, matching a lightweight GitHub-flow-like approach.
- Push the updated default branch.
- If at any point a branch (e.g. an older test branch) is deleted both locally and on the remote, trigger a rescan and confirm the scan log reports it as an **orphaned item** and removes its job from the Multibranch Pipeline folder — while `main`, `dev`, and `stg` remain intact as the three tracked branches.
- Run the `main` branch job once more and confirm:
  - It now includes the merged-in "Staging Verification" stage definition, but the stage is **skipped** (shown as skipped due to the `when` conditional, since `main` isn't `stg`).

## Notes for the AI Agent Executing This Task
- **This task intentionally avoids GitHub-specific Jenkins integration** — use the plain **Git** branch source, even though the example repository may be hosted on GitHub. A separate, GitHub-specific version of this workflow (with webhook-driven scanning) is a distinct follow-on task, not this one.
- **No webhook is configured here on purpose** — this setup simulates an air-gapped/no-inbound-access Jenkins environment, so branch discovery relies on manual or periodic scans rather than push-triggered scans. Don't add a webhook as part of this task unless the user explicitly asks for it.
- Individual branch jobs inside a Multibranch Pipeline folder (e.g. `main`, `dev`, `stg`) are **not directly configurable** — all behavior (branch filtering, checkout behavior, scan triggers) is controlled from the parent Multibranch Pipeline job's configuration only.
- The `env.BRANCH_NAME` variable is what allows a single shared `Jenkinsfile` to behave differently per branch via `when` conditionals — this is the core mechanism that avoids needing a separate Jenkinsfile per branch.
- Orphaned branch cleanup only happens **after a rescan** — deleting a remote branch does not immediately remove its Jenkins job; the next scan (manual, periodic, or webhook-triggered) is what evaluates and removes orphaned items.
- If this task is combined with the companion GitHub webhook setup or Docker/Terraform pipeline tasks, do Step 0 pre-flight checks jointly rather than duplicating them across files.


---

<!-- merged-part-4-from: jenkins labs/Jenkins_Shared_Library_Example_with_GitHub.md -->

## Part 4: Task: Set Up a Jenkins Shared Library Linked to a GitHub Repository

## Objective
Configure Jenkins to use a **Global Shared Library** hosted on GitHub, so that reusable Groovy logic (e.g. a UAT/approval check) can be called from both scripted and declarative Jenkins pipelines — without embedding raw Groovy logic directly inside every pipeline definition.

## Goal
By the end of this task, the environment should have:
1. A Jenkins instance with a configured Global Pipeline Library pointing at a GitHub repo.
2. A test pipeline (both a scripted-style and a declarative-style version) that imports a class from that shared library and uses it to conditionally run build steps based on whether an `approved.txt` file exists in a `tools/` folder.

## Prerequisites
- Jenkins reachable (e.g. `http://localhost:8080`), running on the local machine or inside WSL.
- A GitHub account and a GitHub repository to act as the shared library (e.g. named `jenkins-shared-library`).
- Git available locally / in WSL.
- Admin access to Jenkins (Manage Jenkins permissions).

## Step 0: Pre-Flight Check — Verify Tools, Credentials, and Data Before Executing Anything
Do this entire section **before** starting Step 1. The goal is to gather every dependency and piece of input data up front, so the task can run start-to-finish without stopping partway through to ask for something.

### 0.1 Check tools/environment
- Jenkins reachable: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` (or check the relevant port/service, e.g. `systemctl status jenkins`, or check if a Jenkins process/container is active).
- Git available: `git --version`.
- GitHub CLI available (optional but useful for repo checks/creation): `gh --version`. If missing, it is NOT required — fall back to manual GitHub web steps, but note this to the user rather than silently installing it.
- GitHub CLI authenticated, if `gh` is present: `gh auth status`.

### 0.2 Check credentials and account data
- GitHub account username to use for the shared library repo.
- Whether Jenkins needs to reach the GitHub repo privately (private repo) or the repo is public. If private, a Jenkins credential (GitHub username + Personal Access Token) will be needed — check **Manage Jenkins → Credentials** for an existing usable one before assuming none exists.
- Jenkins admin login/access confirmed (can reach **Manage Jenkins → Configure System**).

### 0.3 Check existing repo/config state
- Whether a `jenkins-shared-library` (or similarly named) GitHub repo already exists under the user's account (`gh repo list` if available, or `git ls-remote <candidate-url>`).
- Whether a Global Pipeline Library is already registered in Jenkins (**Manage Jenkins → Configure System → Global Pipeline Libraries**).
- Whether a pipeline job with a similar name already exists in Jenkins.

### 0.4 Ask the user for anything missing — before proceeding
Compile a single list of everything that is genuinely missing or ambiguous after the checks above (do not ask about things already confirmed present). Typical items that may need to be asked in one batch, upfront:
- The GitHub username/account to use, if not inferable from `gh auth status` or existing config.
- Whether the shared library repo should be created new, or an existing repo name/URL should be reused.
- Whether the repo will be public or private (this determines whether a Jenkins credential/PAT is needed at all).
- If private: a GitHub Personal Access Token, OR explicit permission to generate one interactively (token generation itself requires the user in a browser — see Notes).
- Jenkins base URL, if not `http://localhost:8080`.
- Desired names for: the shared library (Jenkins), the pipeline job(s), and the Groovy package/class if different from the example (`com.<yourname>.UatInput`).

Ask all of this **at once**, before Step 1, so the run isn't interrupted midway. Only proceed to Step 1 once every required input is either confirmed present on the machine or supplied by the user.


## Repository Structure Required for the Shared Library
The shared library repo must follow Jenkins' expected layout:
```
(root)
 └── src/
      └── com/
           └── <yourname>/
                └── UatInput.groovy
```
Example `UatInput.groovy` class logic:
- Define a class (e.g. `UatInput`) with a method `buildIsUatApproved()`.
- That method should check whether a file named `tools/approved.txt` exists in the workspace.
  - If it exists → return `true`.
  - If it doesn't exist (or is named/considered "not approved") → return `false`.

## Steps

### 1. Create the Shared Library Repository on GitHub (skip if it already exists)
- If a suitable repository doesn't already exist, create a new GitHub repository (e.g. `jenkins-shared-library`).
- Check whether `src/com/<yourname>/UatInput.groovy` already exists in that repo; if not, add it with the class described above.
- Commit and push to the `master` (or `main`) branch.
- Copy the repository's clone URL — it will be needed in Jenkins configuration.

### 2. Register the Shared Library in Jenkins (skip if already registered)
- In Jenkins, go to **Manage Jenkins → Configure System**.
- Scroll down to the **Global Pipeline Libraries** section.
- If a library already points at this repo with a usable name, note its name and skip to Step 3.
- Otherwise, click **Add**.
- Fill in:
  - **Name**: a short identifier, e.g. `shared-library` (this exact name is referenced later in pipeline code).
  - **Default version**: the branch to pull from, e.g. `master`.
  - **Retrieval method**: Modern SCM.
  - **Source Code Management**: GitHub.
  - **Project Repository**: paste the GitHub repo URL from Step 1.
- Click **Validate** to confirm the connection works.
- Remove/ignore any unnecessary optional fields (credentials aren't required if the repo is public).
- Click **Apply**, then **Save**.

### 3. Create a Test Pipeline Job (skip creation if one already exists)
- Check Jenkins for an existing pipeline job intended for this test; if one exists and is configured similarly, reuse it instead of creating a new one.
- Otherwise, create a **New Item → Pipeline** project (e.g. named `shared-library-test-pipeline`).
- In the **Pipeline** section of the job configuration:
  - Check whether "Use Groovy Sandbox" is already unchecked; if not, **uncheck it** — this avoids sandbox restrictions when calling shared library classes.

### 4. Write a Scripted Pipeline That Uses the Shared Library
In the Pipeline script box, use syntax equivalent to:
```groovy
@Library('shared-library') _
import com.<yourname>.UatInput

def uatInput = new UatInput()
println "Build is UAT approved: ${uatInput.buildIsUatApproved()}"
```
- `@Library('shared-library')` must match the exact name given in Step 2.
- The import path must match the package/folder structure of the Groovy file (`com/<yourname>/UatInput.groovy` → `com.<yourname>.UatInput`).
- Save and run the build.
- Verify in the **Console Output** that it prints `true` when `tools/approved.txt` exists in the workspace, and `false` when it does not.

### 5. Extend to a Declarative Pipeline
Replace the scripted script with a declarative pipeline that uses the shared library class inside a `when` condition, e.g.:
```groovy
@Library('shared-library') _
import com.<yourname>.UatInput

def uatInput = new UatInput()

pipeline {
    agent any
    stages {
        stage('Run only if approval exists') {
            when {
                expression { return uatInput.buildIsUatApproved() }
            }
            steps {
                echo 'The build has been approved.'
                // Add real build steps here (Maven, Docker, ant, etc.)
            }
        }
    }
}
```
- Save and run the build.
- Confirm the stage executes (and echoes output) only when `tools/approved.txt` exists.
- Remove or rename the file, re-run the build, and confirm the stage is skipped (no output from inside the `when` block) without failing the build.

### 6. Validate End-to-End
- Test with the approval file present → confirm `true` / stage runs.
- Test with the approval file absent or renamed → confirm `false` / stage is skipped.
- Confirm no changes to the shared library repo are needed to reuse this pattern in other pipelines — only the `@Library` declaration and import.

## Notes for the AI Agent Executing This Task
- **Do all discovery and questions in Step 0** — don't ask the user for input mid-task (e.g. after already starting to create a repo). Batch every open question into one round of clarification before Step 1 begins.
- If Jenkins is running inside WSL or accessed from Windows via `localhost`, ensure the correct port (default `8080`) is exposed/forwarded.
- If the shared library GitHub repo is private, a Jenkins credential (username + GitHub Personal Access Token) will need to be created and selected in the Global Pipeline Library configuration (see the companion webhook task file for how to generate a GitHub PAT). Generating a new PAT requires the user to act in a browser (GitHub does not expose PAT creation via API/CLI for security reasons) — if one doesn't already exist, ask the user to generate it and provide it rather than attempting to script around this.
- Groovy Sandbox must be disabled for this simple example; for production use, consider approving specific method signatures via **In-process Script Approval** instead of fully disabling the sandbox.


---

<!-- merged-part-5-from: jenkins labs/Terraform_Jenkins_FLOCI_CICD_Pipeline.md -->

## Part 5: Task: CI/CD Pipeline for Terraform Infrastructure Provisioning via Jenkins into a Simulated AWS Environment (FLOCI)

## Objective
Build a Jenkins pipeline that is triggered by a GitHub webhook, runs a full Terraform workflow (init → workspace select → plan → manual approve/abort → apply) against infrastructure-as-code stored in a GitHub repo, and provisions the resulting infrastructure into **FLOCI**, a simulated AWS environment — rather than a real AWS account. This is intended as a safe sandbox for practicing Terraform + Jenkins CI/CD without incurring real cloud costs or risk.

## Goal
By the end of this task, the environment should have:
1. A GitHub repository containing Terraform code (`VPC.tf`, `Variables.tf`, `Provider.tf`), environment-specific var files (`dev`, `stg.tfvars`, `Prod`), and a `Jenkinsfile` defining the pipeline.
2. A Jenkins pipeline, triggered by a GitHub webhook, with stages: **Checkout → Terraform Init → Workspace Select → Plan (with manual Approve/Abort gate) → Apply → Post (Success/Fail → Mail)**.
3. The pipeline's `Provider.tf` configured so the Terraform CLI executes against **FLOCI** (an AWS API simulation environment) instead of real AWS, creating simulated VPC, Subnets, EC2, and S3 Bucket resources.

## Architecture Overview (from diagram)
```
GitHub Repository                Jenkins CI/CD Server                              FLOCI (AWS Simulation Env)
------------------              --------------------------------------            ---------------------------
VPC.tf                          Pipeline
Variables.tf                      - Stage: Checkout
Provider.tf                       - Terraform Execution
dev                                   - Stage: Terraform Init (terraform init)
stg.tfvars           --CI/CD-->      - Stage: Workspace Select (workspace)   --Executes & Calls-->  Terraform CLI --Simulated AWS API--> Simulated VPC
Prod                  Trigger            - Stage: Plan (plan)                    Provider                              (+ Simulated Subnets,
Jenkinsfile           (Webhook)              -> Approve                                                                 Simulated EC2,
                                              -> Abort                                                                  Simulated S3 Bucket)
                                       - Stage: Apply (apply)
                                   - Stage: Post
                                       -> Success
                                       -> Fail -> Mail
                                                                                  Provider.tf (defines FLOCI as the
                                                                                   Terraform provider endpoint)
```

## Prerequisites
- A GitHub repository to hold the Terraform code and Jenkinsfile.
- A running Jenkins server with the **Terraform** and **Pipeline** plugins available (and Git/GitHub plugins for checkout + webhook triggering).
- Terraform CLI installed wherever the Jenkins agent executes the pipeline.
- Access to FLOCI (or equivalent AWS simulation environment) with whatever endpoint/credentials it requires in place of real AWS credentials.
- An SMTP/mail configuration in Jenkins if the "Fail → Mail" post-action is desired.

## Step 0: Pre-Flight Check — Verify Tools, Credentials, and Data Before Executing Anything
Do this entire section before Step 1, so the pipeline can be built end-to-end without stopping partway through to ask for something.

### 0.1 Check tools/environment
- Jenkins reachable: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080` (or check the relevant service/container).
- Terraform CLI installed on the Jenkins agent/host: `terraform -version`.
- Git available: `git --version`.
- Confirm the Jenkins **Terraform plugin** (or equivalent CLI wrapper approach) and **Pipeline** plugin are installed (**Manage Jenkins → Plugins**).
- Confirm Jenkins **Mailer plugin** (or equivalent) is installed/configured if a "Fail → Mail" step is wanted.

### 0.2 Check credentials and account data
- Whether FLOCI access details (endpoint URL, API key/token, or whatever FLOCI requires to be addressed as a Terraform provider target) already exist or are documented. FLOCI is a simulation tool, not real AWS, so standard AWS credential docs won't apply — the specific FLOCI setup instructions are needed here.
- Whether a Jenkins credential already exists for FLOCI/simulated-provider access (**Manage Jenkins → Credentials**).
- Whether GitHub credentials/webhook access are already configured (see the companion webhook setup task file if not).
- Mail server credentials/SMTP relay details, if the mail-on-failure step is in scope.

### 0.3 Check existing repo/config state
- Whether the target GitHub repo already contains `VPC.tf`, `Variables.tf`, `Provider.tf`, environment var files, and a `Jenkinsfile`, or whether these need to be created from scratch.
- Whether a Jenkins pipeline job already exists for this project.
- Whether Terraform workspaces (`dev`, `stg`, `prod`) already exist in the target backend, or need to be created (`terraform workspace list`).
- What Terraform state backend is in use (local state vs. remote backend) — this affects how `terraform init` behaves and whether extra backend credentials are needed.

### 0.4 Ask the user for anything missing — before proceeding
Compile everything unresolved after the checks above into one batch of questions, asked upfront:
- How to configure `Provider.tf` to target FLOCI specifically — what endpoint, credentials, or provider block format FLOCI expects in place of a real `aws` provider block. (This is the single most important unknown — without it the "Apply" stage cannot actually target the simulation.)
- Which environments/workspaces to set up (`dev`, `stg`, `prod`) and their corresponding `.tfvars` file names/contents.
- Whether the manual Plan Approve/Abort gate should use Jenkins' `input` step (pausing the pipeline for a human), and who should be notified/authorized to approve it.
- Mail recipient(s) for the "Fail → Mail" post-action, if wanted.
- The GitHub repo URL/branch, if not already known from a prior task.

Only proceed to Step 1 once every required input is either confirmed present or supplied by the user.

## Steps

### 1. Prepare the GitHub Repository (skip/reuse pieces already present)
- Ensure the repo contains:
  - `VPC.tf` — VPC resource definitions.
  - `Variables.tf` — input variable declarations.
  - `Provider.tf` — provider block configured to target FLOCI's simulated AWS API (per Step 0.4 answer).
  - Environment var files: `dev` (dir or `.tfvars`), `stg.tfvars`, `Prod` (dir or `.tfvars`) — one per environment/workspace.
  - A `Jenkinsfile` at the repo root defining the pipeline (built in Step 2).
- Commit and push any missing pieces.

### 2. Write the Jenkinsfile (Declarative Pipeline)
Structure the pipeline stages to match the diagram:
```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Terraform Init') {
            steps {
                sh 'terraform init'
            }
        }
        stage('Workspace Select') {
            steps {
                sh 'terraform workspace select ${ENV_NAME} || terraform workspace new ${ENV_NAME}'
            }
        }
        stage('Plan') {
            steps {
                sh 'terraform plan -var-file=${TFVARS_FILE} -out=tfplan'
            }
        }
        stage('Approve') {
            steps {
                input message: 'Apply this Terraform plan?', ok: 'Approve'
            }
        }
        stage('Apply') {
            steps {
                sh 'terraform apply -auto-approve tfplan'
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded.'
        }
        failure {
            mail to: '<recipient-from-step-0.4>',
                 subject: "Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Check console output at ${env.BUILD_URL}"
        }
    }
}
```
- Replace `${ENV_NAME}` and `${TFVARS_FILE}` with actual parameters or a parameterized build (e.g. a Jenkins `choice` parameter for `dev`/`stg`/`prod`).
- The `input` step is what implements the "Approve / Abort" branch from the diagram — declining the prompt aborts the pipeline before `apply` runs.

### 3. Configure the Pipeline Job in Jenkins
- Create (or reuse, per Step 0.3) a Jenkins Pipeline job pointing at the GitHub repo, using "Pipeline script from SCM" so it reads the `Jenkinsfile` directly from the repo.
- Set up the GitHub webhook trigger (see the companion webhook setup task file for full webhook steps) so pushes to the repo trigger this pipeline automatically.

### 4. Configure `Provider.tf` to Target FLOCI
- Set the Terraform provider block to point at FLOCI's simulated AWS API per the details gathered in Step 0.4, instead of a real AWS account/region/credentials.
- Confirm `terraform init` succeeds against this provider configuration.

### 5. Run and Validate End-to-End
- Trigger the pipeline (via webhook push or manually).
- Confirm each stage completes: Checkout → Init → Workspace Select → Plan.
- Confirm the pipeline pauses at the Approve/Abort gate and waits for manual input.
- Approve the plan and confirm Apply runs successfully.
- Confirm FLOCI reflects the simulated VPC, Subnets, EC2, and S3 Bucket resources described in the Terraform code.
- Test the Abort path: reject the plan and confirm Apply does not run and the pipeline stops cleanly.
- Introduce a deliberate failure (e.g. invalid Terraform syntax) and confirm the "Fail → Mail" post-action sends a notification.

## Notes for the AI Agent Executing This Task
- **FLOCI specifics are the main unknown** — this is not a standard AWS provider setup, so don't assume real AWS credential patterns (IAM roles, `~/.aws/credentials`, etc.) apply. Get the actual FLOCI provider configuration format from the user in Step 0.4 rather than guessing.
- The Approve/Abort gate is a manual human checkpoint by design — do not attempt to auto-approve it unless explicitly instructed, since its purpose is to prevent unreviewed infrastructure changes from being applied.
- Keep Terraform state per-environment isolated (via workspaces or separate state files) so that a `dev` apply cannot accidentally affect `stg`/`prod` state.
- If this task is combined with the companion GitHub webhook setup task, do Step 0 pre-flight checks jointly rather than duplicating them.
