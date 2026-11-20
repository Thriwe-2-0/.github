---
name: contributing
description: "Org-wide contribution conventions: repository types, branches, commits, releases, PRs, required files, markdown standard"
date: "2026-11-20T08:55:46.000Z"
lastmod: "2026-11-20T08:55:46.000Z"
tags:
  - type/reference
  - org/thriwe
  - repo/.github
categories:
  - conventions
draft: false
slug: contributing
type: reference
preview: ""
weight: 1
---
<!-- toc:start -->
## Contents
- [Contributing](#contributing) — line 31
  - [Repository types](#repository-types) — line 35
  - [Branches](#branches) — line 48
  - [Commits](#commits) — line 60
  - [Releases](#releases) — line 72
  - [Pull requests](#pull-requests) — line 77
  - [Every repository MUST define](#every-repository-must-define) — line 88
  - [Markdown standard](#markdown-standard) — line 101
  - [Reviews](#reviews) — line 118
<!-- toc:end -->

# Contributing

> **Starter conventions** — ratify with the team and adjust as practice evolves.

## Repository types

The conventions below are shared by all repos. How a change reaches production differs by type:

| Type | Examples | Reaches production via |
|------|----------|------------------------|
| GitOps | `platform-gitops` | Cut a semver tag `vX.Y.Z`; ArgoCD syncs the **highest** tag. `main` is staging — untagged work does not deploy. |
| IaC | `infra-v2` | `plan` runs in CI via OIDC on PR; **apply is human-gated** — never automated, never by agents. |
| Container images | `platform-images` | Build + push to ECR by tag; consumed by tag/digest in GitOps values. |
| Application code | `airflow-dags` | Tagged release consumed downstream (e.g. git-sync into pods). |

Each repo states its own type and release mechanism in its `AGENTS.md` (see below).

## Branches

Never commit to `main` directly. Branch from `main`:

```
<type>/<TICKET-KEY>-<short-description>
```

- **type**: `feat` · `fix` · `infra` · `chore` · `docs`
- **TICKET-KEY**: the Jira issue key, e.g. `PRISM-123`
- example: `feat/PRISM-123-add-redis-cache`

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/) — **scope is the component**:

```
<type>(<scope>): <subject>
```

example: `fix(superset): drop QueuePool sizing keys incompatible with NullPool`

Imperative subject, under ~72 characters. Reference the ticket in the body or PR.

## Releases

Tag releases with semver `vX.Y.Z`. In GitOps repos the highest tag gates deployment, so
treat a tag as a production release: verify on `main`/staging first, then tag.

## Pull requests

1. Open against `main`.
2. Fill in the PR template.
3. At least **two approvals** before merge.
4. CI must be green.
5. **Squash-merge** to keep `main` history linear.

Enforce this with an [organization ruleset](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
(2 required approvals, linear history, no force-push to `main`) where the plan allows.

## Every repository MUST define

These cannot be defaulted from the `.github` repo — each repo owns its own:

- **`.github/CODEOWNERS`** — review routing; self-own the file so ownership changes need owner
  review. Start from [`templates/CODEOWNERS`](templates/CODEOWNERS).
- **`AGENTS.md`** (repo root) — context for AI coding agents. Start from
  [`templates/AGENTS.md`](templates/AGENTS.md). Keep it short. `CLAUDE.md` should be a **symlink**
  to `AGENTS.md`, not a copy, so the two never drift:
  ```
  ln -s AGENTS.md CLAUDE.md
  ```

## Markdown standard

Every `.md` file in every repository follows one standard (org-wiki ADR 0001, proposed; private):

- **Front matter.** Every file starts with 11 fields, in this order: `name`, `description`, `date`, `lastmod`,
  `tags`, `categories`, `draft`, `slug`, `type`, `preview`, `weight`.
  - `date` never changes.
  - `lastmod` changes on every edit.
- **Self index.** Every heading is listed with its line number, between ``.
- **Folder index.** Every folder that holds `.md` files has an `INDEX.md` with one line per file.
  `docs/INDEX.md` is the entry point to a repository's docs.
- **Exemptions.** Files whose own format forbids these fields: `SKILL.md`, Claude agent and command files,
  issue and PR templates, and the `CLAUDE.md` pointer.

`update_md_index.py FILE --dir-index` writes all three, and `--check` verifies them. The tool and its checker ship
in the `documentation-standard` skill in `Thriwe-2-0/agent-plugins`.

## Reviews

- Review for correctness and blast radius first, style second.
- For infrastructure changes: confirm the plan output and exactly what gets created or
  destroyed before approving.
