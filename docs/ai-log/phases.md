# AI work log — phases, agents, models, tokens

Sub-agent token counts come from each agent's completion notice. Main-session (Opus) usage comes from the `/cost` screenshots in `screenshots/`.

## P0–P3 (setup + parallel build) — 2026-10-26

| Agent | Model | Scope | Tokens | Duration | Outcome |
|---|---|---|---|---|---|
| Orchestrator | Opus 5.5 | fork/clone/branch, domain contract, brain (rules, stages, resolver, cross-row), brain tests, evaluator | see /cost | — | — |
| devops-builder | Haiku 5.5 | Docker, compose, Makefile, pre-commit, CI/security/release workflows, Dependabot, agent defs | 113,326 | 5.8 min | done |
| fixture-builder | Haiku 5.5 | sample generator, 6 fake statements + labels, coverage script | 155,831 | 6.8 min | done; 53/66 catalog IDs, gaps covered by unit tests |
| backend-builder | Sonnet 5.5 | ingest, normalize, core, db, services, API, tests | | | |
| frontend-builder | Sonnet 5.5 | Next.js UI per 07/07a | | | |

Decisions:
- Four builders ran in parallel in disjoint directories of one tree instead of separate worktrees. With contracts frozen first there was no merge risk, and it saved worktree setup and merge time.
- Agents used `general-purpose` + a model override with the brief from `.claude/agents/*`, avoiding a session restart.
