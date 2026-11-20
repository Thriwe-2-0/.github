---
name: agents
description: "Starter AGENTS.md: copy to a repository root and fill in"
date: "2026-11-20T09:00:18.000Z"
lastmod: "2026-11-20T09:00:18.000Z"
tags:
  - type/reference
  - org/thriwe
  - repo/.github
categories:
  - template
draft: false
slug: agents-md
type: reference
preview: ""
weight: 1
---
<!-- toc:start -->
## Contents
- [AGENTS.md](#agentsmd) — line 30
  - [What this repo is](#what-this-repo-is) — line 36
  - [Repository type](#repository-type) — line 39
  - [Setup & common commands](#setup--common-commands) — line 42
  - [Conventions](#conventions) — line 45
  - [Releases / how changes reach production](#releases--how-changes-reach-production) — line 50
  - [Guardrails — do not touch](#guardrails--do-not-touch) — line 54
  - [Pointers](#pointers) — line 60
<!-- toc:end -->

# AGENTS.md

> Canonical context for AI coding agents (Claude Code, Codex, Cursor, Copilot, …).
> Keep this SHORT and current — bloated context files measurably degrade agent results.
> Copy to the repo root. `CLAUDE.md` is a one-line pointer file containing `@AGENTS.md`, not a copy.

## What this repo is
<!-- One or two sentences: what it owns, what it explicitly does NOT own. -->

## Repository type
<!-- IaC (Terraform/Terramate) · GitOps (Helm values) · container images · application code -->

## Setup & common commands
<!-- Exact commands. e.g. test: `make test` · lint/fmt: `make fmt` · generate: `make generate` -->

## Conventions
- Branches: `<type>/<TICKET>-<desc>` (feat|fix|infra|chore|docs)
- Commits: Conventional Commits, scope = component — `fix(superset): …`
- Never commit to `main`; open a PR (two approvals required).

## Releases / how changes reach production
<!-- GitOps: cut semver tag `vX.Y.Z`; ArgoCD syncs the HIGHEST tag. `main` is staging — untagged = not deployed.
     IaC: plan runs in CI via OIDC; apply is HUMAN-GATED — agents NEVER apply. -->

## Guardrails — do not touch
- Agents MUST NOT apply/destroy or mutate live cloud/cluster state.
- Verify you are on the intended branch before any delegated commit.
- Do not hand-edit generated files or vendored charts.
<!-- Add repo-specific boundaries: secrets, state, production paths. -->

## Pointers
<!-- Deeper docs, owning team, dashboards, runbooks. -->
