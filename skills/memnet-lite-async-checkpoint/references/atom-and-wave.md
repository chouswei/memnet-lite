# Atom cards and waves

Bind-ready means a list of atom cards. Missing fields means not ready.

Lite: pass the parent's **session=** in every worker prompt. MUST NOT pass tip URLs, invite keys, or SysMLEdge `projectId@rev`.

## Atom card (MUST)

```
id: A2
wave: 1
order: 1
role: Implement
model_family: Gemini flash high
scope:
  paths: [parts/foo/bar.py]
  locators: [PRT.name=Controller]
  hosts: []
  memnet_ids: []
proof:
  cmd: python -m pytest parts/foo -q
  pass_if: exit 0
return: files_changed, proof_tail, blockers
must_not: [edit other paths, settle TSK_*]
```

`wave` is the parallel group. `order` sequences atoms that are not disjoint (later wave) or a serial successor after a named proof.

`model_family` is a **family + tier** label for User Rules **Model by role** — not a pinned product version. MUST NOT write FAST / `*-fast` or a vendor patch version here.

Worker `prompt` is this card plus: Lite `session=` if any; write only inside `scope`; return the contract below.

`scope.locators` are MemNet Lite cues (kind + property), not SysMLEdge qnames. `scope.paths` are git paths (file SSOT).

## Worker return (MUST)

```
atom_id: A2
status: pass | fail | blocked
files_changed:
proof_cmd:
proof_tail:
blockers:
```

Durable facts live in the shared session (`mutate` then `pin_map`), not in this return block alone.

## Disjoint (same wave)

Two atoms may share a wave only if they share **none** of: a write-path, a write-locator, a live host they mutate, a MemNet node they mutate. Read-only overlap is allowed.

If any pair overlaps on a write, Bind MUST raise the later atom's `wave`. MUST NOT put overlapping writes in one wave and hope the workers serialise. Prefer **serialize overlapping writes**. Optional host `reserve` / RSV (if the 0.19.x catalog exposes it) is not a licence to skip that rule — see **memnet-lite-multitask**.

## Ready set

Ready atoms = unsettled cards whose `wave` equals the smallest unsettled `wave`, and whose pairwise scopes are disjoint (true by construction if Bind followed the rule). Spawn that whole set in one parent message.

## Anti-patterns

| Fail | Why |
|------|-----|
| One Task prompt "do A then B" | Collapses atoms; Multitask default |
| Implement before Bind-ready cards | No disjoint test, no proof |
| Parent Implements after tagging Implement | Skips the role |
| Resume worker onto a new atom | Hidden bundling |
| Proof = "looks good" | Not a command with `pass_if` |
| Deploy atom authors files | Split: Implement then Deploy |
| `projectId@rev` / tip URL in the prompt | Wrong product; Lite is local session= |
