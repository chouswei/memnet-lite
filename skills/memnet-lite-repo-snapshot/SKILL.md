---
name: memnet-lite-repo-snapshot
description: >-
  Snapshot a bounded repo slice into local MemNet Lite via host
  ingest_codebase, then pin_map the neighbourhood. Use when indexing
  files/symbols; never paste whole trees into chat.
---

# MemNet Lite — repo snapshot

**Face:** this plugin. **Host:** local `memnet-mcp` (`memnet-llm[mcp]` 0.19.x). **tip ≠ face.** Not SysMLEdge.

Loop glue: **memnet-lite-session**. Atoms: **memnet-lite-atomize**. Design-before-code: **memnet-lite-design-first**.

## Job

Index a **bounded** tree as `:MOD` (file) and `:SYM` (symbol) on the **current** Lite session, then **read** it with `pin_map`. MUST NOT paste whole trees into chat.

Git remains SSOT for **file bytes**. The session is SSOT for **what the agent pinned** about those files — not a second copy of the repo.

## Host tool

Use **`ingest_codebase`** on this host (Path-B; `MOD`/`SYM` with `path=` / `line=` / `signature=` locators). If a 0.19.x catalog names an equivalent documented ingest for code, use that — do not invent a stub indexer.

```text
ingest_codebase(path=<dir or file>, max_files=64, max_nodes=200, session=<id>)
```

Caps stay **hard**. `dry_run=true` to preview. Pass `session=` (never `session_list[0]`). SCHEMA at open MUST include at least:

```text
SCHEMA MOD ; fields=path lang recycle
SCHEMA SYM ; fields=name kind path line recycle
SCHEMA TSK ; fields=goal status recycle
```

## Loop

```text
session_open(map) → ingest_codebase(bounded path) → pin_map(neighbourhood)
  → optional sparse mutate (verified edges only) → pin_map
```

1. Scope the path (one package, not `/`). Keep `max_files` / `max_nodes` bounded.
2. Ingest. Then `pin_map` on a root `MOD.path` or the owning `TSK.goal` (`depth=2`, `max_rows=50`).
3. If stdout has `## Truncation truncated=true`, the Shape is **incomplete**. Narrow `path` / cue; MUST NOT claim a complete extract; MUST NOT paste the omitted tree into chat to “fill gaps”.
4. Verify on disk before adding `calls` / `uses`. Copy locators from the pin. **memnet-lite-atomize**.
5. Handoff: **`session_id` + a fresh `pin_map`**. MUST NOT dump S or the file tree into the next prompt.

Empty cue = session outline. CueConflict (`|Q|>1`): retarget; do not pick a root at random.

## MUST NOT

- Paste whole trees, `find` dumps, or ingest stdout into chat as the working set.
- Soften caps to hide truncation.
- Treat ingest as a substitute for grep/LSP or for design-first (triad **requirements, structures, behaviours**).
- Call SysMLEdge `propose` / `rev_status` / `gql`, or tip MemNet, as this snapshot path.
- Invent fake ingest tools. Host pin is `memnet-llm` **0.19.x**.
