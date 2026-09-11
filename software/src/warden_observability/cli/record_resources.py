from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

from ..pi_resources import build_resource_sample, parse_proc_stat


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Record read-only Raspberry Pi resource evidence as JSONL"
    )
    parser.add_argument("--duration-seconds", type=float, default=1200.0)
    parser.add_argument("--interval-seconds", type=float, default=1.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if (
        not math.isfinite(args.duration_seconds)
        or not math.isfinite(args.interval_seconds)
        or args.duration_seconds <= 0.0
        or args.interval_seconds <= 0.0
    ):
        parser.error("duration and interval must be positive")
    if sys.platform != "linux":
        parser.error("Pi resource capture requires Linux")
    vcgencmd = shutil.which("vcgencmd")
    if vcgencmd is None:
        parser.error("vcgencmd is required to capture Pi power and throttle flags")

    proc_stat = Path("/proc/stat")
    meminfo = Path("/proc/meminfo")
    temperature = Path("/sys/class/thermal/thermal_zone0/temp")
    for required in (proc_stat, meminfo, temperature):
        if not required.is_file():
            parser.error(f"required resource source is missing: {required}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    previous_cpu = parse_proc_stat(proc_stat.read_text(encoding="utf-8"))
    first_record_ns = None
    next_sample = time.monotonic() + args.interval_seconds
    with args.output.open("x", encoding="utf-8") as handle:
        while True:
            remaining = next_sample - time.monotonic()
            if remaining > 0.0:
                time.sleep(remaining)
            now_ns = time.monotonic_ns()
            current_cpu = parse_proc_stat(proc_stat.read_text(encoding="utf-8"))
            throttled = subprocess.run(
                [vcgencmd, "get_throttled"],
                check=True,
                capture_output=True,
                text=True,
                timeout=2.0,
            ).stdout
            sample = build_resource_sample(
                previous_cpu=previous_cpu,
                current_cpu=current_cpu,
                meminfo_text=meminfo.read_text(encoding="utf-8"),
                temperature_text=temperature.read_text(encoding="utf-8"),
                throttled_text=throttled,
                monotonic_ns=now_ns,
            )
            handle.write(json.dumps(asdict(sample), sort_keys=True, allow_nan=False) + "\n")
            handle.flush()
            previous_cpu = current_cpu
            if first_record_ns is None:
                first_record_ns = now_ns
            elif (now_ns - first_record_ns) / 1_000_000_000.0 >= args.duration_seconds:
                break
            next_sample += args.interval_seconds

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
