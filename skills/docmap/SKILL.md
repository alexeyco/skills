---
name: docmap
description: Write excellent repository documentation - human-readable README and guides, agent-facing AGENTS.md, with document contracts, one source of truth per fact, cross-references instead of copies, and a verification script that audits links, root documents, and missing docs. Use when asked to write or document a repository, create or fix a README, put docs in order, audit or format documentation, or build a documentation index before publishing.
license: MIT
metadata:
  author: alexeyco
  version: "0.1.0"
---

You audit and format repository documentation so that every document has one role, one consumer, and one source of truth.

## When to Use

- User asks to document a repository or put its documentation in order
- User asks to audit, format, or fix documentation: README, `docs/`, `SKILL.md`, links
- Preparing a repository for publication
- A documentation map or index must be created or refreshed

## Hard Rules

1. **No duplication.** Every fact lives in exactly one document. Everywhere else, link to it with a relative path. Never restate installation steps, structure, conventions, or spec limits in two files; never copy sections between `README.md`, `docs/`, and `SKILL.md`.
2. **One role, one consumer per document.** Before creating or updating a file, state its consumer - human, agent, or both - and its single purpose, per the contracts in [references/standards.md](references/standards.md). If a document's role is unclear or nobody consumes it, do not write it.
3. **Verify before writing.** Every statement must be derivable from repository evidence: file contents, config, scripts, git history. Run the audit script and read the files you describe. A claim you cannot point at becomes `<!-- TODO: verify <claim> -->`, never invented prose.
4. **Respect existing structure.** Update files in place and follow established naming and formatting. Introduce a new file only when a contract in the standards requires it.
5. **No tables of contents in root documents.** `README.md`, `AGENTS.md`, and `CONTRIBUTING.md` never enumerate the documentation; orientation goes through the single index, `docs/index.md`. Linking a specific article contextually, where the prose needs it, is fine - a contents list is not.

## Workflow

### Step 1: Inventory

Run the audit script:

```bash
python3 <skill-dir>/scripts/docmap.py audit --root ./
```

It gathers facts and prints findings, one per line:

- `MISSING` - expected root document absent (`README.md`)
- `INVALID` - a Markdown file is unreadable (encoding or IO error)
- `BROKEN-LINK` - a relative Markdown link resolves to nothing
- `INFO` - advisory gaps (for example `docs/` without an index, missing `CONTRIBUTING.md`)

Exit code is 1 when any `INVALID` or `BROKEN-LINK` finding exists. Add `--json` for machine-readable output. The script only gathers facts; classification and decisions are yours. After changing the script, run its tests: `python3 scripts/test_docmap.py`.

When Python is unavailable (`command -v python3` fails), do not skip the inventory - check the repository yourself: enumerate `*.md` files excluding hidden and build directories, confirm the root documents and any `docs/` index against the contracts in [references/standards.md](references/standards.md), and resolve every relative link file by file. Report the same finding kinds.

### Step 2: Classify and plan

1. Determine the repository type from evidence - package manifests, directory layout, git remotes: application, library, collection of distributable units, or configuration/personal repo.
2. Look up the required and optional document set for that type in [references/standards.md](references/standards.md).
3. Build a plan: for each file - create, update, or leave; its consumer; the evidence its content will rest on. Show the plan to the user and get agreement before writing when the repository holds more than a few documents.

### Step 3: Write

Create or update the planned documents following their contracts:

- One H1 title, then only the content its consumer needs. No filler sections ("Overview" of things already obvious, "Background" nobody reads).
- Every structure claim, command, and file path must have been checked against the repository in Steps 1-2.
- Cross-reference instead of repeating: when text would appear in two places, keep it where the contract puts it and link from the other place.
- Unknowns become TODO comments, not guesses.

### Step 4: Maintain the single index

`docs/index.md` is the only documentation index in the repository (Hard Rule 5). When `docs/` holds articles:

- Create or refresh `docs/index.md` as a table - one row per article: path, consumer, one-line contents.
- The root documents link `docs/index.md` once, for orientation, and may reference specific articles contextually where the prose calls for it. What they never carry is a contents list or a `## Documentation` enumeration.
- The index lists and points; it never summarizes content the linked article already owns. Refresh in place, idempotently.

Where the repository's product is itself a catalog of items (a table of skills, plugins, examples in `README.md`), that table catalogs the product, not the documentation - it stays.

### Step 5: Verify

1. Re-run the audit and resolve every `INVALID` and `BROKEN-LINK` finding until the exit code is 0.
2. Re-read each document you wrote and check every factual claim against a concrete artifact: a file path, a command output, a commit. Remove or TODO-mark anything left unsupported.
3. Report to the user: files created and updated, findings resolved, open TODOs.
