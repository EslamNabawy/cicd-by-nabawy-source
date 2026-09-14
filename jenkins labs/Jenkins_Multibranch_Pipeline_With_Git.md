# Task: Set Up a Jenkins Multibranch Pipeline Using Git

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
