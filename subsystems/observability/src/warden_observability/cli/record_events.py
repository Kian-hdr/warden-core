"""Validate stdin JSON Lines and write an exclusive event log."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..pi_events import PipelineEventWriter, parse_pipeline_event_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        with PipelineEventWriter(args.output) as writer:
            for line_number, line in enumerate(sys.stdin, start=1):
                if not line.strip():
                    continue
                try:
                    writer.write(parse_pipeline_event_json(line))
                except (KeyError, TypeError, ValueError) as exc:
                    parser.error(f"event line {line_number}: {exc}")
    except OSError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
