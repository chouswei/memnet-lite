---
name: memnet-lite-async-checkpoint
description: >-
  Multi-wave parallel Task workers; Bind → spawn one background worker per
  disjoint atom → end turn → checkpoint. Use when the job is multi-step,
  needs parallel disjoint edits, Bind-ready atoms, or house roles
  (Architect/Bind/Diagnose/Implement/Deploy). Triggers: multi-wave, async
  checkpoint, Bind-ready atoms, parallel Task workers. Not tip MemNet.
  Not SysMLEdge.
---

# MemNet Lite — async checkpoint (multi-wave)

Parent coordinates. Workers execute **one** atom. A **checkpoint** is the next parent turn after a wave; a worker MUST NOT declare the job done.

Skip this skill when the parent can finish a short in-scope answer with its own tools.

**Face:** this plugin (`memnet-lite`). **Host:** local `memnet-llm[mcp]` 0.19.x. **tip ≠ face.**

Pairing: **memnet-lite-multitask** (shared Lite session under parallel workers). Atom schema: [references/atom-and-wave.md](references/atom-and-wave.md). Role duties: [references/roles.md](references/roles.md). Solo goldfish: **memnet-lite-session**.

MUST NOT require tip MemNet, invite keys, OAuth, SysMLEdge, or product `sysmledge` MCP. Model slugs: resolve from User Rules **Model by role** — do not pin versions in this skill; MUST NOT use FAST / `*-fast` variants.

## Route (parent)

| Signal | Next |
|--------|------|
| Unknown cause | Diagnose, then Bind |
| Complex new architecture | Architect (thin), accept, then Bind |
| Normal multi-step | Bind (plan + atom cards) |
| Short in-scope answer | Parent tools; no pipeline |

When the parent can emit Bind-ready cards, Bind **on parent** (soft: a planning-capable parent often does). Spawn a Bind worker only when the parent should not plan. MUST still emit Bind-ready atom cards before Implement. MUST NOT skip Bind because of parent family. Do not require a named vendor parent.

Parent always: mint/settle `TSK_*` / `USR_*` from the shared session (`pin_map` facts, not chat), spawn, checkpoint. Parent MUST NOT Implement, Deploy, Visual, or Web when Bind tagged those roles.

## Two phases (MUST)

**Planner phase** — at most one of Architect, Diagnose, or Bind-as-worker. Spawn it, then **end the turn**. Do not spawn Implement in the same message as a planner worker.

**Execute phase** — only after Bind-ready atom cards exist (this turn if Bind was on parent; else the Bind checkpoint). Spawn **one** background worker **per** ready disjoint atom in the **same** message. Then **end the turn**.

Cursor Multitask "one coherent worker" MUST NOT collapse those atoms. One worker only when Bind emits one atom, the next atom is serial on prior proof, or the answer is a trivial parent call.

## Spawn recipe

Protocol (MUST), independent of IDE chrome: after Bind-ready cards, start **one background worker per ready disjoint atom in the same parent message**, then **end the turn**. Do not poll. Checkpoint is the next parent turn.

When the Cursor **Task** / sub-agent surface is available, map intent to the fields it actually exposes (do not invent extras):

| Intent | Current Cursor Task field |
|--------|---------------------------|
| Distinct title | `description` — role + atom id |
| Worker type | `subagent_type` — `generalPurpose` (house roles are not Cursor types) |
| Model | `model` — slug resolved from User Rules **Model by role**; MUST NOT use FAST / `*-fast`; MUST NOT pin a product version here |
| Background | `run_in_background` — true |
| Atom | `prompt` — one atom card + return contract + Lite `session=` |
| Where | `environment` — `local` unless the operator asked for cloud |

If the IDE names these differently, keep the protocol. MUST NOT use `resume` to start a different atom. Resume the same atom only after a failed proof. MUST NOT default every atom to Implement. MUST name the resolved family when spawning.

After the spawn calls: no poll, no await-on-workers, no extra file edits. End the turn.

## Checkpoint (parent)

1. Shared-session work: **memnet-lite-multitask** — `pin_map` with `session=` first (ops only). Local shared serve when workers share one graph; in-process is **not** a shared store. tip is not this face.
2. Each finished worker: proof command produced sane output (`pass_if`). Fail → same-atom resume or re-Bind that atom. Pass → settle that atom from pin-map facts.
3. Deploy proof: live host shows the change, PIDs/markers recorded, rollback stated. Local tests are not deploy proof.
4. Remaining waves: spawn the next ready set, end the turn. None left: stop.

## Design vs files

Lite design SSOT is the local session graph (**memnet-lite-ssot**, **memnet-lite-design-first**). Architect I/O stays thin (path / graph-locator pointers). Bind fills atom scopes from the last `pin_map`. Implement edits files after Bind-ready. Git remains file SSOT.

MUST NOT require SysMLEdge `projectId@rev`, a bound desk Save, or product `sysmledge` tools.

## MUST NOT

- Treat chat or worker prose as mission SSOT.
- Collapse Bind-ready disjoint atoms into one worker.
- Teach tip MemNet as Lite transport.
- Use FAST / `*-fast` model variants in examples or spawns.
