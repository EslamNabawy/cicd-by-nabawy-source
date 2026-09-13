---
title: Jenkins Webhooks and Triggers
category: platforms
status: complete
difficulty: intermediate
prerequisites:
  - Jenkins Pipelines
  - Git, Branching & Pull Requests (generic triggers)
related:
  - Jenkins Plugins
---

<!-- icon: webhook -->
# Jenkins Webhooks & Triggers

> Webhooks are Jenkins's CI triggers: GitHub notifies Jenkins on push/PR, and Jenkins builds exactly that ref. Polling is the fallback, never the plan.

## 1. Trigger Options

Picking up from **[Jenkins Plugins](jenkins-plugins.md)**, which delivered the GitHub Branch Source plugin — we now wire it: webhooks that turn pushes into builds.

| Method | Latency | Load | Verdict |
|--------|---------|------|---------|
| Webhook (GitHub → Jenkins) | Seconds | Minimal | Default |
| Multibranch scan + webhook | Seconds | Minimal | Default for PRs |
| SCM polling (`H/5 * * * *`) | Minutes | Wasted polls | Fallback / air-gapped |
| Scheduled (`cron`) | — | — | Nightly, releases |
| Manual / upstream trigger | — | — | Promotions, chains |

## 2. GitHub Webhook Setup

1. Jenkins job: enable **GitHub hook trigger for GITScm polling** (or use a Multibranch/Organization job).
2. GitHub repo → *Settings → Webhooks → Add*: Payload URL `https://jenkins.acme.io/github-webhook/`, content type `application/json`, events *push + pull requests*.
3. Push a commit → *GitHub Hook Log* in Jenkins shows delivery; build starts in seconds.

For private networks, the controller needs a reachable URL (reverse proxy / ngrok for labs).

## 3. Multibranch = PR Gates Done Right

A Multibranch Pipeline scans the repo, creates a sub-job per branch/PR with a Jenkinsfile, and reports status back to GitHub checks. Branch disappears → job auto-removed. This replaces hand-maintained per-branch jobs entirely.

## 4. Failure Modes

- Webhook 403/404 → wrong URL (`/github-webhook/` trailing slash matters) or missing GitHub plugin.
- Builds not triggering → webhook received but job's trigger checkbox off; check *GitHub Hook Log*.
- Duplicate builds (webhook + polling both on) → disable polling once webhooks work.
- Secret mismatch → validate webhook secrets so anyone can't trigger builds with curl.

## Related Topics

- [Git, Branching & Pull Requests](../../01-source-control/git-branching-pull-requests.md) (generic triggers)
- [Jenkins Pipelines](jenkins-pipelines.md)

Triggers fire — but open triggers are an attack surface. Continue in **[Jenkins Security](jenkins-security.md)**, where authentication, authorization, and agent trust lock this down.
