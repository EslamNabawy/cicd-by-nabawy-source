---
title: Jenkins Advanced
category: platforms
status: complete
difficulty: advanced
prerequisites:
  - Jenkins Pipelines
  - Jenkins Agents
  - Jenkins Security
related:
  - Jenkins Troubleshooting
  - Jenkins Credentials
---

<!-- icon: jenkins -->
# Jenkins Advanced

> Beyond single-team pipelines: shared libraries for reuse at scale, parallel/matrix execution, Configuration-as-Code for reproducible controllers, backup/restore, and safe administration via the Script Console.

## 1. Shared Libraries (Don't Repeat Yourself)

Picking up from **[Jenkins Security](jenkins-security.md)**, where trust boundaries were drawn — shared libraries run outside the sandbox, so that trust model is exactly what governs them.

A Shared Library is versioned Groovy code (its own repo) imported by many Jenkinsfiles — the Jenkins answer to copy-pasted pipeline logic.

```groovy
// Jenkinsfile: one line replaces 60 lines of boilerplate
@Library('acme-pipeline-lib@1.4') _
standardServicePipeline(app: 'shop', deployEnv: 'staging')
```

```groovy
// vars/standardServicePipeline.groovy in the library repo
def call(Map cfg) {
    pipeline {
        agent { label 'linux' }
        stages {
            stage('Build') { steps { sh 'npm ci && npm run build' } }
            stage('Test')  { steps { sh 'npm test' } }
            stage('Image') { steps { sh "docker build -t registry/${cfg.app}:$GIT_COMMIT ." } }
        }
    }
}
```

- Version the library (`@1.4`, never `@main`) — a breaking lib change must not detonate every pipeline at once.
- Test library code with [JenkinsPipelineUnit](https://github.com/jenkinsci/JenkinsPipelineUnit) before tagging.
- Trust boundary: libraries run outside the sandbox — only admins approve library repos.

## 2. Parallel & Matrix Execution

```groovy
stage('Verify') {
    parallel {
        stage('Unit')       { steps { sh 'npm run test:unit' } }
        stage('Lint')       { steps { sh 'npm run lint' } }
        stage('Secret scan') { steps { sh 'gitleaks detect --no-git' } }
    }
}
```

```groovy
// Matrix: same stages × N axes (JDK versions, browsers, regions)
matrix {
    axes { axis { name 'JDK'; values '17', '21' } }
    stages { stage('Build') { steps { sh "./mvnw -Djava.version=${JDK} package" } } }
}
```

Rule: parallelize independent verification (unit/lint/scan), never dependent deploys. Each parallel branch needs a free executor — size agent pools for peak fan-out, not average load.

## 3. Configuration as Code (JCasC)

Controllers defined in YAML, versioned in Git, applied on boot — rebuild a controller from scratch in minutes.

```yaml
# jenkins.yaml (values redacted; secrets via Vault/credentials store, never plaintext)
jenkins:
  numExecutors: 0
  clouds:
    - docker:
        name: docker-cloud
        dockerApi: { dockerHost: { uri: "unix:///var/run/docker.sock" } }
        templates:
          - labelString: linux
            dockerTemplateBase: { image: "jenkins/agent:jdk17" }
credentials:
  system:
    domainCredentials:
      - credentials:
          - string:
              id: registry-token
              secret: "${REGISTRY_TOKEN}"   # env, resolved at boot
```

- Boot order: base image (pinned) + `plugins.txt` (pinned) + `jenkins.yaml` → identical controller every time.
- Drift rule: UI changes are ephemeral — if it isn't in YAML, it doesn't exist after the next rebuild.

## 4. Backup & Restore

Back up `JENKINS_HOME` **excluding** `workspace/` and `builds/` archives you can afford to lose (or keep history — Jenkins fingerprints hash-link each artifact to the exact builds that produced and consumed it, so audit trails survive):

```bash
tar --exclude='workspace*' --exclude='builds/*/archive*' \
  -czf jenkins-backup-$(date +%F).tgz /var/jenkins_home
```

- Must restore: `jobs/*/config.xml`, `credentials.xml` + `secrets/`, global `config.xml`, `jenkins.yaml`, `plugins/`.
- Test restores quarterly: spin a staging controller from backup + replay the smoke pipeline. An untested backup is a rumor.
- Off-site + encrypted; credentials in the backup decrypt the kingdom — treat backup storage as production-secret scope.

## 5. Script Console Administration

*Manage Jenkins → Script Console* runs Groovy as admin on the controller — the escape hatch for bulk operations:

```groovy
// Bulk-wipe build history older than 30 days (one-off hygiene)
Jenkins.instance.items.each { job ->
    job.builds.findAll { it.timeInMillis < System.currentTimeMillis() - 30L*86400000 }
       .each { it.delete() }
}
```

- Audit every execution (who ran what, when); prefer versioned maintenance jobs over ad-hoc console runs for anything repeated.
- Never paste console snippets from the internet without reading them — they run as full admin.

## 6. Queue & Performance Tuning

| Symptom | Lever |
|---------|-------|
| Builds queue despite idle CPUs | More executors per agent (≤ ~1 per 1–2 cores) or more agents |
| Controller UI slow | Executors=0 on controller, heap (JVM memory) ≥ 4 GB via `-Xmx4g`, SSD for `JENKINS_HOME`, discard old builds aggressively |
| Thundering herd at 09:00 | Stagger cron (`H 9 * * *` not `0 9 * * *`), concurrency limits, quiet periods (a delay that batches rapid commits into one build) on busy multibranch jobs |
| Plugin startup bloat | Remove unused plugins; each adds startup time + conflict surface |

### Production Topology

- **Controller:** active-passive pair (one live, one warm standby from the same `jenkins.yaml` + backup); `JENKINS_HOME` on replicated storage (NFS/EBS snapshots). Stateless agents mean failover loses only in-flight builds, which retry.
- **Agent fleets per team/env:** separate clouds (or namespaces) for `team-a`, `team-b`, `prod-deploy` — noisy neighbors and credential scopes stay isolated; labels route automatically.
- **Network zones:** controller in private subnet behind TLS reverse proxy; agents outbound-only (inbound WebSocket) so no ingress holes; webhook relay for GitHub → private controller.
- **DR drill:** quarterly — restore backup to a fresh region/account, replay smoke pipeline, measure RTO against the SLO. Untested DR is documentation fiction.

## 7. Interview Notes

- Design a shared-library rollout: versioning, testing, trust, migration path for 50 repos.
- Rebuild-a-controller drill: image + plugins + JCasC + secrets + backup — in what order, what breaks first.
- Parallel vs matrix vs sequential: which for unit/lint/scan, for JDK matrix, for staging→prod promotion.

## Related Topics

- [Jenkins Pipelines](jenkins-pipelines.md)
- [Jenkins Agents](jenkins-agents.md)
- [Jenkins Security](jenkins-security.md)
- [Jenkins Troubleshooting](jenkins-troubleshooting.md)

Advanced patterns banked — when they break, diagnose in order. Continue in **[Jenkins Troubleshooting](jenkins-troubleshooting.md)**.
