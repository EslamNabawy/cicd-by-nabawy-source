---
title: Groovy Cheatsheet for Jenkins
category: platforms
status: complete
difficulty: beginner
prerequisites:
  - Jenkins Pipelines
related:
  - Jenkins Pipelines
  - Jenkins Troubleshooting (sandbox approvals)
---

# Groovy Cheatsheet (Jenkins Subset)

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
