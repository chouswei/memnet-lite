# MemNet Lite

Solo-user **local memory graph** for Cursor. This repository is the public SSOT for the **plugin face**: MCP client wiring, one rule, one skill, one serve command. The **host** is PyPI [`memnet-llm[mcp]`](https://pypi.org/project/memnet-llm/) 0.19.x (`memnet-mcp`). This is not tip MemNet and not SysMLEdge.

**Operator:** 衍跡 InkMirage (InkMirage). **Plugin:** `memnet-lite` **v0.1.0**. **Licence:** MIT.

## Architecture (plugin = face, memnet-llm = host)

```text
Cursor agent
  └─ this plugin (face)
       ├─ mcp.json          → stdio command memnet-mcp
       ├─ rules / skills    → local-first loop
       └─ commands          → optional local serve
            │
            ▼
     memnet-llm[mcp] (host)
       ├─ memnet-mcp        → real pin_map / session_open / mutate
       └─ memnet engine     → session graph (in-process by default)
```

| Layer | What it is | What it is not |
|-------|------------|----------------|
| **Face** | This Cursor plugin (`memnet-lite`) | A graph engine, a stub MCP, a secret store |
| **Host** | Local `memnet-llm` + `memnet-mcp` | Tip MemNet BU house HTTP MCP |
| **Product neighbour** | SysMLEdge is a different face (`sysmledge`) | Something this plugin may substitute |

**tip ≠ face.** A remote or house MemNet MCP (historical keys such as `memnet-pi`) is a **tip**. This plugin is a **local face**. Do not use one as the other. Do not use this face as SysMLEdge (`rev_status` / `ask` / `propose`).

Default transport: **in-process stdio**. Optional local IPC: `memnet serve --ipc` with operator env `MEMNET_IPC_SOCKET` (a socket path, **not** a marketplace secret). This plugin declares **no** `variables` secrets.

## Install as a local Cursor plugin

```bash
git clone https://github.com/chouswei/memnet-lite.git ~/.cursor/plugins/local/memnet-lite
```

Or copy this checkout to that path. Cursor loads local plugins from `~/.cursor/plugins/local/<plugin-name>/`. Reload the window, then enable **MemNet Lite**.

### Host (required)

```bash
pip install 'memnet-llm[mcp]>=0.19,<0.20'
```

Python ≥ 3.11. Confirm:

```bash
command -v memnet-mcp
```

If `memnet-mcp` is not on `PATH`, use the documented fallback:

```bash
uvx --from 'memnet-llm[mcp]' memnet-mcp
```

`mcp.json` prefers the **direct** command `memnet-mcp`. `mcp/launch-memnet-mcp.py` execs PATH then that `uvx` line and **exits 127** when both are missing. See [mcp/README.md](mcp/README.md).

## Use

1. Enable the plugin so Cursor starts `memnet-mcp` (namespace from server key `memnet-lite`).
2. Follow skill **memnet-lite-session**: `serve_status` → `session_open` → `pin_map` under caps → `mutate`.
3. Start a local serve only when workers must share one graph: command **start-local-memnet-serve**.

Goldfish loop on the host (do not invent stub tools):

```text
session_open(map) → pin_map(q) → reason → mutate → pin_map
```

Pass `session=` on every tool except `serve_status`. When `pin_map` emit includes `## Truncation truncated=true`, the Shape is **incomplete** — tighten the cue; do not claim a full extract. Caps stay hard.

## Versus mem0

| | **MemNet Lite** | **mem0** |
|--|-----------------|----------|
| Job | Mission **working memory**: a named session **graph** | Long-term **memory store** (typically embeddings + retrieved snippets) |
| Read | Cue, then a bounded **shaped** `pin_map` neighbourhood | Similarity / RAG-style recall |
| Write | GQL `mutate` (CREATE / MATCH / SET / DELETE) | Extract and upsert memories |
| Host | Local `memnet-llm` process (this machine) | Commonly a hosted API plus client SDK |
| Not | A vector corpus, GraphRAG, or chat notepad | A live GQL session graph with truncation-honest pin maps |

Use MemNet Lite when the agent must **pin a neighbourhood and commit sparse graph deltas**. Use mem0-style stores when the product is **durable retrieved memories** rather than a live session graph. They are not drop-in replacements.

## Layout

```text
.cursor-plugin/plugin.json
.gitignore
CHANGELOG.md
LICENSE
README.md
mcp.json
mcp/README.md
mcp/launch-memnet-mcp.py
commands/start-local-memnet-serve.md
rules/memnet-lite-local-first.mdc
skills/memnet-lite-session/SKILL.md
```

GitHub for this SSOT is **this** public repository. Do not add Origin (Gitee/GitLab) mirrors from this tree.

## Secrets

**None** in the plugin. Do not put API keys in `mcp.json` or the manifest. Optional `MEMNET_IPC_SOCKET` is operator IPC only.

Engine playbook (host, not this face): MemNet `docs/LLM-GUIDE.md` in the `memnet-llm` / MemNet checkout.
