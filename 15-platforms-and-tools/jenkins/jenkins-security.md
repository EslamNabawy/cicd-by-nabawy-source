---
title: Jenkins Security
category: platforms
status: complete
difficulty: advanced
prerequisites:
  - Jenkins Credentials
  - Jenkins Architecture
related:
  - Jenkins Credentials
  - Jenkins Agents
---

<!-- icon: security -->
# Jenkins Security

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
