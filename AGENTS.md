# AGENTS.md

Working rules for coding agents in this repository.

## Repository

Personal collection of [Agent Skills](https://agentskills.io): each skill is a directory under `skills/` holding a `SKILL.md` plus optional `scripts/`, `references/`, `assets/`. Document contracts (role and consumer of every file) live in [skills/docmap/references/standards.md](skills/docmap/references/standards.md) - read it before writing or changing documentation.

## Commands

Run after every change:

```bash
make check   # Markdown formatting, documentation audit, tests
```

Individual targets: `make help` lists them (`fmt`, `audit`, `test`).

## Rules

- One source of truth per fact: cross-reference with relative links, never copy a section between `README.md`, `docs/`, and `SKILL.md`.
- Root documents carry no tables of contents; the only documentation index is `docs/index.md`, and `docs/` appears only when three-plus separate topics exist.
- A new skill: kebab-case directory under `skills/` whose name matches the `name` frontmatter; no `README.md` inside the skill directory.
