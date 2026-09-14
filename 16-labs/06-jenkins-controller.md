---
title: "Lab 06 — Jenkins Controller & Agent"
category: labs
status: complete
difficulty: intermediate
prerequisites:
  - Jenkins Setup
  - Jenkins Pipelines
related:
  - Jenkins Setup
  - Jenkins Pipelines
---

<!-- icon: jenkins -->
# Lab 06 — Jenkins Controller & First Pipeline

## Objective

Run a real controller + agent with Docker Compose, connect them, and execute the canonical three-stage Jenkinsfile.

## Prerequisites

- Docker; concepts: [Jenkins Setup](../15-platforms-and-tools/jenkins/jenkins-setup.md), [Jenkins Pipelines](../15-platforms-and-tools/jenkins/jenkins-pipelines.md).

## Architecture

Compose: `jenkins` (controller, port 8080, volume `jenkins_home`) + `agent` (inbound, label `docker-agent`) → Multibranch or Pipeline job → Build/Test/Deploy stages.

## Setup

```bash
mkdir jenkins-lab && cd jenkins-lab
# docker-compose.yml: jenkins/jenkins:lts + inbound agent joined with the secret from the controller UI
docker compose up -d
```

Get the admin password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`.

## Step 1 — Connect the agent

### Execute

Manage Jenkins → Nodes → create node `agent-1`, labels `docker-agent`, launch via inbound; run the agent container with the secret + controller URL. Install suggested plugins.

### Expected Result

Node page shows `agent-1` online with 2–4 executors.

### Why

Controller schedules, agents execute — this split is the whole architecture (see [Jenkins Architecture](../15-platforms-and-tools/jenkins/jenkins-architecture.md)).

## Step 2 — Run the canonical pipeline

### Execute

New Pipeline job, agent `docker-agent`, script:

```groovy
pipeline {
  agent { label 'docker-agent' }
  stages {
    stage('Build') { steps { sh 'echo build' } }
    stage('Test')  { steps { sh 'echo test' } }
    stage('Deploy'){ steps { echo 'deploy' } }
  }
}
```

### Expected Result

Stage View shows three green boxes on `agent-1`.

### Why

The minimal pipeline that proves scheduling, execution, and visualization all work.

## Verification

- [ ] Agent online, labeled, executors idle after run.
- [ ] Three green stages in Stage View.
- [ ] Controller ran zero builds (check: no executors on `master`).

## Failure Scenarios

- Agent offline: wrong secret/URL or controller unreachable — check container logs, use `http://jenkins:8080` in-Compose.
- No executors on controller is correct — never enable them in prod.

## Cleanup

`docker compose down` keeps `jenkins_home` volume; `down -v` wipes everything.

## What This Proved

Controller/agent split hands-on. Continue with [Lab 07](07-jenkins-shared-library.md).

## Interview Notes

- `down` vs `down -v`: which one wipes `jenkins_home` and why that distinction is the whole lesson.
- Zero executors on the controller — what you check to prove no build ever ran there.
