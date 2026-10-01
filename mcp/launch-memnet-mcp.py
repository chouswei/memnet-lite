#!/usr/bin/env python3
"""Exec the real memnet-mcp host; exit 127 if it is not available.

PATH first, then uvx --from 'memnet-llm[mcp]' memnet-mcp.
Does not implement graph tools.
"""

from __future__ import annotations

import os
import shutil
import sys

_MISSING = (
    "memnet-mcp not found on PATH and uvx fallback failed. "
    "Install the host: pip install 'memnet-llm[mcp]>=0.19,<0.20' "
    "or run: uvx --from 'memnet-llm[mcp]' memnet-mcp\n"
)


def main() -> int:
    argv = sys.argv[1:]
    path_bin = shutil.which("memnet-mcp")
    if path_bin:
        try:
            os.execvp(path_bin, [path_bin, *argv])
        except OSError as exc:
            sys.stderr.write(f"failed to exec {path_bin}: {exc}\n")
            return 127

    uvx = shutil.which("uvx")
    if uvx:
        try:
            os.execvp(
                uvx,
                [uvx, "--from", "memnet-llm[mcp]", "memnet-mcp", *argv],
            )
        except OSError as exc:
            sys.stderr.write(f"failed to exec uvx memnet-mcp: {exc}\n")
            return 127

    sys.stderr.write(_MISSING)
    return 127


if __name__ == "__main__":
    raise SystemExit(main())
