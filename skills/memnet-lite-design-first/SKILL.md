---
name: memnet-lite-design-first
description: >-
  Invent system design in the local MemNet Lite graph before writing repo
  code. SysML v2 MBSE ideas (packages, parts, requirements, connections,
  behaviour / actions / states) as MemNet kinds — not SysMLEdge tools.
  Use when structuring a repo in-session.
---

# MemNet Lite — design first

**Inspiration:** SysML v2 **MBSE mindset** — decomposition, requirements, connections, **and behaviour** — not SysML text syntax and not a modelling GUI.

**Face:** this plugin (`memnet-lite`). **Host:** local `memnet-mcp`. **tip ≠ face.** This is a **MemNet Lite local graph**, **not** SysMLEdge. MUST NOT call `propose` / `rev_status` / `gql` / product `pin_map` on `sysmledge` from this skill.

Lite does **not** require `.sysml` files. Graph atoms are enough. Optional later Path-B `ingest_sysml` is out of scope here.

Loop glue: **memnet-lite-session**. Atom grain: **memnet-lite-atomize**.

## SSOT split (once)

**MemNet Lite session = SSOT for system design** (architecture, behaviour, requirements, decisions). **Git / repo tree = SSOT for files.** Code, docs, and PRs trail the graph: pin → mutate → re-pin → then implement. Rule: `rules/memnet-lite-ssot.mdc`. MUST NOT keep a parallel design only in Markdown or chat.

## Contrast: coding-first vs design-first

| Coding-first | Design-first (this skill) |
|--------------|---------------------------|
| Grep / invent architecture in chat, then maybe pin | Open session → pin → invent `PKG`/`PRT`/`REQ`/`CON`/`BEH` in the graph |
| README or PR body as the design | `mutate` then implement files that allocate to those parts and behaviours |
| Code first, then reverse-fit behaviour | Structure **and** behaviour **and** reqs **and** interconnection in the graph **before** code |

## Kinds (host SCHEMA — already supported)

Declare at `session_open` (`map_lines`) **before** first mutate. Schema is frozen at open. These are MemNet kinds, not SysMLEdge qnames:

```text
SCHEMA PKG ; fields=qname kind status recycle
SCHEMA PRT ; fields=name kind role status recycle
SCHEMA POR ; fields=name kind dir typeRef status recycle
SCHEMA CON ; fields=name kind ends status recycle
SCHEMA REQ ; fields=requirementId text status recycle
SCHEMA BEH ; fields=name kind status recycle
SCHEMA ACT ; fields=name kind status recycle
SCHEMA STA ; fields=name kind status recycle
SCHEMA CLM ; fields=type code recycle
SCHEMA TSK ; fields=goal status recycle
SCHEMA USR ; fields=code recycle
```

| SysML v2 idea | MemNet kind | Role in Lite |
|---------------|-------------|--------------|
| Package / namespace | `PKG` | Decomposition container (`qname`) |
| Part def / usage | `PRT` | Structure (a thing in the system) |
| Port | `POR` | Interface on a part (`dir`, `typeRef`) |
| Connection / link | `CON` | Interconnection (ends named; edges to ports/parts) |
| Requirement | `REQ` | SHALL-class intent (`requirementId` + short `text`) |
| Behaviour / activity / use case | `BEH` | Behaviour-level intent (`name` + short `kind`/`status`) |
| Action / step | `ACT` | One step inside a `BEH` (optional; see split rule) |
| State | `STA` | One state (optional; see split rule) |
| Satisfy | edge `satisfies` | `PRT` → `REQ` and `BEH` → `REQ` (not an id-list on the node) |
| Allocate | edge `allocatedTo` | `BEH` → `PRT` |
| Realise | edge `realizes` | `PRT` → `BEH` |
| Nested part / step / state | edge `declaredIn` / `owns` | Membership via **edges** (`ACT` → `BEH`, `STA` → `BEH` or `PRT`, `PRT` → `PKG`) |

`BEH` is **first-class**: invent it in the same loop as structure, reqs, and interconnection. Prefer few kinds with clear cues over a SysML mirror. `ACT` / `STA` stay optional.

**When to split:** default is one `BEH` per named behaviour (cue on `BEH.name`). Split to `ACT` when distinct steps need their own edges (to ports, reqs, or other acts) — one action per atom, `ACT` `-[:declaredIn]->` parent `BEH`. Split to `STA` when states need their own transitions — one state per atom; do not dump a state machine into one `BEH` field. If the behaviour is one short intent with no step-level edges, stay on `BEH` alone.

Extend SCHEMA only when you will mutate that kind. Port–port host convention is `BIND`; node–node uses typed rels. Set `allow_new_relation=true` when rel types are outside the default vocabulary.

## Loop

```text
session_open(map) → pin_map (caps) → invent PKG/PRT/REQ/CON/POR/BEH
  → mutate sparse (ACT/STA when splitting) → pin_map → then write repo code
```

1. `serve_status` then `session_open` with the map above (plus `CLM`/`TSK`/`USR` as needed).
2. `pin_map` under caps (`depth=2`, `max_rows=50`). Empty cue = outline. Truncation mark → incomplete; tighten cue. **memnet-lite-atomize**.
3. Invent in the **session**, not in a design Markdown file. Structure, behaviour, reqs, and interconnection land together.
4. Sparse `mutate`. Re-`pin_map`. Copy locators from the Shape.
5. Implement files that realise those parts and behaviours. Git remains file SSOT; do not skip the graph.

```cypher
CREATE (pkg:PKG {qname: 'LiteDemo', kind: 'root', status: 'active', recycle: 'persistent'})
CREATE (p:PRT {name: 'Controller', kind: 'partUsage', role: 'compute', status: 'active', recycle: 'persistent'})
CREATE (por:POR {name: 'cmd_in', kind: 'portUsage', dir: 'in', typeRef: 'Cmd', status: 'active', recycle: 'persistent'})
CREATE (r:REQ {requirementId: 'REQ-01', text: 'Accept local commands', status: 'active', recycle: 'persistent'})
CREATE (b:BEH {name: 'AcceptCommand', kind: 'activity', status: 'active', recycle: 'persistent'})
CREATE (a:ACT {name: 'ParseCmd', kind: 'action', status: 'active', recycle: 'persistent'})
CREATE (t:TSK {goal: 'Design LiteDemo before code', status: 'in_progress', recycle: 'persistent'})
MATCH (p:PRT {name: 'Controller'}), (pkg:PKG {qname: 'LiteDemo'})
CREATE (p)-[:declaredIn]->(pkg)
MATCH (p:PRT {name: 'Controller'}), (por:POR {name: 'cmd_in'})
CREATE (p)-[:hasPort]->(por)
MATCH (p:PRT {name: 'Controller'}), (r:REQ {requirementId: 'REQ-01'})
CREATE (p)-[:satisfies]->(r)
MATCH (b:BEH {name: 'AcceptCommand'}), (p:PRT {name: 'Controller'})
CREATE (b)-[:allocatedTo]->(p)
MATCH (b:BEH {name: 'AcceptCommand'}), (r:REQ {requirementId: 'REQ-01'})
CREATE (b)-[:satisfies]->(r)
MATCH (p:PRT {name: 'Controller'}), (b:BEH {name: 'AcceptCommand'})
CREATE (p)-[:realizes]->(b)
MATCH (a:ACT {name: 'ParseCmd'}), (b:BEH {name: 'AcceptCommand'})
CREATE (a)-[:declaredIn]->(b)
MATCH (t:TSK {goal: 'Design LiteDemo before code'}), (pkg:PKG {qname: 'LiteDemo'})
CREATE (t)-[:owns]->(pkg)
```

Cue next turn on `PKG.qname`, `PRT.name`, `REQ.requirementId`, or `BEH.name` — not a chat recap.

## MUST NOT

- Route model work through SysMLEdge (`propose` / `rev_status` / `gql` on `sysmledge`).
- Require SysML v2 text files for Lite.
- Code the repo first and reverse-fit a graph as theatre.
- Reverse-fit behaviour only after coding.
- Dump a design novel into one `CLM`, one `REQ.text`, or one `BEH`.
- Treat tip MemNet as this face.
- Invent fake MCP tools. Host pin is `memnet-llm` **0.19.x**.
