---
name: readme
description: What the .github repository holds and how org-wide default files apply
date: "2026-11-20T08:55:46.000Z"
lastmod: "2026-11-20T08:55:59.000Z"
tags:
  - type/reference
  - org/thriwe
  - repo/.github
categories:
  - overview
draft: false
slug: github-thriwe-organization-defaults
type: reference
preview: ""
weight: 1
---
<!-- toc:start -->
## Contents
- [`.github` — Thriwe organization defaults](#github--thriwe-organization-defaults) — line 26
  - [What lives here](#what-lives-here) — line 34
  - [Precedence](#precedence) — line 45
  - [Not defaultable from here](#not-defaultable-from-here) — line 50
<!-- toc:end -->

# `.github` — Thriwe organization defaults

This repository holds **organization-wide defaults** for every repo in the `Thriwe-2-0` org.
GitHub automatically applies the files here to any repository that does **not** define its own.

> ⚠ This repo must stay **public** for the defaults to apply. GitHub ignores a private
> `.github` repo for organization-wide defaulting.

## What lives here

| File | Effect across the org |
|------|------|
| `CONTRIBUTING.md` | Surfaced on every new issue/PR in repos without their own — the shared conventions |
| `PULL_REQUEST_TEMPLATE.md` | Pre-fills the PR description box |
| `.github/ISSUE_TEMPLATE/` | Issue forms offered when opening an issue |
| `SECURITY.md` | Linked from the Security tab of every repo |
| `profile/README.md` | Rendered on the org's public profile: https://github.com/Thriwe-2-0 |
| `templates/` | Starters repos copy in (`AGENTS.md`, `CODEOWNERS`) — these can't be auto-defaulted |

## Precedence

A repository's **own** file always wins. GitHub looks in the consuming repo first
(`.github/` → root → `docs/`); only if nothing is found does it fall back to the default here.

## Not defaultable from here

`LICENSE`, repo-level `README.md`, **`CODEOWNERS`**, and agent-context files
(**`AGENTS.md`** / `CLAUDE.md`) cannot be defaulted org-wide — each repo must define its own.
Use the starters in [`templates/`](templates/).
