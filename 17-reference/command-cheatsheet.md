---
title: Command Cheatsheet
category: reference
status: complete
difficulty: beginner
prerequisites: []
related:
  - Git, Branching & Pull Requests
  - CI/CD Pipelines
---

<!-- icon: build -->
# Command Cheatsheet

> Every command used across the labs and guides, grouped by tool. Copy-paste ready; details live in the linked chapters.

## Git

```bash
git checkout -b feat/x      # short branch, merge daily
git push -u origin feat/x
gh pr create --fill         # PR with CI gate
```

See [Git, Branching & Pull Requests](../01-source-control/git-branching-pull-requests.md).

## npm / Builds

```bash
npm ci                      # lockfile-exact install (CI only)
npm test
./gradlew build             # wrapper pins toolchain
```

See [Build Systems](../03-build-systems/build-systems.md).

## Docker / GHCR

```bash
docker build -t ghcr.io/OWNER/APP:sha-SHORT .
docker push ghcr.io/OWNER/APP:sha-SHORT
docker pull ghcr.io/OWNER/APP:sha-SHORT   # same digest everywhere
```

See [Artifact Management](../05-artifacts-and-packaging/artifact-management.md).

## Jenkins (Compose lab)

```bash
docker compose up -d
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
docker compose stop jenkins          # before backup
docker compose down -v               # destroy everything
```

See [Lab 06](../16-labs/06-jenkins-controller.md), [Lab 08](../16-labs/08-jenkins-backup-restore.md).

## Jenkins backup

```bash
docker run --rm -v LAB_jenkins_home:/data -v "$PWD":/out alpine \
  tar czf /out/jenkins-backup.tar.gz -C /data .
```

See [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md).

## GitHub Actions snippets

```yaml
runs-on: ubuntu-latest
needs: build                # DAG edge
permissions: { packages: write }
environment: production     # approval gate
```

See [GitHub Actions](../15-platforms-and-tools/github-actions.md).

## Related Topics

- [Topic Index](../TOPIC_INDEX.md)
- [Glossary](../GLOSSARY.md)
