from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Self, TextIO


@dataclass(frozen=True)
class VioPipelineEvent:
    camera_capture_ns: int
    output_ns: int
    valid: bool
    kind: str = "vio"


@dataclass(frozen=True)
class CommandPipelineEvent:
    output_ns: int
    valid: bool
    kind: str = "command"


PipelineEvent = VioPipelineEvent | CommandPipelineEvent


def parse_pipeline_event(value: dict[str, Any]) -> PipelineEvent:
    kind = value.get("kind")
    if kind == "vio":
        event: PipelineEvent = VioPipelineEvent(
            camera_capture_ns=_integer(value, "camera_capture_ns"),
            output_ns=_integer(value, "output_ns"),
            valid=_boolean(value, "valid"),
        )
        if event.camera_capture_ns < 0:
            raise ValueError("camera capture timestamp must be non-negative")
        if event.output_ns < event.camera_capture_ns:
            raise ValueError("VIO output timestamp precedes camera capture")
    elif kind == "command":
        event = CommandPipelineEvent(
            output_ns=_integer(value, "output_ns"),
            valid=_boolean(value, "valid"),
        )
    else:
        raise ValueError(f"unknown pipeline event kind {kind!r}")
    if event.output_ns < 0:
        raise ValueError("pipeline event timestamp must be non-negative")
    return event


def parse_pipeline_event_json(line: str) -> PipelineEvent:
    try:
        value = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ValueError("pipeline event is not valid JSON") from exc
    if not isinstance(value, dict):
        raise TypeError("pipeline event must be an object")
    return parse_pipeline_event(value)


class PipelineEventWriter:
    """Write one exclusive, canonical, timing-validated pipeline event log."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._handle: TextIO = path.open("x", encoding="utf-8")
        self._last_output_ns: dict[str, int] = {}

    def write(self, event: PipelineEvent) -> None:
        parsed = parse_pipeline_event(asdict(event))
        previous = self._last_output_ns.get(parsed.kind)
        if previous is not None and parsed.output_ns <= previous:
            raise ValueError(f"{parsed.kind} output timestamps must be strictly increasing")
        self._handle.write(json.dumps(asdict(parsed), sort_keys=True, separators=(",", ":")) + "\n")
        self._handle.flush()
        self._last_output_ns[parsed.kind] = parsed.output_ns

    def close(self) -> None:
        if not self._handle.closed:
            self._handle.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def _integer(value: dict[str, Any], field: str) -> int:
    result = value[field]
    if not isinstance(result, int) or isinstance(result, bool):
        raise TypeError(f"{field} must be an integer")
    return result


def _boolean(value: dict[str, Any], field: str) -> bool:
    result = value[field]
    if not isinstance(result, bool):
        raise TypeError(f"{field} must be boolean")
    return result
