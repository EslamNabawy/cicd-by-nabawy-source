---
title: Jenkins Agents
category: platforms
status: complete
difficulty: intermediate
prerequisites:
  - Jenkins Architecture
  - Jenkins Pipelines
related:
  - Jenkins Security
---

<!-- icon: server -->
# Jenkins Agents

> Agents are Jenkins's word for runners: machines offering **executors** to the controller, selected by **labels**. Prefer ephemeral agents that live only for one build.

## 1. Types

Picking up from the **[Groovy Cheatsheet](jenkins-groovy-cheatsheet.md)** — pipelines written, language in hand — we now provision the machines that execute them: agents, labels, executors.

| Type | Lifecycle | Best for |
|------|-----------|----------|
| Permanent (SSH/inbound) | Long-lived VM | Special hardware, Windows/GPU builders |
| Docker cloud | Container per build, destroyed after | Default Linux builds — clean env every time |
| Kubernetes cloud | Pod per build | Elastic, bursty CI on existing clusters |

## 2. Labels & Executors

```groovy
agent { label 'linux && docker' }   // must have BOTH labels
agent { docker { image 'node:20' } } // ephemeral container on any Docker agent
agent none                           // top-level: each stage picks its own agent
```

- **Label:** capability tag (`linux`, `windows`, `gpu`, `docker`) matched by `agent { label ... }`.
- **Executor:** one build slot; a 4-core agent typically offers 2–4 executors.

## 3. Minimal Docker-Agent Pipeline

```groovy
pipeline {
    agent { docker { image 'maven:3.9-eclipse-temurin-17' } }
    stages {
        stage('Build') { steps { sh 'mvn -B package' } }
    }
}
```

Each run gets a pristine container — "works on my machine" dies here.

## 4. Connection Methods

- **Inbound (agent → controller):** agent initiates via WebSocket/JNLP; survives NAT, needs port 50000 or WebSocket endpoint.
- **SSH (controller → agent):** controller SSHes in; simple on flat networks, needs credential + open port 22.

## 5. Failure Modes

- Label typo (`lable 'linx'`) → build waits forever in queue; check *Build Executor Status*.
- Stale permanent agents (tool drift) → flaky builds; prefer ephemeral or reimage regularly.
- Too many executors per CPU → builds starve each other; ~1 executor per 1–2 cores.

## 6. Interview Notes

- Inbound vs SSH connection: which side initiates, and which survives NAT without opening inbound ports.
- Why ephemeral agents beat permanent ones for reproducibility — what "tool drift" does to flaky-build rates.
- Label expressions vs executor counts: what a build stuck in queue almost always means.

Agents run the work — next they need secrets. Continue in **[Jenkins Credentials](jenkins-credentials.md)**.

## Related Topics

- [Jenkins Architecture](jenkins-architecture.md)
- [Jenkins Pipelines](jenkins-pipelines.md)
