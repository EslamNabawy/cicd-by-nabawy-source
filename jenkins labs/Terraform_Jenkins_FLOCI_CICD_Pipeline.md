# Task: CI/CD Pipeline for Terraform Infrastructure Provisioning via Jenkins into a Simulated AWS Environment (FLOCI)

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
