#!/usr/bin/env python3
"""docmap audit - gather documentation facts for a repository.

Standard library only; Python >= 3.9.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse

VERSION = "1.0.0"
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
SCHEME_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
FENCE_RE = re.compile(r"```[\s\S]*?(?:```|$)")


def walk_markdown(root):
    """Yield absolute paths of all .md/.mdx files under root, sorted."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith((".md", ".mdx")) and not name.startswith("."):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def extract_links(text):
    return LINK_RE.findall(FENCE_RE.sub("", text))


def is_relative_link(target):
    if SCHEME_RE.match(target):
        return False  # http:, mailto:, ...
    return not target.startswith(("#", "/"))


def audit(root):
    """Return a list of findings: dicts with kind, file, message."""
    findings = []

    def add(kind, file, message):
        findings.append({"kind": kind, "file": os.path.relpath(file, root) or ".", "message": message})

    if not os.path.isdir(root):
        raise NotADirectoryError(root)

    if not os.path.isfile(os.path.join(root, "README.md")):
        add("MISSING", os.path.join(root, "README.md"), "expected root document absent")
    if not os.path.isfile(os.path.join(root, "CONTRIBUTING.md")):
        add("INFO", os.path.join(root, "CONTRIBUTING.md"),
            "absent (needed only for public repos with outside contributors)")
    docs_dir = os.path.join(root, "docs")
    if os.path.isdir(docs_dir) and not os.path.isfile(os.path.join(docs_dir, "index.md")):
        add("INFO", docs_dir, "docs/ has no index.md index")

    for path in walk_markdown(root):
        try:
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
        except (OSError, UnicodeDecodeError) as error:
            add("INVALID", path, f"unreadable: {error}")
            continue

        for target in extract_links(text):
            if not is_relative_link(target):
                continue
            resolved = os.path.normpath(
                os.path.join(os.path.dirname(path), urllib.parse.unquote(target.split("#")[0]))
            )
            if not os.path.exists(resolved):
                add("BROKEN-LINK", path, f"relative link target missing: {target}")

    return findings


def format_findings(findings, root):
    if not findings:
        return f"No findings under {root}\n"
    order = ["MISSING", "INVALID", "BROKEN-LINK", "INFO"]
    lines = [
        f'{f["kind"].ljust(11)} {f["file"]}: {f["message"]}'
        for f in sorted(findings, key=lambda f: (order.index(f["kind"]), f["file"]))
    ]
    blocking = sum(1 for f in findings if f["kind"] != "INFO")
    info = len(findings) - blocking
    return "\n".join(lines) + f"\n\n{blocking} blocking, {info} info\n"


def main(argv=None):
    parser = argparse.ArgumentParser(prog="docmap", description="Audit repository documentation.")
    parser.add_argument("command", choices=["audit"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    findings = audit(root)
    if args.as_json:
        print(json.dumps({"version": VERSION, "root": root, "findings": findings}, indent=2))
    else:
        sys.stdout.write(format_findings(findings, root))
    return 1 if any(f["kind"] != "INFO" for f in findings) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (NotADirectoryError, FileNotFoundError) as error:
        sys.stderr.write(f"docmap: {error}\n")
        sys.exit(2)
