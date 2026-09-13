---
title: "Lab 07 — Jenkins Shared Library"
category: labs
status: complete
difficulty: advanced
prerequisites:
  - Lab 06
  - Jenkins Pipelines
related:
  - Jenkins Pipelines
---

<!-- icon: jenkins -->
# Lab 07 — Jenkins Shared Library

## Objective

Extract a duplicated pipeline step into a versioned shared library consumed by two pipelines — reuse without copy-paste.

## Prerequisites

- Lab 06 running; a second pipeline job; a git repo to host the library.

## Architecture

Library repo (`vars/notifySlack.groovy`-style step) → Global Pipeline Libraries → two Jenkinsfiles call the same step → one fix propagates to both.

## Setup

Create repo `pipeline-library` with `vars/standardTest.groovy`:

```groovy
def call(Map cfg = [:]) {
  sh "${cfg.cmd ?: 'npm test'}"
}
```

## Step 1 — Register the library

### Execute

Manage Jenkins → System → Global Pipeline Libraries → add `my-lib`, default version `main`, source pointing at the repo.

### Expected Result

Library listed, HEAD resolved.

### Why

Versioned libraries are dependencies: pinned, reviewed, rollback-able — unlike copy-pasted steps.

## Step 2 — Consume from two pipelines

### Execute

In both Jenkinsfiles:

```groovy
@Library('my-lib') _
pipeline {
  agent { label 'docker-agent' }
  stages { stage('Test') { steps { standardTest(cmd: 'npm test') } } }
}
```

### Expected Result

Both pipelines green, both calling the shared step.

### Why

One definition, N consumers — the DRY payoff, with the version pin as the safety rail.

## Verification

- [ ] Both pipelines call the library step.
- [ ] Breaking the library breaks both (proves sharing); reverting fixes both.
- [ ] Library change went through PR review on its own repo.

## Failure Scenarios

- `Library my-lib not found`: name mismatch or version unresolvable — check Global config + repo branch.
- Untrusted library on sandbox: approve signatures or restrict to trusted source.

## Cleanup

Keep the library repo — it is the seed of pipeline governance.

## What This Proved

Reusable pipeline code with versioning. Continue with [Lab 08](08-jenkins-backup-restore.md).
