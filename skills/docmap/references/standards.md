# Documentation Standards

Single source of truth for document contracts and format limits used by the docmap workflow. SKILL.md links here; do not copy this content into other files.

## Document contracts

| Document          | Consumer       | Purpose                                                                                    | When required                           |
| ----------------- | -------------- | ------------------------------------------------------------------------------------------ | --------------------------------------- |
| `README.md`       | human + agent  | Entry point: what the repo is, one-paragraph purpose, how to install/use, where to go next | Always                                  |
| `AGENTS.md`       | agent          | Working rules for coding agents in this repo (checks, style, constraints)                  | When agents work in the repo            |
| `CONTRIBUTING.md` | human          | How an outside contributor sets up, changes, and submits work                              | Public repos with external contributors |
| `CHANGELOG.md`    | human          | Release history users can rely on                                                          | Versioned releases only                 |
| `SECURITY.md`     | human          | Vulnerability reporting channel                                                            | Public products only                    |
| `docs/<topic>.md` | human or agent | One deep topic that exceeds what fits in README                                            | When a topic needs more than ~50 lines  |
| `docs/index.md`   | human + agent  | Index of `docs/`: one line per file with consumer noted                                    | Whenever `docs/` exists                 |

Rules that follow from the table:

- A document not demanded by the repo's situation stays unwritten. A README and a skill table cover a small repo; `docs/` earns its existence at three-plus separate topics.
- Content that would repeat verbatim moves to the document the contract assigns; other documents link to it with relative paths.
- The consumer decides tone and vocabulary: agent-facing files are imperative and terse; human-facing files may explain motivation.
