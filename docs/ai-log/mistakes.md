# Where AI got things wrong (and how it was caught)

| # | Phase | What the AI did | How it was caught | Fix |
|---|---|---|---|---|
| 1 | P0 | Tried `winget install` for uv/make; it hung on a hidden prompt for 5 min | Orchestrator noticed no progress | Switched to uv's official standalone installer. make isn't needed locally (CI runs on Linux) |
| 2 | P0 | Issued an `rmdir` of an empty folder that the safety check flagged | Claude Code safety check | Dropped the step; create-next-app accepts an empty dir |
| 3 | P2 | Fixture agent labelled the D35 typo merchant (`HOEM DEPOT`) as `auto`, but the catalog says auto only if the fuzzy score clears the threshold | Orchestrator label review against plan 04 | Label corrected to the engine's documented behaviour (fuzzy match → review) |
