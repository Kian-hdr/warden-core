"""Assess an existing pipeline capture using declared measurement limits."""

from __future__ import annotations

import argparse
from pathlib import Path

from ..compute_gate import PiBenchmarkRun, assess_pi_compute_gate
from .common import ensure_available, json_text, load_limits, write_new


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limits", type=Path, help="JSON overrides for numeric assessment limits")
    args = parser.parse_args()
    try:
        ensure_available(args.output)
        assessment = assess_pi_compute_gate(
            PiBenchmarkRun.load(args.capture), load_limits(args.limits)
        )
        payload = json_text(assessment.to_dict())
        if args.output is not None:
            write_new(args.output, payload)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(payload, end="")
    return 0 if assessment.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
