from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from warden_observability.compute_gate import ResourceSample


@dataclass(frozen=True)
class CpuCounters:
    idle: int
    total: int


def parse_proc_stat(text: str) -> CpuCounters:
    first_line = text.splitlines()[0] if text.splitlines() else ""
    fields = first_line.split()
    if not fields or fields[0] != "cpu" or len(fields) < 5:
        raise ValueError("/proc/stat does not contain aggregate CPU counters")
    try:
        counters = [int(value) for value in fields[1:]]
    except ValueError as exc:
        raise ValueError("/proc/stat CPU counters must be integers") from exc
    if any(value < 0 for value in counters):
        raise ValueError("/proc/stat CPU counters must be non-negative")
    idle = counters[3] + (counters[4] if len(counters) > 4 else 0)
    return CpuCounters(idle=idle, total=sum(counters[:8]))


def cpu_utilization(previous: CpuCounters, current: CpuCounters) -> float:
    total_delta = current.total - previous.total
    idle_delta = current.idle - previous.idle
    if total_delta <= 0 or idle_delta < 0 or idle_delta > total_delta:
        raise ValueError("CPU counters are not monotonic")
    return (total_delta - idle_delta) / total_delta


def parse_meminfo_utilization(text: str) -> float:
    values: dict[str, int] = {}
    for line in text.splitlines():
        fields = line.split()
        if len(fields) >= 2 and fields[0] in {"MemTotal:", "MemAvailable:"}:
            try:
                values[fields[0]] = int(fields[1])
            except ValueError as exc:
                raise ValueError("/proc/meminfo values must be integers") from exc
    total = values.get("MemTotal:")
    available = values.get("MemAvailable:")
    if total is None or available is None or total <= 0 or not 0 <= available <= total:
        raise ValueError("/proc/meminfo is missing valid total or available memory")
    return 1.0 - available / total


def parse_temperature_c(text: str) -> float:
    try:
        raw = float(text.strip())
    except ValueError as exc:
        raise ValueError("thermal-zone temperature must be numeric") from exc
    temperature = raw / 1000.0 if abs(raw) > 500.0 else raw
    if not isfinite(temperature) or not -40.0 <= temperature <= 150.0:
        raise ValueError("thermal-zone temperature is outside the supported range")
    return temperature


def parse_get_throttled(text: str) -> tuple[bool, bool, bool]:
    prefix = "throttled="
    normalized = text.strip().lower()
    if not normalized.startswith(prefix):
        raise ValueError("vcgencmd output must begin with throttled=")
    try:
        mask = int(normalized[len(prefix) :], 0)
    except ValueError as exc:
        raise ValueError("vcgencmd throttling mask is invalid") from exc
    if mask < 0:
        raise ValueError("vcgencmd throttling mask must be non-negative")
    undervoltage = bool(mask & ((1 << 0) | (1 << 16)))
    frequency_capped = bool(mask & ((1 << 1) | (1 << 17)))
    thermal_throttled = bool(mask & ((1 << 2) | (1 << 3) | (1 << 18) | (1 << 19)))
    return undervoltage, frequency_capped, thermal_throttled


def build_resource_sample(
    *,
    previous_cpu: CpuCounters,
    current_cpu: CpuCounters,
    meminfo_text: str,
    temperature_text: str,
    throttled_text: str,
    monotonic_ns: int,
) -> ResourceSample:
    if monotonic_ns < 0:
        raise ValueError("resource timestamp must be non-negative")
    undervoltage, frequency_capped, thermal_throttled = parse_get_throttled(throttled_text)
    return ResourceSample(
        monotonic_ns=monotonic_ns,
        cpu_utilization_fraction=cpu_utilization(previous_cpu, current_cpu),
        memory_utilization_fraction=parse_meminfo_utilization(meminfo_text),
        temperature_c=parse_temperature_c(temperature_text),
        thermal_throttled=thermal_throttled,
        undervoltage_observed=undervoltage,
        frequency_capped=frequency_capped,
    )
