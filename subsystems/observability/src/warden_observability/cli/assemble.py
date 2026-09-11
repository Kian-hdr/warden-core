"""Assemble local pipeline and resource logs into a versioned capture."""

from __future__ import annotations

import argparse
from pathlib import Path

from ..compute_gate import assess_pi_compute_gate
from ..pi_capture import assemble_pi_benchmark_capture_from_files
from .common import ensure_available, json_text, load_limits, write_new


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("events", type=Path)
    parser.add_argument("resources", type=Path)
    parser.add_argument("--capture-output", type=Path, required=True)
    parser.add_argument("--assessment-output", type=Path)
    parser.add_argument("--limits", type=Path, help="JSON overrides for numeric assessment limits")
    args = parser.parse_args()
    try:
        ensure_available(args.capture_output, args.assessment_output)
        run = assemble_pi_benchmark_capture_from_files(args.metadata, args.events, args.resources)
        assessment = assess_pi_compute_gate(run, load_limits(args.limits))
        capture_payload = json_text(run.to_dict())
        assessment_payload = json_text(assessment.to_dict())
        write_new(args.capture_output, capture_payload)
        if args.assessment_output is not None:
            write_new(args.assessment_output, assessment_payload)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(assessment_payload, end="")
    return 0 if assessment.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
