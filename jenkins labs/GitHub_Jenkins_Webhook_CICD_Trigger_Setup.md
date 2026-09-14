# Task: Configure GitHub Webhook to Automatically Trigger a Jenkins CI/CD Pipeline

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
