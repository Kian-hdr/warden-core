from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import Enum
from itertools import pairwise
from math import ceil, isfinite
from pathlib import Path
from typing import Any

from .validation import boolean, integer, number, object_value, records, text


class ComputeEvidenceKind(str, Enum):
    REAL_PI_RECORDED_REPLAY = "real_pi_recorded_replay"
    REAL_PI_PROPS_OFF_MOTION = "real_pi_props_off_motion"
    SYNTHETIC = "synthetic"


@dataclass(frozen=True)
class VioSample:
    camera_capture_ns: int
    output_ns: int
    valid: bool


@dataclass(frozen=True)
class CommandSample:
    output_ns: int
    valid: bool


@dataclass(frozen=True)
class ResourceSample:
    monotonic_ns: int
    cpu_utilization_fraction: float
    memory_utilization_fraction: float
    temperature_c: float
    thermal_throttled: bool
    undervoltage_observed: bool = False
    frequency_capped: bool = False


@dataclass(frozen=True)
class CaptureProvenance:
    device_inventory_id: str
    source_data_sha256: str
    pipeline_manifest_id: str
    camera_calibration_id: str
    camera_to_body_extrinsics_id: str
    timestamp_domain: str
    clock_sync_method: str
    clock_sync_verified: bool
    power_supply_id: str


@dataclass(frozen=True)
class PiBenchmarkRun:
    schema_version: int
    run_id: str
    evidence_kind: ComputeEvidenceKind
    device_model: str
    os_version: str
    vio_implementation: str
    policy_id: str
    provenance: CaptureProvenance
    vio_samples: tuple[VioSample, ...]
    command_samples: tuple[CommandSample, ...]
    resource_samples: tuple[ResourceSample, ...]

    def to_dict(self) -> dict[str, object]:
        value = asdict(self)
        value["evidence_kind"] = self.evidence_kind.value
        for field in ("vio_samples", "command_samples", "resource_samples"):
            value[field] = list(value[field])
        return value

    @classmethod
    def load(cls, path: Path) -> PiBenchmarkRun:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PiBenchmarkRun:
        data = object_value(data, "capture")
        provenance = object_value(data["provenance"], "provenance")
        run = cls(
            schema_version=integer(data, "schema_version"),
            run_id=text(data, "run_id"),
            evidence_kind=ComputeEvidenceKind(text(data, "evidence_kind")),
            device_model=text(data, "device_model"),
            os_version=text(data, "os_version"),
            vio_implementation=text(data, "vio_implementation"),
            policy_id=text(data, "policy_id"),
            provenance=CaptureProvenance(
                device_inventory_id=text(provenance, "device_inventory_id"),
                source_data_sha256=text(provenance, "source_data_sha256"),
                pipeline_manifest_id=text(provenance, "pipeline_manifest_id"),
                camera_calibration_id=text(provenance, "camera_calibration_id"),
                camera_to_body_extrinsics_id=text(provenance, "camera_to_body_extrinsics_id"),
                timestamp_domain=text(provenance, "timestamp_domain"),
                clock_sync_method=text(provenance, "clock_sync_method"),
                clock_sync_verified=boolean(provenance, "clock_sync_verified"),
                power_supply_id=text(provenance, "power_supply_id"),
            ),
            vio_samples=tuple(
                VioSample(
                    integer(item, "camera_capture_ns"),
                    integer(item, "output_ns"),
                    boolean(item, "valid"),
                )
                for item in records(data, "vio_samples")
            ),
            command_samples=tuple(
                CommandSample(integer(item, "output_ns"), boolean(item, "valid"))
                for item in records(data, "command_samples")
            ),
            resource_samples=tuple(
                ResourceSample(
                    monotonic_ns=integer(item, "monotonic_ns"),
                    cpu_utilization_fraction=number(item, "cpu_utilization_fraction"),
                    memory_utilization_fraction=number(item, "memory_utilization_fraction"),
                    temperature_c=number(item, "temperature_c"),
                    thermal_throttled=boolean(item, "thermal_throttled"),
                    undervoltage_observed=boolean(
                        {"undervoltage_observed": False, **item}, "undervoltage_observed"
                    ),
                    frequency_capped=boolean(
                        {"frequency_capped": False, **item}, "frequency_capped"
                    ),
                )
                for item in records(data, "resource_samples")
            ),
        )
        _validate_run(run)
        return run


@dataclass(frozen=True)
class ComputeGateLimits:
    minimum_vio_hz: float = 30.0
    minimum_command_hz: float = 50.0
    maximum_vio_p95_latency_ms: float = 50.0
    maximum_processing_gap_ms: float = 100.0
    minimum_duration_minutes: float = 20.0
    maximum_cpu_p95_utilization_fraction: float = 0.85
    maximum_memory_utilization_fraction: float = 0.85
    maximum_final_window_temperature_range_c: float = 5.0

    def __post_init__(self) -> None:
        for name, value in asdict(self).items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be numeric")
            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be positive and finite")
        for name in ("maximum_cpu_p95_utilization_fraction", "maximum_memory_utilization_fraction"):
            if getattr(self, name) > 1:
                raise ValueError(f"{name} must not exceed one")


@dataclass(frozen=True)
class ComputeGateAssessment:
    run_id: str
    evidence_kind: str
    duration_minutes: float
    vio_duration_minutes: float
    command_duration_minutes: float
    vio_hz: float
    command_hz: float
    vio_p95_latency_ms: float | None
    maximum_processing_gap_ms: float | None
    maximum_vio_gap_ms: float | None
    maximum_command_gap_ms: float | None
    cpu_p95_utilization_fraction: float
    maximum_memory_utilization_fraction: float
    maximum_temperature_c: float
    final_window_temperature_range_c: float
    invalid_vio_samples: int
    invalid_command_samples: int
    thermal_throttle_samples: int
    power_fault_samples: int
    provenance_valid: bool
    failures: tuple[str, ...]
    passed: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def assess_pi_compute_gate(
    run: PiBenchmarkRun, limits: ComputeGateLimits | None = None
) -> ComputeGateAssessment:
    configured = limits or ComputeGateLimits()
    _validate_run(run)

    valid_vio = tuple(sample for sample in run.vio_samples if sample.valid)
    valid_commands = tuple(sample for sample in run.command_samples if sample.valid)
    vio_times = tuple(sample.output_ns for sample in valid_vio)
    command_times = tuple(sample.output_ns for sample in valid_commands)
    duration_minutes = (
        _duration_s(tuple(sample.monotonic_ns for sample in run.resource_samples)) / 60.0
    )
    vio_duration_minutes = _duration_s(vio_times) / 60.0
    command_duration_minutes = _duration_s(command_times) / 60.0
    vio_hz = _rate_hz(vio_times)
    command_hz = _rate_hz(command_times)
    vio_latency_ms = tuple(
        (sample.output_ns - sample.camera_capture_ns) / 1_000_000.0 for sample in valid_vio
    )
    p95_latency = _percentile(vio_latency_ms, 0.95)
    vio_gap_ms = _maximum_gap_ms(vio_times)
    command_gap_ms = _maximum_gap_ms(command_times)
    known_gaps = [gap for gap in (vio_gap_ms, command_gap_ms) if gap is not None]
    maximum_processing_gap_ms = max(known_gaps) if known_gaps else None
    cpu_p95 = _percentile(
        tuple(sample.cpu_utilization_fraction for sample in run.resource_samples), 0.95
    )
    maximum_memory = max(sample.memory_utilization_fraction for sample in run.resource_samples)
    maximum_temperature = max(sample.temperature_c for sample in run.resource_samples)
    final_window = _final_quarter(run.resource_samples)
    final_temperature_range = max(sample.temperature_c for sample in final_window) - min(
        sample.temperature_c for sample in final_window
    )
    invalid_vio = len(run.vio_samples) - len(valid_vio)
    invalid_commands = len(run.command_samples) - len(valid_commands)
    throttle_samples = sum(sample.thermal_throttled for sample in run.resource_samples)
    power_fault_samples = sum(
        sample.undervoltage_observed or sample.frequency_capped for sample in run.resource_samples
    )
    provenance_failures = _provenance_failures(run.provenance)

    failures: list[str] = []
    if run.evidence_kind is ComputeEvidenceKind.SYNTHETIC:
        failures.append("synthetic evidence cannot pass the deployed Raspberry Pi gate")
    if not run.device_model.strip().lower().startswith("raspberry pi 4"):
        failures.append("capture is not identified as Raspberry Pi 4 hardware")
    if duration_minutes < configured.minimum_duration_minutes:
        failures.append("run duration is below the configured thermal endurance requirement")
    if vio_duration_minutes < configured.minimum_duration_minutes:
        failures.append("VIO stream does not cover the configured endurance duration")
    if command_duration_minutes < configured.minimum_duration_minutes:
        failures.append("command stream does not cover the configured endurance duration")
    resource_start = run.resource_samples[0].monotonic_ns
    resource_end = run.resource_samples[-1].monotonic_ns
    if not _stream_covers_resource_window(vio_times, resource_start, resource_end):
        failures.append("VIO stream does not cover the resource-monitoring window")
    if not _stream_covers_resource_window(command_times, resource_start, resource_end):
        failures.append("command stream does not cover the resource-monitoring window")
    if vio_hz < configured.minimum_vio_hz:
        failures.append("VIO output rate is below the configured minimum")
    if command_hz < configured.minimum_command_hz:
        failures.append("command output rate is below the configured minimum")
    if p95_latency is None:
        failures.append("VIO latency is unavailable because no valid samples were recorded")
    elif p95_latency > configured.maximum_vio_p95_latency_ms:
        failures.append("VIO p95 latency exceeds the configured maximum")
    if vio_gap_ms is None:
        failures.append("VIO gap is unavailable because fewer than two valid samples were recorded")
    elif vio_gap_ms > configured.maximum_processing_gap_ms:
        failures.append("VIO processing gap exceeds the configured maximum")
    if command_gap_ms is None:
        failures.append(
            "command gap is unavailable because fewer than two valid samples were recorded"
        )
    elif command_gap_ms > configured.maximum_processing_gap_ms:
        failures.append("command processing gap exceeds the configured maximum")
    if cpu_p95 > configured.maximum_cpu_p95_utilization_fraction:
        failures.append("CPU reserve is below the configured minimum")
    if maximum_memory > configured.maximum_memory_utilization_fraction:
        failures.append("memory reserve is below the configured minimum")
    if final_temperature_range > configured.maximum_final_window_temperature_range_c:
        failures.append("temperature did not stabilize in the final quarter of the run")
    if throttle_samples:
        failures.append("thermal throttling was observed")
    if power_fault_samples:
        failures.append("undervoltage or frequency capping was observed")
    if invalid_vio:
        failures.append("invalid VIO samples were observed")
    if invalid_commands:
        failures.append("invalid command samples were observed")
    failures.extend(provenance_failures)

    return ComputeGateAssessment(
        run_id=run.run_id,
        evidence_kind=run.evidence_kind.value,
        duration_minutes=duration_minutes,
        vio_duration_minutes=vio_duration_minutes,
        command_duration_minutes=command_duration_minutes,
        vio_hz=vio_hz,
        command_hz=command_hz,
        vio_p95_latency_ms=p95_latency,
        maximum_processing_gap_ms=maximum_processing_gap_ms,
        maximum_vio_gap_ms=vio_gap_ms,
        maximum_command_gap_ms=command_gap_ms,
        cpu_p95_utilization_fraction=cpu_p95,
        maximum_memory_utilization_fraction=maximum_memory,
        maximum_temperature_c=maximum_temperature,
        final_window_temperature_range_c=final_temperature_range,
        invalid_vio_samples=invalid_vio,
        invalid_command_samples=invalid_commands,
        thermal_throttle_samples=throttle_samples,
        power_fault_samples=power_fault_samples,
        provenance_valid=not provenance_failures,
        failures=tuple(failures),
        passed=not failures,
    )


def _validate_run(run: PiBenchmarkRun) -> None:
    if integer({"schema_version": run.schema_version}, "schema_version") != 2:
        raise ValueError("Pi benchmark capture schema_version must be 2")
    if len(run.vio_samples) < 2 or len(run.command_samples) < 2:
        raise ValueError("benchmark requires at least two VIO and command samples")
    if len(run.resource_samples) < 2:
        raise ValueError("benchmark requires at least two resource samples")
    for sample in (*run.vio_samples, *run.command_samples, *run.resource_samples):
        data = asdict(sample)
        for field in data:
            if field.endswith("_ns"):
                if integer(data, field) < 0:
                    raise ValueError(f"{field} must be non-negative")
            elif field in {
                "valid",
                "thermal_throttled",
                "undervoltage_observed",
                "frequency_capped",
            }:
                boolean(data, field)
        for field in ("cpu_utilization_fraction", "memory_utilization_fraction", "temperature_c"):
            if field in data:
                number(data, field)
    boolean(asdict(run.provenance), "clock_sync_verified")
    for sample in run.vio_samples:
        if sample.camera_capture_ns < 0 or sample.output_ns < sample.camera_capture_ns:
            raise ValueError("VIO timestamps must be monotonic and causally ordered")
    _require_strictly_increasing(tuple(sample.output_ns for sample in run.vio_samples))
    _require_strictly_increasing(tuple(sample.output_ns for sample in run.command_samples))
    _require_strictly_increasing(tuple(sample.monotonic_ns for sample in run.resource_samples))
    for sample in run.resource_samples:
        values = (
            sample.cpu_utilization_fraction,
            sample.memory_utilization_fraction,
            sample.temperature_c,
        )
        if not all(isfinite(value) for value in values):
            raise ValueError("resource values must be finite")
        if not 0.0 <= sample.cpu_utilization_fraction <= 1.0:
            raise ValueError("CPU utilization must be a fraction from zero to one")
        if not 0.0 <= sample.memory_utilization_fraction <= 1.0:
            raise ValueError("memory utilization must be a fraction from zero to one")


def _provenance_failures(provenance: CaptureProvenance) -> tuple[str, ...]:
    failures: list[str] = []
    required_text = {
        "device inventory ID": provenance.device_inventory_id,
        "pipeline manifest ID": provenance.pipeline_manifest_id,
        "camera calibration ID": provenance.camera_calibration_id,
        "camera-to-body extrinsics ID": provenance.camera_to_body_extrinsics_id,
        "timestamp domain": provenance.timestamp_domain,
        "clock synchronization method": provenance.clock_sync_method,
        "power supply ID": provenance.power_supply_id,
    }
    for label, value in required_text.items():
        normalized = value.strip().lower()
        if not normalized or normalized.startswith(("unknown", "replace", "pending")):
            failures.append(f"{label} is missing or unresolved")
    digest = provenance.source_data_sha256.strip().lower()
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        failures.append("source replay data SHA-256 is missing or malformed")
    if not provenance.clock_sync_verified:
        failures.append("camera and pipeline clock synchronization is not verified")
    return tuple(failures)


def _require_strictly_increasing(values: tuple[int, ...]) -> None:
    if any(after <= before for before, after in pairwise(values)):
        raise ValueError("sample timestamps must be strictly increasing")


def _duration_s(values: tuple[int, ...]) -> float:
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / 1_000_000_000.0


def _rate_hz(values: tuple[int, ...]) -> float:
    if len(values) < 2:
        return 0.0
    duration = _duration_s(values)
    return (len(values) - 1) / duration if duration > 0.0 else 0.0


def _maximum_gap_ms(values: tuple[int, ...]) -> float | None:
    if len(values) < 2:
        return None
    return max(after - before for before, after in pairwise(values)) / 1_000_000.0


def _percentile(values: tuple[float, ...], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, ceil(len(ordered) * fraction) - 1)]


def _final_quarter(samples: tuple[ResourceSample, ...]) -> tuple[ResourceSample, ...]:
    threshold = samples[0].monotonic_ns + int(
        (samples[-1].monotonic_ns - samples[0].monotonic_ns) * 0.75
    )
    return tuple(sample for sample in samples if sample.monotonic_ns >= threshold)


def _stream_covers_resource_window(
    stream_times: tuple[int, ...], resource_start_ns: int, resource_end_ns: int
) -> bool:
    if len(stream_times) < 2:
        return False
    tolerance_ns = 1_000_000_000
    return (
        stream_times[0] <= resource_start_ns + tolerance_ns
        and stream_times[-1] >= resource_end_ns - tolerance_ns
    )
