# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-10-01

### Changed

- Marketplace manifest parity with Endleaf: `minClientVersions`, InkMirage author + email, `logo`, `category` / `tags` / `keywords`, explicit `mcpServers` and `skills` paths. Author name is English **InkMirage** only (no `variables` / secrets).
- Default `mcp.json` launches `python3` + `${CURSOR_PLUGIN_ROOT}/mcp/launch-memnet-mcp.py` (PATH `memnet-mcp` then `uvx`; exit 127 if missing). PATH `memnet-mcp` remains a documented alternate.

### Added

- `assets/logo.svg` marketplace mark (abstract graph / memory; not the Endleaf logo).

## [0.1.0] - 2026-10-01

### Added

- Public SSOT for **MemNet Lite**: Cursor plugin face (`memnet-lite` v0.1.0) over a local `memnet-llm[mcp]` host.
- `mcp.json` invokes the real `memnet-mcp` console script (PyPI `memnet-llm` 0.19.x). No stub graph tools.
- `mcp/launch-memnet-mcp.py` execs `memnet-mcp` from PATH, then `uvx --from 'memnet-llm[mcp]' memnet-mcp`; exits 127 if both are missing.
- Command `start-local-memnet-serve` for optional local IPC serve (`MEMNET_IPC_SOCKET` is operator IPC, not a marketplace secret).
- Rule `memnet-lite-local-first`: plugin = face, `memnet-llm` = host; tip ≠ face; not SysMLEdge.
- Skill `memnet-lite-session`: serve/health → `session_open` → `pin_map` under caps → `mutate` with truncation honesty.
