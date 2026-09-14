---
title: Jenkins Credentials
category: platforms
status: complete
difficulty: intermediate
prerequisites:
  - Jenkins Pipelines
related:
  - Jenkins Security
---

<!-- icon: security -->
# Jenkins Credentials

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
