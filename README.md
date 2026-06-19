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

## Precedence

A repository's **own** file always wins. GitHub looks in the consuming repo first
(`.github/` → root → `docs/`); only if nothing is found does it fall back to the default here.

## Not defaultable from here

`LICENSE`, repo-level `README.md`, and **`CODEOWNERS`** cannot be defaulted org-wide —
each repository must define its own. CODEOWNERS in particular is per-repo only.
