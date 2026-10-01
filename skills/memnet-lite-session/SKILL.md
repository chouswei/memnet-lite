---
name: memnet-lite-session
description: >-
  Local MemNet Lite session loop on memnet-llm[mcp]. Use when this plugin's
  memnet-lite MCP is in the catalog: health, session_open, pin_map under caps,
  mutate. Hard teaches: atomize, design-first, repo-snapshot. Not tip MemNet.
  Not SysMLEdge.
---

# MemNet Lite session (local host)

**Face:** this plugin (`memnet-lite`). **Host:** local `memnet-mcp` from `memnet-llm[mcp]` 0.19.x. **tip ≠ face.** If SysMLEdge tools are present, they are a different product — do not route model work through this skill.

If `memnet-lite` / `memnet-mcp` tools are **absent** from the catalog: skip this loop; plain Markdown only. Do not invent tool calls.

## Hard teaches (open the specialist — do not paste it here)

| Skill | When |
|-------|------|
| **memnet-lite-atomize** | Prose → short atoms; edges not id-lists; filter-out vs silent truncate; truncation marks |
| **memnet-lite-design-first** | Invent `PKG`/`PRT`/`REQ`/`CON`/`BEH` (optional `ACT`/`STA`) in the graph **before** repo code (SysML v2 MBSE *ideas*, not SysMLEdge) |
| **memnet-lite-repo-snapshot** | Bounded host `ingest_codebase`, then `pin_map`; MUST NOT paste trees into chat |

Design SSOT: rule **memnet-lite-ssot** (graph = system design; git = files).

## Loop

```text
serve/health → session_open → pin_map(under caps) → reason → mutate → pin_map
```

### 1. Serve / health

Call `serve_status` first.

- Default Lite is **in-process**. `running` false is normal; the MCP process **is** the host.
- If the operator started `memnet serve --ipc`, `MEMNET_IPC_SOCKET` is a local socket path (not a plugin secret). Do not require TCP.
- Envelope tools (except `serve_status`) return JSON `{exit_code, stdout, stderr, session_id, errors}`. Parse **`stdout`** for graph text.

### 2. `session_open`

Open **this** operator's session. Schema is frozen at open. Missing map → `no_map`. Unknown kind → `unknown_tag`.

Pass `map_lines` covering at least `CLM`, `TSK`, `USR`, `SYM` (extend before first mutate if you will write more kinds — design-first and repo-snapshot list theirs):

```text
SCHEMA CLM ; fields=type code recycle
SCHEMA TSK ; fields=goal status recycle
SCHEMA USR ; fields=code recycle
SCHEMA SYM ; fields=path line recycle
```

Copy `session_id` from the envelope. Pass `session=` on every later call. MUST NOT adopt `session_list[0]` or a foreign catalog. Engine TTL is 1..1440 minutes. Durable path is `session_save` to a dated file, not chat.

Optional `seed_lines` are openCypher-shaped. Set `allow_new_relation=true` when seed uses relation types outside the default vocabulary.

### 3. `pin_map` under caps

Cue, then a **bounded** neighbourhood. Defaults: `depth=2`, `max_rows=50`. Raise depth only if the slice is too thin. Keep `max_rows` bounded.

```text
pin_map(kind="TSK", locators=["goal=<cue>"], depth=2, max_rows=50, session=<id>)
```

If the ego is unknown: `find` (hard `limit`) then `pin_map` from labels+properties. Empty cue = session outline. Optional `view=shell` | `interior` on a **seed**, not on the outline.

Drop the prior map from the next prompt. Product read is `pin_map`. leftover `query_warm` is leftover.

**Truncation:** when stdout includes `## Truncation truncated=true`, the Shape is **incomplete**. Tighten cue. Grain and filter-out: **memnet-lite-atomize**. MUST NOT soften `max_rows` to hide the clip. Shaped emit MUST NOT be read as identity via `hid` / `_memnet_hid` / `elementId`. Nickname property `id` is not GraphElement identity.

CueConflict (`|Q|>1`): retarget the cue. MUST NOT mutate a foreign neighbourhood.

### 4. `mutate`

Product write: `mutate` with `wire_lines` (openCypher-shaped CREATE / MATCH / SET / DELETE). leftover `add` / `update` wrap the same envelope — do not teach them as TARGET. Atom shape and membership: **memnet-lite-atomize**. Then `pin_map` again.

Copy locators from the last `pin_map`. After persistent CLM / USR / SYM / TSK facts, `session_save` to a new dated file when durability is needed. Handoff is `session_id` plus a fresh `pin_map`.

## Caps (Lite)

| Control | Lite practice |
|---------|----------------|
| `depth` | 2 unless the slice is too thin |
| `max_rows` | 50 unless the operator raises it; cap stays **hard** |
| Truncation mark | incomplete Shape; re-cue (**memnet-lite-atomize**) |
| `housekeep_stats` | counts only; do not prune a mutate-maintained catalog as "orphans" |

## MUST NOT

- Stub or fake `pin_map` / `mutate` in this plugin.
- Use this skill as SysMLEdge (`propose` / `rev_status`) or as tip MemNet.
- Require marketplace secrets. `MEMNET_IPC_SOCKET` is optional operator IPC.
- Claim host **1.0**. Pin `memnet-llm` 0.19.x.
- Put the graph in chat; handoff is `session_id` plus a fresh `pin_map`.
- Duplicate the three specialist teaches in this file.
