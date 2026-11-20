#!/usr/bin/env python3
"""Check every tracked markdown file against org-wiki ADR 0001.

Usage: check_docs.py   (run from anywhere inside the repository)

Checks:
1. `update_md_index.py --check` passes for each tracked `.md` file except the exempt ones. That covers the 11
   fields in order and a self index whose line numbers are current.
2. Every folder that holds a checked file has an `INDEX.md`, with a `](<file>)` line for each of its files.
3. Every relative link in an `INDEX.md` points to a file that exists.

Exempt files: `CLAUDE.md`, `SKILL.md`, `.github/` issue and PR templates, and `profile/README.md` (the public org profile page).

Exit codes: 0 valid, 1 a check failed (one line per problem on stdout), 2 not inside a git repository.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "update_md_index.py")
EXEMPT_NAMES = {"CLAUDE.md", "SKILL.md", "PULL_REQUEST_TEMPLATE.md"}
LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")


def main():
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if top.returncode != 0:
        print("not inside a git repository", file=sys.stderr)
        return 2
    os.chdir(top.stdout.strip())
    files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
    files = [f for f in files if os.path.basename(f) not in EXEMPT_NAMES
             and not f.startswith(".github/ISSUE_TEMPLATE/") and f != "profile/README.md"]
    problems = []
    result = subprocess.run([sys.executable, "-I", TOOL, "--check", *files], capture_output=True, text=True)
    problems += [line for line in result.stdout.splitlines() if line.startswith("FAIL")]
    by_dir = {}
    for f in files:
        by_dir.setdefault(os.path.dirname(f) or ".", []).append(os.path.basename(f))
    for d, names in sorted(by_dir.items()):
        index = os.path.join(d, "INDEX.md")
        if not os.path.exists(index):
            problems.append(f"FAIL {index}: missing")
            continue
        text = open(index, encoding="utf-8").read()
        for name in names:
            if name != "INDEX.md" and f"]({name})" not in text:
                problems.append(f"FAIL {index}: no line for {name}")
        for target in LINK_RE.findall(text):
            if "://" not in target and not os.path.exists(os.path.normpath(os.path.join(d, target))):
                problems.append(f"FAIL {index}: link to missing {target}")
    for p in problems:
        print(p)
    print(f"{'OK' if not problems else 'FAILED'}: {len(files)} files checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
