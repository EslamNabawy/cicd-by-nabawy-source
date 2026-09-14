---
title: Jenkins Troubleshooting
category: platforms
status: complete
difficulty: intermediate
prerequisites:
  - Jenkins Pipelines
  - Jenkins Agents
related:
  - Jenkins Plugins
  - Jenkins Security
---

<!-- icon: troubleshooting -->
# Jenkins Troubleshooting

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
