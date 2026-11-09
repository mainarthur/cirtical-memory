# Claude Code Instructions — Critical Memory

This repository uses Critical Memory. Refer to `AGENTS.md` and `docs/obsidian/` for full conventions.

- **Vault Location:** `docs/obsidian/` (or `.memdoc/`).
- **Map of Content ($O(1)$ Discovery):** Read `docs/obsidian/Index.md` first and keep it updated with `[[Wikilinks]]` whenever notes in `docs/`, `docs/decisions/`, or `tasks/items/` are added or renamed.
- **Rolling Audit Log:** Record completed tasks and prompt milestones in `tasks/prompts-log.md` (max 15 recent entries; archive older entries to `tasks/archive/`).
- **Architectural Gatekeeping:** Before changing architecture, databases, or core libraries, check `docs/Decisions.md` and `docs/decisions/`. If a request contradicts an accepted ADR:
  1. Debate trade-offs with a structured **Trade-off Matrix** and **Migration/Rollback Plan**.
  2. Draft the conflicting ADR as `Status: Proposed` (keeping production code compliant with the active ADR until human sign-off), OR mark it `Accepted` (`Superseded by [[ADR-xxx]]`) if overriding was explicitly authorized.
- **Validation:** Run `./scripts/validate-vault.py` (when available) to verify link and frontmatter hygiene.

