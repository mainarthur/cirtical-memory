# GitHub Copilot Instructions — Critical Memory

- **Context & Architecture ($O(1)$ Hub):** Reference `docs/obsidian/Index.md` for project structure and living documentation. Keep `Index.md` updated with `[[Wikilinks]]` for all notes in `docs/`, `docs/decisions/`, and `tasks/items/`.
- **Traceability & Rolling Log:** Record prompt outcomes and tasks in `docs/obsidian/tasks/prompts-log.md` (capped at 15 entries; rotate older entries to `tasks/archive/`).
- **Architectural Integrity:** Verify consistency with `docs/obsidian/docs/Decisions.md` and `docs/decisions/` before making breaking structural changes. Flag conflicting decisions, present a trade-off matrix + rollback plan, and record the new ADR as `Proposed` (until approved) or `Accepted` (`Superseded by [[ADR-xxx]]`) when explicitly authorized.
- **Validation:** Run `./scripts/validate-vault.py` to enforce link, orphan, and frontmatter hygiene.

