---
title: Jenkins Plugins
category: platforms
status: complete
difficulty: beginner
prerequisites:
  - Jenkins Setup
related:
  - Jenkins Pipelines
  - Jenkins Webhooks
---

<!-- icon: plugin -->
# Jenkins Plugins

> Plugins are how Jenkins grows: Git integration, Docker agents, Blue Ocean UI, credentials bindings — nearly every capability beyond the core is a plugin.

## 1. Essential Plugin Set

Picking up from **[Jenkins Credentials](jenkins-credentials.md)** — whose bindings are themselves a plugin — we now survey the plugin ecosystem that makes Jenkins Jenkins.

| Plugin | Why |
|--------|-----|
| Pipeline (workflow-*) | Declarative/Scripted pipelines, `stage`/`steps` |
| Git + GitHub / GitLab Branch Source | Checkout, multibranch discovery, webhooks |
| Credentials + Credentials Binding | Secret storage + `withCredentials` |
| Docker / Kubernetes | Ephemeral build agents |
| JUnit / Warnings NG | Test reports, static-analysis gates |
| Blue Ocean (optional) | Readable pipeline visualization |

## 2. Management Rules

- Pin versions in production; upgrade in a staging Jenkins first — plugin updates, not Jenkins core, cause most outages.
- Install via UI (*Manage Jenkins → Plugins*) for learning; via `plugins.txt` / Configuration-as-Code for anything reproducible:

```text
# plugins.txt (pinned, version-controlled)
git:5.2.1
workflow-aggregator:596.v8c21c963d92d
credentials-binding:681.v346b_f30f5d80
docker-workflow:572.v950f58993843
junit:1300.v07d6c232e1c3
```

- Remove unused plugins — each one is attack surface + startup time + a future version conflict.

## 3. Failure Modes

- Update-all-plugins Friday → Monday outage; update deliberately with a rollback snapshot.
- Missing plugin step error (`No such DSL method 'docker'`) → the owning plugin isn't installed.
- Core/plugin version skew → cryptic startup failures; keep LTS core + compatible plugin set.

## 4. Interview Notes

- Pinning vs update-all: why `plugins.txt` with versions beats UI installs for reproducible controllers.
- `No such DSL method` — which layer is actually missing and how you prove it.
- Core/plugin skew: why LTS core + compatible set matters more than latest-everything.

## Related Topics

- [Jenkins Setup](jenkins-setup.md)
- [Jenkins Troubleshooting](jenkins-troubleshooting.md)

Plugins installed — now connect the trigger wire. Continue in **[Jenkins Webhooks](jenkins-webhooks.md)**, where pushes become builds in seconds.
