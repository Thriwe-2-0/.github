# Contributing

> **Starter conventions** — ratify with the team and adjust as practice evolves.

## Branches

Never commit to `main` directly. Branch from `main` using:

```
<type>/<TICKET-KEY>-<short-description>
```

- **type**: `feat` · `fix` · `infra` · `chore` · `docs`
- **TICKET-KEY**: the Jira issue key, e.g. `PRISM-123`
- example: `feat/PRISM-123-add-redis-cache`

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>
```

example: `fix(superset): drop QueuePool sizing keys incompatible with NullPool`

Keep the subject imperative and under ~72 characters. Reference the ticket in the body or PR.

## Pull requests

1. Open against `main`.
2. Fill in the PR template.
3. At least **two approvals** before merge.
4. CI must be green.
5. **Squash-merge** to keep `main` history linear.

## Code ownership

Define a `CODEOWNERS` file **in each repository** — this cannot be set org-wide.
Listed owners are auto-requested for review on matching paths.

## Reviews

- Review for correctness and blast radius first, style second.
- For infrastructure changes: confirm the plan output and exactly what gets created or
  destroyed before approving.
