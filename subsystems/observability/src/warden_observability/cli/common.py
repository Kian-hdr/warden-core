"""Shared command-line file handling."""

from __future__ import annotations

import json
from pathlib import Path

from ..compute_gate import ComputeGateLimits


def json_text(value: object) -> str:
    return json.dumps(value, indent=2, allow_nan=False) + "\n"


def ensure_available(*paths: Path | None) -> None:
    selected = [path.resolve() for path in paths if path is not None]
    if len(set(selected)) != len(selected):
        raise ValueError("output paths must be distinct")
    for path in selected:
        if path.exists():
            raise FileExistsError(f"output already exists: {path}")


def write_new(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(payload)


def load_limits(path: Path | None) -> ComputeGateLimits:
    if path is None:
        return ComputeGateLimits()
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError("limits must be an object")
    return ComputeGateLimits(**value)
