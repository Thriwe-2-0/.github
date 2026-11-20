#!/usr/bin/env python3
"""Make a markdown file compliant: full frontmatter, self index, directory index.

Usage:
    update_md_index.py FILE [FILE ...] [--dir-index] [--type T] [--tags a,b]
                       [--categories a,b] [--description TEXT] [--check]

For every FILE the script:
  1. ensures all 11 frontmatter fields exist (missing ones are filled, existing
     values are kept) and bumps `lastmod`;
  2. regenerates the self index (<!-- toc:start --> ... <!-- toc:end -->) with
     heading + line number, converging so numbers match the final file;
  3. with --dir-index, adds/updates the file's line in INDEX.md of the same
     directory, then applies steps 1-2 to INDEX.md as well.

--check only reports problems and changes nothing (exit 1 if any).
Standard library only.
"""
import argparse
import datetime
import os
import re
import sys

FIELDS = ["name", "description", "date", "lastmod", "tags", "categories",
          "draft", "slug", "type", "preview", "weight"]
LIST_FIELDS = {"tags", "categories"}
TOC_START, TOC_END = "<!-- toc:start -->", "<!-- toc:end -->"
STOP_WORDS = {"a", "an", "the", "of", "and", "or", "to", "in", "on", "for", "with", "is"}


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def kebab(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def make_slug(text):
    words = [w for w in kebab(text).split("-") if w]
    kept = [w for w in words if w not in STOP_WORDS]
    return "-".join(kept or words)


def split_frontmatter(text):
    """Return (blocks, body). blocks is an ordered list of (key, [raw lines])."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm, body = lines[1:i], "\n".join(lines[i + 1:])
            break
    else:
        return None, text
    blocks = []
    for ln in fm:
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", ln)
        if m:
            blocks.append([m.group(1), [ln]])
        elif blocks:
            blocks[-1][1].append(ln)
    return blocks, body


def block_value(lines):
    first = lines[0].split(":", 1)[1].strip()
    if first:
        return first.strip("\"'")
    items = [l.strip()[2:].strip().strip("\"'") for l in lines[1:] if l.strip().startswith("- ")]
    return items


def quote(value):
    if value == "" or re.search(r'[:#\[\]{}&*!|>\'"%@`,]', value) or value != value.strip():
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def render(key, value):
    if key in LIST_FIELDS:
        return [f"{key}:"] + [f"  - {quote(v)}" for v in value]
    if key in ("draft", "weight"):
        return [f"{key}: {value}"]
    if key in ("date", "lastmod"):
        return [f'{key}: "{value}"']
    return [f"{key}: {quote(str(value))}"]


def first_heading(body):
    for ln in body.split("\n"):
        m = re.match(r"^#{1,6}\s+(.*)", ln)
        if m and m.group(1).strip().lower() != "contents":
            return m.group(1).strip()
    return ""


def build_frontmatter(blocks, body, path, opts):
    stem = os.path.splitext(os.path.basename(path))[0]
    existing = {k: block_value(v) for k, v in (blocks or [])}
    extra = [(k, v) for k, v in (blocks or []) if k not in FIELDS]
    title = first_heading(body) or stem
    ftype = opts.type or ("index" if stem.upper() == "INDEX" else "doc")
    try:
        created = datetime.datetime.fromtimestamp(
            os.stat(path).st_ctime, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    except OSError:
        created = now_iso()
    name = existing.get("name") or kebab(stem)
    defaults = {
        "name": name,
        "description": opts.description or title,
        "date": created,
        "lastmod": now_iso(),
        "tags": [t for t in (opts.tags or "").split(",") if t.strip()] or [ftype],
        "categories": [c for c in (opts.categories or "").split(",") if c.strip()] or ["general"],
        "draft": "false",
        "slug": make_slug(title) or name,
        "type": ftype,
        "preview": "",
        "weight": "1",
    }
    out, filled = [], []
    for key in FIELDS:
        val = existing.get(key)
        empty = val is None or (key in LIST_FIELDS and not val) or \
            (key not in ("preview",) and val == "")
        if key == "lastmod":
            val = defaults["lastmod"]  # always bump
        elif empty:
            val = defaults[key]
            filled.append(key)
        out += render(key, val)
    for _, raw in extra:
        out += raw
    return "---\n" + "\n".join(out) + "\n---\n", filled


def anchor(title):
    a = re.sub(r"[^\w\- ]", "", title.lower()).strip()
    return re.sub(r" ", "-", a)


def strip_toc(body):
    pat = re.compile(re.escape(TOC_START) + r".*?" + re.escape(TOC_END) + r"\n*", re.S)
    return pat.sub("", body, count=1)


def headings(lines, first_line_no):
    """Yield (level, title, absolute_line_no) skipping fenced code and the toc."""
    in_fence, in_toc = False, False
    for off, ln in enumerate(lines):
        if ln.strip() == TOC_START:
            in_toc = True
        if in_toc:
            if ln.strip() == TOC_END:
                in_toc = False
            continue
        if re.match(r"^\s*(```|~~~)", ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", ln)
        if m:
            yield len(m.group(1)), m.group(2), first_line_no + off


def build_toc(fm_text, body):
    clean = strip_toc(body).lstrip("\n")
    fm_lines = fm_text.count("\n")
    hs = list(headings(clean.split("\n"), 1))
    if not hs:
        return fm_text + clean
    # toc block = start marker + "## Contents" + one line per heading + end marker + blank line
    offset = fm_lines + len(hs) + 4
    entries = [(lvl, t, ln + offset) for lvl, t, ln in hs]
    base = min(l for l, _, _ in entries)
    toc = [TOC_START, "## Contents"]
    for lvl, t, ln in entries:
        toc.append(f"{'  ' * (lvl - base)}- [{t}](#{anchor(t)}) — line {ln}")
    toc += [TOC_END, ""]
    return fm_text + "\n".join(toc) + "\n" + clean


def process(path, opts, check=False):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    blocks, body = split_frontmatter(text)
    fm_text, filled = build_frontmatter(blocks, body, path, opts)
    new = build_toc(fm_text, body)
    if not new.endswith("\n"):
        new += "\n"
    if check:
        old_nolm = re.sub(r'^lastmod:.*$', '', text, flags=re.M)
        new_nolm = re.sub(r'^lastmod:.*$', '', new, flags=re.M)
        ok = old_nolm == new_nolm
        print(f"{'OK  ' if ok else 'FAIL'} {path}" + ("" if ok else f" (missing/stale: {filled or 'index/format'})"))
        return ok
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(new)
    print(f"updated {path}" + (f" (filled: {', '.join(filled)})" if filled else ""))
    return True


def update_dir_index(path, opts):
    d = os.path.dirname(os.path.abspath(path))
    idx = os.path.join(d, "INDEX.md")
    base = os.path.basename(path)
    if base == "INDEX.md":
        return
    with open(path, encoding="utf-8") as fh:
        blocks, _ = split_frontmatter(fh.read())
    info = {k: block_value(v) for k, v in blocks}
    line = f"- [{info['name']}]({base}) — {info['description']}"
    if not os.path.exists(idx):
        with open(idx, "w", encoding="utf-8") as fh:
            fh.write(f"# {os.path.basename(d)} index\n\n")
    with open(idx, encoding="utf-8") as fh:
        text = fh.read()
    pat = re.compile(r"^- \[[^\]]*\]\(" + re.escape(base) + r"\).*$", re.M)
    if pat.search(text):
        text = pat.sub(lambda _: line, text, count=1)
    else:
        text = text.rstrip("\n") + "\n" + line + "\n"
    with open(idx, "w", encoding="utf-8") as fh:
        fh.write(text)
    idx_opts = argparse.Namespace(type="index", tags="index", categories="general",
                                  description=f"Index of markdown files in {os.path.basename(d)}")
    process(idx, idx_opts)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--dir-index", action="store_true")
    ap.add_argument("--type")
    ap.add_argument("--tags")
    ap.add_argument("--categories")
    ap.add_argument("--description")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only-fields", help="comma list limiting the managed fields "
                    "(for files whose platform allows only some keys, e.g. SKILL.md: name,description)")
    opts = ap.parse_args()
    if opts.only_fields:
        global FIELDS
        FIELDS = [f for f in FIELDS if f in opts.only_fields.split(",")]
    ok = True
    for f in opts.files:
        ok &= process(f, opts, check=opts.check)
        if opts.dir_index and not opts.check:
            update_dir_index(f, opts)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
