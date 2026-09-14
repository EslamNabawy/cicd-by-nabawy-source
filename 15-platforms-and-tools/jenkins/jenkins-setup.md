---
title: Jenkins Setup
category: platforms
status: complete
difficulty: beginner
prerequisites:
  - Jenkins Architecture
related:
  - Jenkins Agents
  - Jenkins Plugins
---

<!-- icon: jenkins -->
# Jenkins Setup

> Run Jenkins the reproducible way: a pinned Docker image with a persistent volume — never an untracked WAR on someone's laptop.

## 1. Recommended Install (Docker)

Picking up from **[Jenkins Architecture](jenkins-architecture.md)**, where the controller–agent topology was defined — we now run it: one container, one volume, one socket.

```bash
docker volume create jenkins_home
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:2.516-lts-jdk17
docker logs jenkins 2>&1 | grep -A2 "initialAdminPassword"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8080` → paste the admin password → **Install suggested plugins** → create admin user.

## 2. Alternatives

| Method | When |
|--------|------|
| `jenkins/jenkins:lts` Docker image | Default: local dev, training, labs |
| OS package (`apt`/`yum`) | Long-lived on-prem server |
| Kubernetes (Helm chart) | Production with ephemeral agents |
| Bare `jenkins.war` | Only for debugging — hard to reproduce |

## 3. Windows vs WSL2: Where to Run Jenkins

- **Yes, Jenkins runs natively on Windows:** Windows installer (`jenkins.msi`) or `java -jar jenkins.war` with a supported JDK (17 or 21). Works fine as controller or as a Windows build agent (needed for .NET / MSBuild / PowerShell workloads).
- **Prefer Docker Desktop (WSL2 backend) on a Windows dev machine:** same `docker run` command from §1 works in PowerShell or WSL2, keeps paths/line-endings Linux-normal, and matches CI. This is the default recommendation for this KB.
- **Prefer WSL2 Ubuntu when:** pipelines assume `sh`, `make`, `docker`, or Linux-only tooling; you want `apt` packages and case-sensitive paths without Cygwin/Git-Bash quirks.
- **Keep a Windows agent when:** you must build Windows artifacts — run controller in Docker/WSL2, attach a Windows agent via inbound (WebSocket) agent, label it `windows`, and constrain those jobs with `agent { label 'windows' }`.
- **Pitfalls on native Windows:** `bat` vs `sh` steps (use `bat` for `.bat`/PowerShell steps, `sh` only on Linux agents); Git auto-CRLF breaking shell scripts; `C:\` vs `/var/jenkins_home` path mapping into containers; Windows firewall blocking ports 8080/50000.

## 4. First Pipeline Job (Smoke Test)

1. New Item → **Pipeline** → name it `hello`.
2. Definition: *Pipeline script*, enter:

```groovy
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps { echo 'Jenkins is alive' }
        }
    }
}
```

3. Build Now → green ball = controller + executors + workspace all work.

<!-- icon: terminal -->
## 5. Run & Use: Step by Step

### Step 1 — Run the controller

```bash
docker volume create jenkins_home
docker run -d --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:2.516-lts-jdk17
```

### Step 2 — Unlock

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Open `http://localhost:8080`, paste the password, click **Install suggested plugins**, create the admin user.

### Step 3 — Lock the controller out of builds

*Manage Jenkins → Nodes → Built-In Node → Configure → # of executors: 0 → Save.* Builds must never run on the controller.

### Step 4 — Connect an agent

*Manage Jenkins → Nodes → New Node* → name `linux-1`, type *Permanent Agent* → labels `linux docker`, executors `2`, launch method per your network (SSH or inbound). Confirm it shows **in sync / idle** under *Build Executor Status*.

### Step 5 — Create the pipeline

New Item → **Multibranch Pipeline** → name `acme-shop` → Branch Source: your repo URL + credentials → Save. Jenkins scans, finds the `Jenkinsfile` (see [jenkins-pipelines.md](jenkins-pipelines.md)), and builds each branch.

### Step 6 — Trigger on push

Repo → *Settings → Webhooks → Add* → Payload URL `http://<jenkins-host>:8080/github-webhook/`, events *push + pull requests* (see [jenkins-webhooks.md](jenkins-webhooks.md)). Push a commit → build starts in seconds.

### Step 7 — Verify the loop

Green build → image in registry → staging deployed → approve → production. Break something on purpose, watch the pipeline go red, read the console log, fix, push green again (see [jenkins-troubleshooting.md](jenkins-troubleshooting.md)).

## 6. Production Hardening Checklist

- [ ] Controller executors = 0; builds run on agents only.
- [ ] `JENKINS_HOME` on persistent, backed-up storage (test restore!).
- [ ] Pin image/plugin versions; upgrade deliberately, never auto-update prod plugins blindly.
- [ ] Reverse proxy (TLS) + authentication matrix from day one (see [jenkins-security.md](jenkins-security.md)).

## 7. Failure Modes

- Data lost on container recreate → volume wasn't mounted; `JENKINS_HOME` must be persistent.
- Stuck on Unlock screen → read the password from `secrets/initialAdminPassword` inside the container, not the host.
- Port 50000 blocked → inbound agents can't connect; open it or use WebSocket agents.

## 8. Interview Notes

- Why zero executors on the controller — what breaks when builds run where scheduling and secrets live.
- What `JENKINS_HOME` must persist across a container recreate, and what is safe to lose (workspaces).
- Webhook vs polling triggers; which port inbound agents need and why WebSocket agents exist.

## Related Topics

- [Jenkins Architecture](jenkins-architecture.md)
- [Jenkins Pipelines](jenkins-pipelines.md)

Server running and first job green — now write real pipelines. Continue in **[Jenkins Pipelines](jenkins-pipelines.md)**.
