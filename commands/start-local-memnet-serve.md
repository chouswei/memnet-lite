---
name: start-local-memnet-serve
description: Start optional local memnet-llm IPC serve for MemNet Lite. Solo default is in-process memnet-mcp; use this only when local workers must share one graph.
---

# Start local MemNet serve (optional)

MemNet Lite's Cursor face (`mcp.json`) launches `mcp/launch-memnet-mcp.py`, which execs **`memnet-mcp`** in-process. That is enough for a single agent. Start a local serve only when several local processes must share one graph.

## Host

```bash
pip install 'memnet-llm[mcp]>=0.19,<0.20'
```

Python ≥ 3.11. Pin stays on **0.19.x**. Do not claim 1.0.

## IPC (preferred when serve is needed)

```bash
export MEMNET_IPC_SOCKET="${MEMNET_IPC_SOCKET:-/tmp/memnet.sock}"
memnet serve --ipc
```

`MEMNET_IPC_SOCKET` is **operator IPC** (a socket path). It is not a marketplace secret. Do not put it in plugin `variables`. Clients that should join this graph need the **same** env value.

Then restart the `memnet-lite` MCP server in Cursor so `memnet-mcp` inherits the env (or set it only in the operator shell that launches Cursor).

## TCP fallback (loopback only)

```bash
memnet serve
```

Default is loopback TCP (`127.0.0.1:18765` in current `memnet-llm` 0.19.x). Lite MUST stay local. Do not teach LAN bind, Bearer HTTP, or tip-house URLs as this plugin's face.

## Health

1. `serve_status` — TCP probe. Under default in-process, `running` may be false; that is not a Lite failure.
2. If you started `--ipc` / TCP, confirm the socket or loopback port is the one this operator set.
3. Continue with skill `memnet-lite-session`: `session_open` → `pin_map` under caps → `mutate`.

## MUST NOT

- Treat this command as required for solo in-process `memnet-mcp`.
- Substitute tip MemNet or SysMLEdge for this local host.
- Write tokens, passwords, or marketplace secrets into tracked files.
