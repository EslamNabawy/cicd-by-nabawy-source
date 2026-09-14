# Task: Set Up a Jenkins Shared Library Linked to a GitHub Repository

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
