# MCP face (this plugin) vs host (`memnet-llm`)

This directory is **Cursor wiring**, not a graph engine. Graph tools come from the real host: console script **`memnet-mcp`** in PyPI extra **`memnet-llm[mcp]`** (0.19.x). Do not add stub `pin_map` / `mutate` servers here.

**tip ≠ face.** This plugin is the solo-user **local face**. It is not tip MemNet (BU house HTTP MCP) and not SysMLEdge (`sysmledge`).

## Preferred launch (what `mcp.json` uses)

Install the host, then let Cursor run the plugin launcher:

```bash
pip install 'memnet-llm[mcp]>=0.19,<0.20'
```

```json
{
  "mcpServers": {
    "memnet-lite": {
      "command": "python3",
      "args": ["${CURSOR_PLUGIN_ROOT}/mcp/launch-memnet-mcp.py"]
    }
  }
}
```

`${CURSOR_PLUGIN_ROOT}` is the Cursor plugin convention (install path). Cursor expands it in `command`, `args`, `env`, and `cwd`. It does **not** expand the Agent Plugins `${PLUGIN_ROOT}` token in `mcp.json`.

`launch-memnet-mcp.py` tries `memnet-mcp` on `PATH`, then `uvx --from 'memnet-llm[mcp]' memnet-mcp`, then **exits 127**. Default transport is **stdio in-process**. A solo Cursor agent does not need `memnet serve`.

## Alternate: PATH `memnet-mcp`

If the operator already has the console script on `PATH`, they may launch it directly (private MCP entry or a shell), instead of the plugin default:

```bash
memnet-mcp
# or: uvx --from 'memnet-llm[mcp]' memnet-mcp
```

## Optional operator IPC (not a plugin secret)

`MEMNET_IPC_SOCKET` is a **local filesystem path** for `memnet serve --ipc`. It is not a marketplace variable and MUST NOT be declared in `.cursor-plugin/plugin.json` `variables`. Set it in the operator shell (or a private, untracked env) when sharing one graph across local workers. See `commands/start-local-memnet-serve.md`.

## Host SSOT

Engine + generic MCP live in [memnet-llm](https://pypi.org/project/memnet-llm/) / the MemNet checkout. This repo does not vendor that code.
