---
name: memnet-lite-multitask
description: >-
  Shared MemNet Lite session under Multitask / parallel Task workers; one
  mission session id in every worker prompt; local shared serve (not
  in-process). Use when Multitask Mode is on or background workers must
  share one graph. Not tip MemNet. Not SysMLEdge.
---

# MemNet Lite — shared session under Multitask

Wave protocol (atom cards, disjoint, spawn, end turn, checkpoint) lives in **memnet-lite-async-checkpoint**. This skill owns the **shared MemNet Lite session** under Multitask / Task. Pair with **memnet-lite-session** (solo loop, in-process default).

**Face:** this plugin (`memnet-lite`). **Host:** local `memnet-llm[mcp]` 0.19.x. **tip ≠ face.** Chat is never mission SSOT.

MUST NOT require tip MemNet, invite keys, OAuth, SysMLEdge, or product `sysmledge` MCP.

## When to load

| Signal | Action |
|--------|--------|
| Multitask Mode on, or Task / background workers that share a graph | This skill + **memnet-lite-async-checkpoint** |
| Spawning Task workers | Parent checklist below; pass `session=` in every worker prompt |
| Single-agent goldfish | **memnet-lite-session** only — default in-process MCP is fine |

## Transport (Lite truth)

| Transport | When |
|-----------|------|
| **MCP in-process** (plugin `memnet-mcp` stdio) | **OK** for a single agent. See **memnet-lite-session**. |
| **Local shared host** — `memnet serve` with IPC (`MEMNET_IPC_SOCKET`) or local streamable-http **bridged to that serve** | **MUST** when Multitask / parallel workers share one graph. Command **start-local-memnet-serve**. |
| Isolated in-process MCP **per worker** | **MUST NOT** — each process gets its own graph. |
| Tip MemNet / invite keys / OAuth / house HTTP MCP | **MUST NOT** — tip ≠ face. Lite stays local-first. |

`MEMNET_IPC_SOCKET` is operator IPC (a socket path), not a marketplace secret. Probe with `serve_status` before delegating if uncertain. If MemNet tools are absent: skip MemNet; plain Markdown only.

## Parent coordinator

### MUST

- `session_open` / `session_load` **one** mission `session` id; pass it in every worker prompt.
- Mint and own **`TSK_*`** / **`USR_*`**: `status=active` → `status=settled`; optional `led_to_success` edges. Mint/settle from **pin_map**, not from chat.
- Self-contained worker prompts: session id, anchor ids, write scope (subgraph or relation types), return shape.
- After Bind-ready cards: spawn **one** background worker **per** disjoint atom in the **same** message. Protocol: **memnet-lite-async-checkpoint**.
- **End the turn** after background spawn — no poll, no await.
- Next coordinator turn: **`pin_map` first**; act from the refreshed slice — do not redo worker investigation from chat.
- Keep overlapping files / locators **serial**; parallel only when atom scopes are disjoint.

### MUST NOT

- Treat chat, tool transcripts, or sub-agent prose as durable mission state.
- Settle `TSK_*` / `USR_*` from worker chat — only from shared-session pin-map facts.
- Use isolated in-process MCP for a shared mission.
- Collapse Bind-ready disjoint atoms into Cursor Multitask "one coherent worker".
- Bundle Bind + Implement in one worker.
- Run parallel workers on the **same** anchor slice. Prefer **serialize overlapping writes**.

## Worker agent

### MUST

- Use the parent's **session id**; **`pin_map` first** every turn (caps + truncation honesty: **memnet-lite-session**, **memnet-lite-atomize**).
- Copy assigned ids from pin map — **MUST NOT** invent ids the parent already minted.
- Mutate only under the **assigned subgraph** (anchors + relations in the prompt).
- Return a concise result; durable facts live in MemNet rows (`mutate` then `pin_map`).

### MUST NOT

- Open a different session unless explicitly assigned.
- Use a private in-process MCP when the parent uses the shared local serve.
- Settle parent-owned `TSK_*` / `USR_*` unless delegated.

## Overlapping writes

Prefer **serial** waves when scopes share a write-path, write-locator, live host, or MemNet node.

If the 0.19.x catalog exposes `reserve` / RSV, treat it as **optional** neighbourhood locking — do not claim ACL, session roles, or RSV as fully productized. MUST NOT skip Bind's disjoint test because reserve exists.

## Anti-patterns (Lite)

| Anti-pattern | Why it fails |
|--------------|--------------|
| Chat as SSOT for ids / mission state | Parent and workers diverge |
| Isolated in-process MCP under Multitask | Each process gets its own graph |
| Tip MemNet / invite / OAuth as Lite transport | tip ≠ face; Lite is local-first |
| Parent polls or re-runs worker work | Token waste; violates turn boundary |
| Collapse Bind-ready atoms into one worker | Violates one-worker-per-disjoint-atom spawn |
| Bundle Bind + Implement | Collapses roles; Bind must finish before Implement |
| Worker mints duplicate `TSK_*` | Parent owns task lifecycle |
| Teaching ACL / RSV as required | Not assumed productized on 0.19.x; serialize overlapping writes |
| SysMLEdge product Multitask as required | Different product; not this face |
| Host pin 0.4.x / engine-repo MN-REQ-12 tables | Outdated pack; Lite host is `memnet-llm` **0.19.x** |

## Related

| Skill / command | Role |
|-----------------|------|
| **memnet-lite-async-checkpoint** | Waves, atom cards, spawn, end turn, checkpoint |
| **memnet-lite-session** | Solo loop; in-process default |
| **memnet-lite-atomize** | Graph grain; truncation honesty |
| **memnet-lite-ssot** | Session = design SSOT; git = files |
| **start-local-memnet-serve** | Optional local IPC/`memnet serve` for a shared graph |
