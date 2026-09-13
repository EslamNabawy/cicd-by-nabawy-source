---
title: "Lab 08 — Jenkins Backup & Restore"
category: labs
status: complete
difficulty: advanced
prerequisites:
  - Lab 06
  - Jenkins Advanced (backup section)
related:
  - Jenkins Advanced
  - Rollback & Recovery
---

<!-- icon: jenkins -->
# Lab 08 — Jenkins Backup & Restore

## Objective

Prove disaster recovery: back up `JENKINS_HOME`, destroy the controller, restore on fresh infra, replay the smoke pipeline.

## Prerequisites

- Lab 06 controller with job history; concepts: [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md) backup section.

## Architecture

Running controller → stop → archive `jenkins_home` volume → wipe → fresh controller → restore archive → verify jobs, credentials, history → run smoke pipeline.

## Setup

Note one job's last build number and one credential ID — these are what you will verify after restore.

## Step 1 — Back up

### Execute

```bash
docker compose stop jenkins
docker run --rm -v jenkins-lab_jenkins_home:/data -v "$PWD":/out alpine \
  tar czf /out/jenkins-backup.tar.gz -C /data .
docker compose start jenkins
```

### Expected Result

`jenkins-backup.tar.gz` exists, timestamped; controller restarts normally.

### Why

Offline backup = consistent snapshot; live copies risk half-written state.

## Step 2 — Destroy and restore

### Execute

```bash
docker compose down -v          # destroy EVERYTHING, including the volume
docker compose up -d            # fresh controller
docker compose stop jenkins
docker run --rm -v jenkins-lab_jenkins_home:/data -v "$PWD":/in alpine \
  tar xzf /in/jenkins-backup.tar.gz -C /data
docker compose start jenkins
```

### Expected Result

Jobs, build history, credentials, and plugins all present; recorded build number matches.

### Why

Backup untested = backup imaginary. This drill is the quarterly DR practice from the advanced doc.

## Verification

- [ ] Job list + history identical (check the recorded build number).
- [ ] Credential ID present and usable.
- [ ] Smoke pipeline (Lab 06's) runs green on the restored controller.

## Failure Scenarios

- Plugin version drift: restore on a different image tag — pin `jenkins:lts` digests for controller + backup.
- Permission errors: volume owned by wrong UID — `chown -R 1000:1000` on the volume.

## Cleanup

Store one backup off-machine; delete the rest.

## What This Proved

Recovery measured, not assumed. Labs complete — return to the [Topic Index](../TOPIC_INDEX.md).
