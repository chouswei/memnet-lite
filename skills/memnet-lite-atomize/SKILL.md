---
name: memnet-lite-atomize
description: >-
  Atomise prose into short MemNet Lite graph atoms (CLM/TSK/USR/SYM and
  siblings) for mutate. Use when turning chat or notes into CREATE/MATCH
  wire; when a pin is bloated or truncated; not for mem0-style dumps.
---

# MemNet Lite — atomise

**Face:** this plugin. **Host:** local `memnet-mcp` (`memnet-llm[mcp]` 0.19.x). **tip ≠ face.** Not SysMLEdge.

Session loop lives in **memnet-lite-session**. This skill is the **hard teach** for graph grain.

## What an atom is

One **idea** per node. Membership is **edges**, not id-lists in properties. Fields stay short (codes, paths, goals) — not paragraphs.

| Kind | One atom means | Cue on |
|------|----------------|--------|
| `CLM` | one claim / decision | `code` / `type` |
| `TSK` | one work unit | `goal` |
| `USR` | one operator constraint | `code` |
| `SYM` | one symbol / locator | `name` + `path` |
| `MOD` | one file | `path` |
| `RUL` | one policy | `code` |

Extend `session_open` `map_lines` **before** first mutate of a new kind. Schema is frozen at open. Design kinds under the triad (requirements `REQ`; structures `PKG` / `PRT` / `POR` / `CON`; behaviours `BEH` / `ACT` / `STA`): **memnet-lite-design-first**. Code index: **memnet-lite-repo-snapshot**.

## Prose → `mutate` wire

1. Split the paragraph into ideas. Drop scrapbook colour (chat recap, mem0-style “remember this blob”).
2. Name kinds + locators. Prefer labels+properties already on the last `pin_map`.
3. `CREATE` new atoms; `MATCH` existing ones; `CREATE` typed rels. One `mutate` call, many `wire_lines`.
4. Re-`pin_map`. If `## Truncation truncated=true`, the Shape is **incomplete** — filter the cue; do not claim a full extract.

```cypher
CREATE (t:TSK {goal: 'Pin local host loop', status: 'in_progress', recycle: 'persistent'})
CREATE (c:CLM {type: 'decision', code: 'plugin is face; memnet-llm is host', recycle: 'persistent'})
CREATE (u:USR {code: 'solo in-process default', recycle: 'persistent'})
MATCH (c:CLM {code: 'plugin is face; memnet-llm is host'}), (t:TSK {goal: 'Pin local host loop'})
CREATE (c)-[:documents]->(t)
MATCH (t:TSK {goal: 'Pin local host loop'}), (u:USR {code: 'solo in-process default'})
CREATE (t)-[:constrained_by]->(u)
```

Set `allow_new_relation=true` when the rel type is outside the host default vocabulary. leftover `add` / `update` / `id:'NEW'` are leftover — product write is `mutate`.

### Filter-out, do not silent-truncate

When the batch would overflow `pin_map` caps (`depth`, `max_rows`):

- **Filter-out:** omit out-of-cue atoms from this mutate; tighten `kind` / locators / keyword; keep caps **hard**.
- **MUST NOT** stuff leftover prose into one node so the engine clips it.
- **MUST NOT** raise `max_rows` to hide `## Truncation truncated=true`.
- Honour the mark: incomplete Shape → re-cue. Prefer a thinner neighbourhood over a dump.

## Anti-patterns

| Bad | Good |
|-----|------|
| One `CLM.code` that is a paragraph of architecture | Several `CLM` + edges |
| `members: 'a,b,c'` on a node | `CREATE (p)-[:owns]->(c)` per member |
| Paste the chat into `USR` | One constraint per `USR` |
| mem0 upsert of snippets | Sparse GQL `mutate` on a session graph |
| Chat as the design log | Atoms in MemNet (rule **memnet-lite-ssot**) |

## MUST NOT

- Chat scrapbook / mem0-style dump as graph content.
- Treat nickname `id` / `hid` / `elementId` as GraphElement identity.
- Invent stub `pin_map` / `mutate`. Use the host tools.
- Route this teach through SysMLEdge (`propose` / `rev_status`) or tip MemNet.
