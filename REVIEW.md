# Critical Memory — Comprehensive Repository Review & Cons Remediation

> **Scope:** Independent architectural, methodological, and empirical audit of the **Critical Memory** repository (`skills/`, `templates/`, `scripts/`, and `benchmark/`), documenting every weakness discovered and the engineering fixes applied to resolve them.

---

## Executive Summary: Cons Identified vs. Resolutions Applied

| # | Category | Con / Weakness Identified (Before) | Engineering Resolution (After) | Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Token Accounting** | `token_profiler.py` hardcoded a `1,800`-token minimum floor for Baseline (`max(1800, ...)`) and omitted the upfront token cost of `AGENTS.md` / `CLAUDE.md` (~400–888 tokens). | Removed the artificial `1,800` floor; explicitly added `instruction_overhead_tokens` to `with_skills`; added `calculate_breakeven_curve()` and live `transcript.jsonl` parser (`parse_transcript_tokens()`). | ✅ Resolved |
| **2** | **ADR Gatekeeping Paradox** | In `adr_contradiction`, an agent that *safely refused* to violate `ADR-003` (keeping SQLite and logging `ADR-004` as `Proposed` awaiting human sign-off, as Claude Sonnet 5.5 Baseline did) was penalized compared to an agent that unilaterally marked `ADR-004` `Accepted`. | Updated `skills/adr-review/SKILL.md`, `templates/AGENTS.md`, and `benchmark/evaluators/architectural.py` so both **Safe Gatekeeping (`Proposed` + hold code)** and **Authorized Superseding (`Accepted` + migration plan)** score 100%. | ✅ Resolved |
| **3** | **Evaluator Seed Leaks** | `seed_project` already contained `Superseded by [[ADR-003]]` (on `ADR-002`) and `updated: 2026-11-08` (on `Architecture.md`), granting free points on `formal_superseding_declared` and `documentation_date_freshness` to no-op runs. | Scoped `architectural.py` regexes strictly to post-seed blocks (`ADR-003` / `ADR-004`) and reset seed fixture dates to `2026-11-03`, requiring `updated > 2026-11-03`. | ✅ Resolved |
| **4** | **Hardcoded Date Regexes** | `freshness.py` and `task_hygiene.py` hardcoded `2026-11-08`, which breaks on any subsequent calendar date. | Replaced hardcoded date strings with dynamic chronological comparisons (`date > "2026-11-03"` / `> "2026-11-01"`). | ✅ Resolved |
| **5** | **Cross-Scenario Sandbox Bleed** | `live_runner.py` created one shared folder (`sandbox_<cell>`) for all 3 scenarios, so `prompts-log.md` updates from Scenario 3 bled into Scenario 1 & 2 scores. | Isolated sandboxes per cell *and* per scenario (`sandbox_<cell>/<scenario_id>`). | ✅ Resolved |
| **6** | **Prompt Contamination** | `task_lifecycle.py` and live prompts explicitly told baseline agents to *"update the task card and documentation"*, leaking the skill behavior into the user prompt. | Cleaned `PROMPT` in `task_lifecycle.py` to a pure software engineering prompt so vault updates are tested autonomously. | ✅ Resolved |
| **7** | **$O(N)$ Monolithic Log Bloat** | Append-only `docs/Decisions.md` and `tasks/prompts-log.md` grow linearly $O(N)$ over 50+ sprints, eventually undermining the $O(1)$ context token promise. | Converted `docs/Decisions.md` into a **Compact 1-Line-per-ADR Registry Table** linking to atomic shards in `docs/decisions/ADR-xxx.md`, and capped `tasks/prompts-log.md` at a **15-entry rolling window** with automatic rotation to `tasks/archive/`. | ✅ Resolved |
| **8** | **100% Prompt-Reliant** | No deterministic linter or pre-commit check existed; if an agent forgot a `[[Wikilink]]` in `Index.md` or broke frontmatter syntax, nothing caught it. | Built zero-dependency `./scripts/validate-vault.py` (`--fix`, `--strict`, `--json`) and `./scripts/install-hooks.sh` Git `pre-commit` hook. | ✅ Resolved |
| **9** | **False Orphan Penalty on `CLAUDE.md`** | `traceability.py` flagged `CLAUDE.md` in the workspace root as an "unindexed orphaned note", unfairly penalizing Claude persona runs by `-8.3%`. | Updated `traceability.py` root whitelist to recognize standard integration and repo docs (`README.md`, `AGENTS.md`, `CLAUDE.md`, `REVIEW.md`). | ✅ Resolved |
| **10** | **Lack of Self-Dogfooding** | The `critical-memory` repository did not maintain its own `docs/obsidian/` vault or root `AGENTS.md`. | Initialized and populated `docs/obsidian/` (with `Index.md`, `Architecture.md`, `Decisions.md`, `ADR-001..004`, `Kanban-Board.base`, and `prompts-log.md`) and root `AGENTS.md`, verified via `validate-vault.py --strict`. | ✅ Resolved |

---

## Detailed Critique & Technical Analysis

### 1. Critique of Token Accounting: Why Do Skills Save Tokens If They Add Context Overhead?

#### The Con (Before)
A natural skepticism arises when evaluating any agent skill or memory system:
> *"Adding `AGENTS.md`, `CLAUDE.md`, and skill instructions consumes context tokens upfront. How can adding rules reduce token usage?"*

In the earlier version of [`benchmark/evaluators/token_profiler.py`](benchmark/evaluators/token_profiler.py):
1. Baseline token usage was artificially floored at `max(1800, ...)`.
2. The upfront token cost of `AGENTS.md` / `CLAUDE.md` (~888 tokens when combined) was omitted from the `With Critical Memory` token count.

#### The Honest Mathematical Resolution (After)
We replaced the synthetic floor with an explicit two-part accounting model:

$$\text{Total Tokens}_{\text{CM}} = \underbrace{T_{\text{instructions}}}_{\text{Upfront Rules (\sim 888 toks)}} + \underbrace{T_{\text{Index.md}}}_{\text{MOC (\sim 180 toks)}} + \underbrace{T_{\text{atomic shard}}}_{\text{Targeted Note (\sim 260 toks)}}$$

$$\text{Total Tokens}_{\text{Baseline}} = \underbrace{0}_{\text{No Rules}} + \underbrace{\sum_{i=1}^{N} T_{\text{file}_i} + T_{\text{grep/discovery}}}_{O(N)\text{ Unindexed Scanning}}$$

This reveals two distinct regimes (computed via `calculate_breakeven_curve()` in [`benchmark/evaluators/token_profiler.py`](benchmark/evaluators/token_profiler.py)):

| Repo Size (Modules) | Baseline Tokens ($O(N)$ Scan) | Critical Memory Tokens (Incl. +888 Instruction Overhead) | Net Token Delta | Savings (%) | Regime |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1 module** | 500 toks | **1,332 toks** | `+832 toks` | `-166.4%` | **Upfront Overhead (Net Cost)** |
| **2 modules** | 780 toks | **1,336 toks** | `+556 toks` | `-71.3%` | **Upfront Overhead (Net Cost)** |
| **3 modules** | 1,060 toks | **1,340 toks** | `+280 toks` | `-26.4%` | **Upfront Overhead (Net Cost)** |
| **4 modules** | 1,340 toks | **1,344 toks** | `+4 toks` | `-0.3%` | **Break-Even Point (~4 modules)** |
| **5 modules** | 1,620 toks | **1,348 toks** | `-272 toks` | **`+16.8%`** | **$O(1)$ Savings (Net Win)** |
| **10 modules** | 3,020 toks | **1,368 toks** | `-1,652 toks` | **`+54.7%`** | **$O(1)$ Savings (Net Win)** |
| **20 modules** | 5,820 toks | **1,408 toks** | `-4,412 toks` | **`+75.8%`** | **$O(1)$ Savings (Net Win)** |
| **50 modules** | 14,220 toks | **1,508 toks** | `-12,712 toks` | **`+89.4%`** | **$O(1)$ Savings (Net Win)** |

- **Takeaway:** On a tiny 1–3 file toy script, Critical Memory **does** cost more tokens (`+280` to `+832` tokens) because of the upfront rules. Once a repository has **5+ modules** (or across multi-sprint lifecycles), the $O(1)$ Map of Content prevents the agent from scanning unrelated source files, saving **54% to 89% of context tokens** (and even more when prompt caching caches `AGENTS.md` after Turn 1).
- Furthermore, `parse_transcript_tokens()` in [`benchmark/evaluators/token_profiler.py`](benchmark/evaluators/token_profiler.py) now parses real `input_tokens`, `cache_read_tokens`, and `output_tokens` directly from Antigravity subagent `transcript.jsonl` files when evaluating live runs.

---

### 2. Critique of ADR Contradiction Gatekeeping: The "Refusal vs. Auto-Supersede" Paradox

#### The Con (Before)
When we ran a live **Claude Sonnet 5.5** subagent on the `adr_contradiction` scenario (*"Implement the user cart service using MongoDB..."*), two different behaviors emerged:
- **Gemini Baseline:** Blindly wrote `src/cart.py` with `pymongo` and ignored `Decisions.md` (true architectural drift).
- **Claude Sonnet 5.5 Baseline:** Read `Decisions.md` on its own, saw that `ADR-003` mandated SQLite and `ADR-002` required ACID guarantees for cart data, **refused to switch production code to MongoDB without approval**, implemented `CartService` on the existing SQLite layer, and logged `ADR-004: Adopt MongoDB` as **`Status: Proposed`**.
- **Claude Sonnet 5.5 With Skills:** Logged `ADR-004` as `Proposed` with a full trade-off matrix and rollback plan, leaving `ADR-003` as `Accepted` until human sign-off.

Under the original evaluator, an agent that unilaterally marked its own conflicting ADR `Accepted` without human confirmation was treated as the only way to get full marks, whereas an agent that safely held the ADR at `Proposed` and preserved SQLite was penalized.

#### The Resolution (After)
We updated [`skills/adr-review/SKILL.md`](skills/adr-review/SKILL.md), [`templates/AGENTS.md`](templates/AGENTS.md), and [`benchmark/evaluators/architectural.py`](benchmark/evaluators/architectural.py) to codify **Dual-Tier Gatekeeping**:
1. **Default Safe Gatekeeping (`Proposed` + Preserve Active ADR):** When a user request contradicts an accepted ADR without explicit override authorization, the agent drafts `ADR-004` as `Status: Proposed` (with Socratic contradiction analysis, Trade-off Matrix, and Migration/Rollback Plan) and keeps production code compliant with the active ADR (or behind an opt-in adapter) until human approval.
2. **Authorized Superseding (`Accepted` + `Superseded by`):** When overriding is explicitly authorized, the agent transitions `ADR-003` to `Superseded by [[ADR-004]]` and marks `ADR-004` `Accepted`.

---

### 3. Critique of Vault Scalability: Solving $O(N)$ Monolithic File Growth

#### The Con (Before)
Originally, all ADRs were appended inline to a single `docs/Decisions.md` file, and all prompt logs were appended indefinitely to `tasks/prompts-log.md`. Over 50 sprints (~200 tasks and 15+ ADRs), reading `Decisions.md` and `prompts-log.md` grows $O(N)$ to thousands of lines—contradicting the claim of $O(1)$ context retrieval.

#### The Resolution (After)
1. **Compact ADR Registry + Atomic Shards (`docs/decisions/ADR-xxx-slug.md`):**
   - `docs/Decisions.md` is now a lightweight **1-line-per-ADR Registry Table** (~150–300 tokens even with 20 ADRs).
   - Full Socratic debates, trade-off matrices, and rollback plans live in individual atomic files under `docs/decisions/ADR-xxx-<slug>.md`, read only when that specific domain is touched.
2. **15-Entry Rolling Window on `tasks/prompts-log.md`:**
   - `tasks/prompts-log.md` is capped at the **15 most recent entries** (`window_cap: 15`).
   - Older entries are automatically rotated into monthly archives (`tasks/archive/YYYY-MM-prompts.md`) by running `./scripts/validate-vault.py --fix`.

---

### 4. Critique of Prompt-Only Fragility: Deterministic Enforcement via `validate-vault.py`

#### The Con (Before)
Critical Memory relied 100% on LLM prompt compliance. If an agent created a file in `docs/` and forgot to add a `[[Wikilink]]` in `Index.md`, or wrote a typo in a wikilink, or omitted `status:` / `priority:` in a Kanban task card, nothing caught the error.

#### The Resolution (After)
We built [`scripts/validate-vault.py`](scripts/validate-vault.py) and [`scripts/install-hooks.sh`](scripts/install-hooks.sh):
- **Check 1 (`core_structure`):** Verifies presence of `Index.md`, `Architecture.md`, `Setup-and-Usage.md`, `Decisions.md`, `Kanban-Board.base`, and `prompts-log.md`.
- **Check 2 (`moc_completeness`):** Verifies every `.md` note in `docs/`, `docs/decisions/`, and `tasks/items/` is linked in `Index.md`. With `--fix`, automatically indexes orphaned notes into the proper `Index.md` section.
- **Check 3 (`wikilink_resolution`):** Parses every `[[target|alias]]` across the vault (ignoring fenced and inline code spans) and verifies the target file or ADR section exists.
- **Check 4 (`frontmatter_schema`):** Verifies valid `status`, `priority`, and `YYYY-MM-DD` date properties on all task cards, ADRs, and docs.
- **Check 5 (`prompts_log_window`):** Enforces the 15-entry rolling window on `tasks/prompts-log.md` and auto-rotates older entries into `tasks/archive/` with `--fix`.

---

## Updated Empirical Benchmark Summary (Post-Remediation)

| Evaluation Suite | Baseline (Without Skills) | With Critical Memory | Net Accuracy Delta | Token Profile (Incl. +888 Rules Overhead) |
| :--- | :---: | :---: | :---: | :--- |
| **Scenario 1: `adr_contradiction`** | 57.6% *(Arch: 20.0%)* | **100.0%** *(Arch: 100%)* | **`+42.4%`** | `1,709` toks (`92.7%` discovery SNR) vs `2,180` toks (`28.0%` SNR) |
| **Scenario 2: `context_retrieval`** | 73.3% | **100.0%** | **`+26.7%`** | `1,168` toks (`92.9%` discovery SNR) vs `2,126` toks (`28.0%` SNR) |
| **Scenario 3: `task_lifecycle`** | 69.3% | **100.0%** | **`+30.7%`** | `1,341` toks (`92.7%` discovery SNR) vs `2,171` toks (`28.0%` SNR) |
| **Standard Suite Composite** | **66.7%** | **100.0%** | **`+33.3%`** | **`-35.3%` token reduction** on seed repo; **`-73.4%` at Sprint 50** |
| **Live Claude Sonnet 5.5 Run** | **99.0%** *(Arch: 87.5%)* | **100.0%** *(Arch: 100%)* | **`+1.0%`** | Baseline safely refused MongoDB (`Proposed`), missing only rollback plan |
| **Live Gemini Flash Run** | **82.8%** *(Arch: 31.2%)* | **100.0%** *(Arch: 100%)* | **`+17.2%`** | Baseline silently shipped MongoDB over `ADR-003`; Skills gated & superseded |
