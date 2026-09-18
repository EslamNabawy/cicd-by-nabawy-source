---
title: Jenkins Advanced Ops
status: complete
merged_from:
  - 15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md
  - 15-platforms-and-tools/jenkins/jenkins-credentials.md
  - 15-platforms-and-tools/jenkins/jenkins-plugins.md
  - 15-platforms-and-tools/jenkins/jenkins-webhooks.md
  - 15-platforms-and-tools/jenkins/jenkins-security.md
  - 15-platforms-and-tools/jenkins/jenkins-advanced.md
  - 15-platforms-and-tools/jenkins/jenkins-troubleshooting.md
---

# Jenkins Advanced Ops

> Merged handbook. Sources: 15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md, 15-platforms-and-tools/jenkins/jenkins-credentials.md, 15-platforms-and-tools/jenkins/jenkins-plugins.md, 15-platforms-and-tools/jenkins/jenkins-webhooks.md, 15-platforms-and-tools/jenkins/jenkins-security.md, 15-platforms-and-tools/jenkins/jenkins-advanced.md, 15-platforms-and-tools/jenkins/jenkins-troubleshooting.md.


---

<!-- merged-part-1-from: 15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md -->

## Part 1: Groovy Cheatsheet (Jenkins Subset)

> Only the Groovy you need for Jenkinsfiles. Full language reference: [groovy-lang.org](https://groovy-lang.org/documentation.html).

Picking up from **[Jenkins Pipelines](jenkins-pipelines.md)**, where Declarative skeletons met Scripted power — this is the Groovy subset both run on. Next, give those pipelines somewhere to run: **[Jenkins Agents](jenkins-agents.md)**.

## Variables & Strings

```groovy
def app = 'acme-shop'                    // def: dynamic type
String tag = env.GIT_COMMIT.take(7)      // typed, first 7 chars
echo "Building ${app}:${tag}"            // GString: ${} interpolates (double quotes only)
echo 'literal $HOME, no interpolation'   // single quotes: plain string
```

## Collections

```groovy
def stages = ['build', 'test', 'scan']
stages.each { s -> echo "stage: ${s}" }  // iterate with closure
def images = stages.collect { s -> "app:${s}" }   // map → new list
def failed = results.findAll { k, v -> v != 'SUCCESS' }  // filter a map
```

## Conditionals

```groovy
if (env.BRANCH_NAME == 'main') {
    echo 'releasing'
} else if (env.CHANGE_ID) {
    echo "PR #${env.CHANGE_ID}"
} else {
    echo 'feature branch'
}
def deployEnv = env.BRANCH_NAME == 'main' ? 'prod' : 'staging'  // ternary
```

## Loops & Dynamic Stages (Scripted)

```groovy
// Generates one stage per service — impossible in pure Declarative
def services = ['api', 'web', 'worker']
node('linux') {
    services.each { svc ->
        stage("Test ${svc}") {
            sh "./test.sh ${svc}"
        }
    }
}
```

## Functions

```groovy
def notifySlack(String msg) {
    sh "curl -X POST -d '{\"text\":\"${msg}\"}' \$SLACK_URL"
}
```

## Maps (Options, Config)

```groovy
def cfg = [retries: 3, timeout: 20, notify: true]
echo cfg.retries
timeout(time: cfg.timeout, unit: 'MINUTES') { sh 'make ci' }
```

## Safe Navigation & Elvis (Null-Proof Pipelines)

```groovy
def owner = env.CHANGE_AUTHOR?.toLowerCase() ?: 'unknown'
// ?. skips the call on null; ?: falls back when null/empty
```

## Jenkinsfile Idioms

```groovy
withCredentials([string(credentialsId: 'api-token', variable: 'T')]) {
    sh 'curl -H "Authorization: Bearer $T" https://api.acme.io/health'
}
retry(3) { sh './flaky-deploy.sh' }      // retry block on failure
timeout(time: 10, unit: 'MINUTES') { sh 'make e2e' }
catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
    sh './optional-audit.sh'             // mark unstable, keep pipeline green-ish
}
```

## Sandbox Gotchas

| Code | Problem | Fix |
|------|---------|-----|
| `new File('/x').text` | Filesystem access blocked | Use `readFile` step |
| `System.getenv('X')` | Blocked | Use `env.X` |
| `.execute()` on strings | Process launch blocked | Use `sh` step |
| Static methods/imports | Often not allowlisted | *In-process Script Approval*, or restructure with steps |

Rule: if Groovy fights you, push the logic into `sh` (shell) and keep Groovy as glue — Declarative + shell covers 95% of pipelines.

## Interview Notes

- Sandbox vs Script Approval: why `new File()` dies in sandbox and which step replaces it.
- `env.X` vs `System.getenv()` — the one-line difference between working and blocked.
- When logic belongs in `sh` instead of Groovy, and what "Groovy as glue" costs you in testability.

## Related Topics

- [Jenkins Pipelines](jenkins-pipelines.md)
- [Jenkins Troubleshooting](jenkins-troubleshooting.md)


---

<!-- merged-part-2-from: 15-platforms-and-tools/jenkins/jenkins-credentials.md -->

<!-- icon: security -->
## Part 2: Jenkins Credentials

> Jenkins **credentials** are secrets with typed kinds and scoped storage, injected into builds via **bindings** — never hardcoded, never echoed.

## 1. Kinds & Scopes

Picking up from **[Jenkins Agents](jenkins-agents.md)**, where executors run untrusted build code — secrets must therefore never live in Jenkinsfiles. Enter the credentials store.

| Kind | Holds | Binding step |
|------|-------|--------------|
| Secret text | API token | `string(credentialsId: ...)` |
| Username + password | Registry login | `usernamePassword(...)` |
| SSH private key | Git/agent SSH | `sshUserPrivateKey(...)` |
| Secret file | kubeconfig, keystore | `file(...)` |
| Certificate | mTLS client cert | `certificate(...)` |

Scopes: **System** (server internals, e.g. agent SSH) vs **Global/Job** (usable in pipelines). Prefer the narrowest scope that works.

## 2. Usage (Bindings)

```groovy
stages {
    stage('Push image') {
        steps {
            withCredentials([usernamePassword(
                credentialsId: 'registry-creds',
                usernameVariable: 'U', passwordVariable: 'P')]) {
                sh 'echo "$P" | docker login registry -u "$U" --password-stdin'
            }
        }
    }
}
```

Jenkins **masks** bound variables in console output automatically.

## 3. Rules

- Create via UI (*Manage Jenkins → Credentials*) or Configuration-as-Code; rotate by replacing the entry — same ID, zero Jenkinsfile changes.
- IDs are stable references (`registry-creds`); values never appear in Jenkinsfiles, logs, or artifacts.
- `credentials()` helper also works in `environment { REG = credentials('registry-creds') }`.

## 4. Failure Modes

- Secret echoed via `sh 'echo $P'` in a non-masked context or baked into an image layer — treat any leak as compromised, rotate immediately.
- Wrong scope (System-only cred used in pipeline) → "credentials not found"; move it to Global.
- Duplicate IDs across stores → ambiguous resolution; keep IDs unique and descriptive (`github-acme-app-token`).

## 5. Interview Notes

- IDs vs values: why rotation replaces the entry without touching any Jenkinsfile.
- Masking limits — what Jenkins hides in logs vs what still leaks into image layers and artifacts.
- Scopes (System vs Global): where a "credentials not found" error almost always comes from.

Secrets stored — but who delivers all these capabilities? Continue in **[Jenkins Plugins](jenkins-plugins.md)**, where Git, Docker, and credentials bindings themselves come from.

## Related Topics

- [Jenkins Security](jenkins-security.md)
- [Jenkins Pipelines](jenkins-pipelines.md)


---

<!-- merged-part-3-from: 15-platforms-and-tools/jenkins/jenkins-plugins.md -->

<!-- icon: plugin -->
## Part 3: Jenkins Plugins

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
## Part 3: plugins.txt (pinned, version-controlled)
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


---

<!-- merged-part-4-from: 15-platforms-and-tools/jenkins/jenkins-webhooks.md -->

<!-- icon: webhook -->
## Part 4: Jenkins Webhooks & Triggers

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

## 5. Interview Notes

- Webhook vs polling: why push delivery beats minute-interval polling for PR feedback time.
- 403/404 on delivery — URL shape vs plugin vs secret, in the order you check them.
- Why duplicate builds happen when both triggers are on, and which one you disable first.

## Related Topics

- [Git, Branching & Pull Requests](../../01-source-control/git-branching-pull-requests.md) (generic triggers)
- [Jenkins Pipelines](jenkins-pipelines.md)

Triggers fire — but open triggers are an attack surface. Continue in **[Jenkins Security](jenkins-security.md)**, where authentication, authorization, and agent trust lock this down.


---

<!-- merged-part-5-from: 15-platforms-and-tools/jenkins/jenkins-security.md -->

<!-- icon: security -->
## Part 5: Jenkins Security

> Jenkins holds production credentials and runs arbitrary build code — harden authentication, authorization, and the agent channel, or one malicious PR owns the fleet.

## 1. Authentication & Authorization

Picking up from **[Jenkins Webhooks](jenkins-webhooks.md)**, where anyone-with-curl could fire builds — we now decide who may do what: authentication, authorization, and the agent trust boundary.

- **Authentication (who):** local users for labs; SSO via OIDC/SAML plugins for teams — log in with Google/GitHub/Okta instead of a Jenkins-local password — disable open signup (`Enable Sign Up` off).
- **Authorization (what):** **Matrix-based security**: Developers = Job/Build + Read; Leads = + Configure/Cancel; Admins = Overall/Administer. Start from *Logged-in users can do nothing* and grant upward.
- Audit with the **Audit Trail** plugin: who triggered, configured, or canceled what.

## 2. Agent-to-Controller Rules

Builds execute attacker-influenced code (PR contents). Defaults to distrust:

- Keep **Agent → Controller Access Control** restrictive (default deny); builds must not read controller files or other jobs' secrets.
- Prefer ephemeral agents — a compromised container dies with the build.
- Never run untrusted PR builds on permanent agents holding deploy credentials; route forks to isolated, credential-free agents.

## 3. Secrets Hygiene

- All secrets in the credentials store, injected via bindings (see [jenkins-credentials.md](jenkins-credentials.md)); `set +x` around manual `sh` handling; console masking is a backstop, not a guarantee.
- Webhook secrets validated; admin over TLS only (reverse proxy, no plain HTTP in production).
- Rotate credentials by ID replacement; revoke ex-employees' tokens with the SSO deprovisioning flow, not by memory.

## 4. Update Discipline

Jenkins CVEs cluster in plugins. Patch cadence: staging Jenkins validates LTS + plugin set → snapshot → production. Subscribe to the Jenkins security advisory feed.

## 5. Interview Notes

- Matrix authorization design for a 3-role team.
- Why PR builds are a trust boundary (agent isolation, credential scoping).
- What breaks if `JENKINS_HOME/secrets` leaks (everything — it decrypts the store).

## Related Topics

- [Jenkins Credentials](jenkins-credentials.md)
- [Jenkins Troubleshooting](jenkins-troubleshooting.md)

Hardened core — now scale the craft. Continue in **[Jenkins Advanced](jenkins-advanced.md)**: shared libraries, matrix builds, JCasC, and backup/restore.


---

<!-- merged-part-6-from: 15-platforms-and-tools/jenkins/jenkins-advanced.md -->

<!-- icon: jenkins -->
## Part 6: Jenkins Advanced

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
## Part 6: jenkins.yaml (values redacted; secrets via Vault/credentials store, never plaintext)
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


---

<!-- merged-part-7-from: 15-platforms-and-tools/jenkins/jenkins-troubleshooting.md -->

<!-- icon: troubleshooting -->
## Part 7: Jenkins Troubleshooting

> Diagnose in order: **queue → executor → workspace → log → plugin/config**. Most Jenkins mysteries are label mismatches, full disks, or a Friday plugin update.

## 1. Triage Table

Picking up from **[Jenkins Advanced](jenkins-advanced.md)**, where shared libraries, JCasC, and tuning multiplied the moving parts — this is the diagnostic order that untangles them: queue → executor → workspace → log → plugin/config.

| Symptom | Check | Fix |
|---------|-------|-----|
| Build stuck in queue | *Build Executor Status*; label exists? agents online? | Fix label typo, bring agent online, free an executor |
| `No such DSL method` | Plugin providing the step installed? | Install/pin the plugin |
| `command not found` in `sh` | Tool on that agent? PATH? | Use matching label or Docker agent with the image |
| Clone/auth failure | Credentials ID + scope + repo URL | Rebind correct Global credential; test URL |
| Webhook not firing | *GitHub Hook Log*, trigger checkbox | Fix payload URL, enable trigger, check secret |
| Controller slow/frozen | Disk (`JENKINS_HOME`), heap (JVM memory), executor hog | Discard old builds, raise heap (`-Xmx`, e.g. `-Xmx4g` in `JAVA_OPTS`), executors=0 on controller |
| Red after plugin update | Which plugin changed | Roll back plugin, restore snapshot |
| Secrets in console | Masking bypassed via interpolation | `set +x`, bindings only, rotate leaked secret |

## 2. Reading a Build Log

1. **Console Output** → first red line is usually the *effect*; scroll up for the *cause* (failing `sh` exit code, Groovy stack in Declarative errors).
2. Replay with **Replay** button (edit-and-rerun) for pipeline logic bugs — without pushing commits.
3. Workspace check: *Workspace → wipe* then rebuild distinguishes dirty-workspace flakes from real failures.

## 3. Groovy Sandbox Notes

Untrusted/edited scripts run in the **sandbox**; calls outside the allowlist need **In-process Script Approval**. Prefer allowlisted steps over approvals — each approval is future maintenance.

## 4. Recovery

- Bad config change → `JENKINS_HOME/config.xml` (or job `config.xml`) is versioned? Restore the file, reload config — no full restart needed (*Manage Jenkins → Reload Configuration*).
- Full disaster → restore `JENKINS_HOME` backup (jobs + secrets + config) to a fresh pinned image; verify by running the smoke pipeline from [setup](jenkins-setup.md).

## 5. Interview Notes

- First red line is the effect, not the cause — where you actually scroll to find a pipeline failure.
- Dirty workspace vs real failure: the one action that distinguishes them before you debug further.
- Config recovery without restart — which file you restore and which button reloads it.

## Related Topics

- [Jenkins Setup](jenkins-setup.md)
- [Jenkins Agents](jenkins-agents.md)

Jenkins domain complete — now meet the sibling implementation. Continue in **[GitHub Actions](../github-actions.md)**, which solves the same pipeline with hosted runners and YAML.
