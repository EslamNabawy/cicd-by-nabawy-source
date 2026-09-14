---
title: Rollback & Recovery
category: reliability
status: complete
difficulty: intermediate
prerequisites:
  - Deployment Strategies
  - Observability & Feedback
related:
  - Deployment Strategies
  - Observability & Feedback
---

<!-- icon: monitoring -->
# Rollback & Recovery

> Rollback is a feature, not an apology: a practiced, boring path from bad production back to good — decided by signals, executed in minutes, reviewed afterward.

## 1. What Is It?

Picking up from **[CI/CD Security](../11-security/cicd-security.md)**, where defenses were hardened — defenses still fail, so recovery must be engineered with the same rigor as release.

## 2. Rollback per Strategy

| Strategy | Rollback move | Time |
|----------|--------------|------|
| Rolling | Roll back batch by batch (or `rollout undo`) | Minutes |
| Blue/Green | Flip router back to Blue | Seconds |
| Canary | Drain canary, 100% to stable | Seconds–minutes |
| Feature flag | Toggle off | Instant |
| Recreate | Redeploy previous digest | Slowest — avoid where recovery matters |

Rollback deploys a **previous known-good digest** ([Artifact Management](../05-artifacts-and-packaging/artifact-management.md)) — never a fresh build. Fresh builds during incidents add untested variables to a fire.

## 3. Rollback vs Forward-Fix Decision

- **Rollback when:** cause unknown, blast radius growing, error budget burning fast, or the fix is uncertain. Default for Sev1.
- **Forward-fix when:** cause known, fix tiny and verified, rollback itself risky (migrations already applied — data can't "roll back," only migrate forward).
- **Decider:** on-call with pre-agreed thresholds, not a committee. Decide in minutes; review in the postmortem.

## 4. Recovery Drills (MTTR Practice)

- Game days: inject failure in staging (kill pods, expire certs, break the pipeline), time the recovery, fix the gaps found.
- Rollback rehearsal: each service rolls back on staging quarterly until MTTR is measured, not guessed.
- Jenkins/server recovery: restore `JENKINS_HOME` backup to fresh infra, replay smoke pipeline (see [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md)).

## 5. Postmortems That Prevent Recurrence

Blameless, owner-assigned, pipeline-linked: every action item becomes a test, check, alert, or runbook — or it will recur. Track repeat-incident rate; a postmortem without a merged pipeline change is a diary entry.

## 6. Failure Modes

- No practiced rollback → improvisation during incidents; rehearse until boring.
- Rolling forward into a migration → data corruption; expand-contract migrations make both directions safe.
- Rollback untested because "we never need it" → the one time it's needed, it doesn't work. Test the path you pray you never take.

## 7. Interview Notes

- Rollback vs forward-fix: decision criteria in 60 seconds.
- Why rollback uses old digests, never fresh builds.
- Design a game day for a canary-deployed service.

## Related Topics

- [Deployment Strategies](../10-deployment-strategies/deployment-strategies.md)
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Observability & Feedback](../13-observability-and-feedback/observability-feedback.md)
- [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md)

Recovery engineered — the library's concept arc is complete. Return to the **[Topic Index](../TOPIC_INDEX.md)** for labs and reference.
