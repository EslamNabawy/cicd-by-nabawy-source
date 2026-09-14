---
title: Jenkins Domain
category: platforms
status: complete
difficulty: beginner-to-advanced
prerequisites:
  - CI/CD Pipelines
related:
  - CI/CD Pipelines
  - Artifact Management
---

<!-- icon: jenkins -->
# Jenkins

> Jenkins is an open-source automation server that *implements* CI/CD concepts: pipelines become Jenkinsfiles, runners become agents, secrets become credentials. Concepts live in [CI/CD Pipelines](../../06-ci-cd-pipelines/pipelines.md); Jenkins specifics live here.

Picking up from **[Observability & Feedback](../../13-observability-and-feedback/observability-feedback.md)**, where the loop closed — we now implement that entire loop in Jenkins, starting with the topology that runs everything.

## Concept → Jenkins Map

| Generic Concept | Jenkins Implementation | Document |
|---|---|---|
| Pipeline | Jenkins Pipeline (Declarative / Scripted) | [jenkins-pipelines.md](jenkins-pipelines.md) |
| Runner / Agent | Jenkins agent (node), executor slots | [jenkins-agents.md](jenkins-agents.md) |
| CI Trigger | Webhook, polling, multibranch scan | [jenkins-webhooks.md](jenkins-webhooks.md) |
| Secrets | Credentials store + bindings | [jenkins-credentials.md](jenkins-credentials.md) |
| Extensibility | Plugins | [jenkins-plugins.md](jenkins-plugins.md) |
| Server topology | Controller + agents | [jenkins-architecture.md](jenkins-architecture.md) |
| Hardening | Auth matrix, agent-to-controller rules | [jenkins-security.md](jenkins-security.md) |
| Installation | WAR / Docker / package | [jenkins-setup.md](jenkins-setup.md) |
| Debugging | Build logs, executor states | [jenkins-troubleshooting.md](jenkins-troubleshooting.md) |

## Why Jenkins?

- **WHAT:** open-source automation server — pipelines as code (Jenkinsfile), 1,800+ plugins, controller + agents topology. Self-hosted, free, runs anywhere.
- **WHY:** vendor-neutral, owns your data/secrets on your infra, reaches exotic targets (mainframes, air-gapped, Windows/GPU builders) SaaS runners can't, and its plugin ecosystem covers nearly every tool.
- **WITHOUT IT (manual CI or scripts on laptops):** no audit trail of who built what, secrets scattered in shell history, "release laptop" as single point of failure, no PR gates, every release depends on one person's memory.

## Reading Order

1. [Architecture](jenkins-architecture.md) → 2. [Setup](jenkins-setup.md) → 3. [Pipelines](jenkins-pipelines.md) → 4. [Groovy Cheatsheet](jenkins-groovy-cheatsheet.md) → 5. [Agents](jenkins-agents.md) → 6. [Credentials](jenkins-credentials.md) → 7. [Plugins](jenkins-plugins.md) → 8. [Webhooks](jenkins-webhooks.md) → 9. [Security](jenkins-security.md) → 10. [Advanced](jenkins-advanced.md) → 11. [Troubleshooting](jenkins-troubleshooting.md)

## The Golden Rule

If a paragraph would be true for GitHub Actions too, it belongs in the generic docs — not here. Jenkins files contain only what is *distinctively Jenkins*.

## Jenkins vs GitHub Actions

Canonical comparison lives in [GitHub Actions](../github-actions.md#9-github-actions-vs-jenkins): Actions trades control for convenience (hosted, YAML, repo-local); Jenkins trades convenience for control (self-hosted, Groovy, controller/agents).

## Interview Notes

- Controller vs agents in one sentence each — where scheduling, secrets, and execution actually live.
- The Golden Rule test: which paragraph in a Jenkins doc proves it belongs in the generic docs instead.
- Jenkins vs GitHub Actions tradeoff in one line — what you gain and what you pay for self-hosting.

Begin the implementation path in **[Jenkins Architecture](jenkins-architecture.md)** — controller, agents, and executors first, because every later doc assumes them.
