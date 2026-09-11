from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from warden_observability.compute_gate import (
    CaptureProvenance,
    CommandSample,
    ComputeEvidenceKind,
    PiBenchmarkRun,
    ResourceSample,
    VioSample,
    _validate_run,
)

from .validation import (
    boolean as _boolean,
)
from .validation import (
    integer as _integer,
)
from .validation import (
    number as _number,
)
from .validation import (
    object_value,
)
from .validation import (
    text as _text,
)


def assemble_pi_benchmark_capture(
    metadata: dict[str, Any], event_log: bytes, resource_log: bytes
) -> PiBenchmarkRun:
    metadata = object_value(metadata, "metadata")
    if _integer(metadata, "schema_version") != 1:
        raise ValueError("Pi capture metadata schema_version must be 1")
    source_digest = hashlib.sha256(event_log + b"\0" + resource_log).hexdigest()
    provenance = metadata.get("provenance")
    if not isinstance(provenance, dict):
        raise TypeError("Pi capture provenance must be an object")

    vio: list[VioSample] = []
    commands: list[CommandSample] = []
    for line_number, event in _jsonl_records(event_log, "pipeline event"):
        kind = event.get("kind")
        try:
            if kind == "vio":
                vio.append(
                    VioSample(
                        camera_capture_ns=_integer(event, "camera_capture_ns"),
                        output_ns=_integer(event, "output_ns"),
                        valid=_boolean(event, "valid"),
                    )
                )
            elif kind == "command":
                commands.append(
                    CommandSample(
                        output_ns=_integer(event, "output_ns"),
                        valid=_boolean(event, "valid"),
                    )
                )
            else:
                raise ValueError(f"unknown pipeline event kind {kind!r}")
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"pipeline event line {line_number}: {exc}") from exc

    resources: list[ResourceSample] = []
    for line_number, sample in _jsonl_records(resource_log, "resource sample"):
        try:
            resources.append(
                ResourceSample(
                    monotonic_ns=_integer(sample, "monotonic_ns"),
                    cpu_utilization_fraction=_number(sample, "cpu_utilization_fraction"),
                    memory_utilization_fraction=_number(sample, "memory_utilization_fraction"),
                    temperature_c=_number(sample, "temperature_c"),
                    thermal_throttled=_boolean(sample, "thermal_throttled"),
                    undervoltage_observed=_boolean(sample, "undervoltage_observed"),
                    frequency_capped=_boolean(sample, "frequency_capped"),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"resource sample line {line_number}: {exc}") from exc

    run = PiBenchmarkRun(
        schema_version=2,
        run_id=_text(metadata, "run_id"),
        evidence_kind=ComputeEvidenceKind(metadata["evidence_kind"]),
        device_model=_text(metadata, "device_model"),
        os_version=_text(metadata, "os_version"),
        vio_implementation=_text(metadata, "vio_implementation"),
        policy_id=_text(metadata, "policy_id"),
        provenance=CaptureProvenance(
            device_inventory_id=_text(provenance, "device_inventory_id"),
            source_data_sha256=source_digest,
            pipeline_manifest_id=_text(provenance, "pipeline_manifest_id"),
            camera_calibration_id=_text(provenance, "camera_calibration_id"),
            camera_to_body_extrinsics_id=_text(provenance, "camera_to_body_extrinsics_id"),
            timestamp_domain=_text(provenance, "timestamp_domain"),
            clock_sync_method=_text(provenance, "clock_sync_method"),
            clock_sync_verified=_boolean(provenance, "clock_sync_verified"),
            power_supply_id=_text(provenance, "power_supply_id"),
        ),
        vio_samples=tuple(vio),
        command_samples=tuple(commands),
        resource_samples=tuple(resources),
    )

    _validate_run(run)
    return run


def assemble_pi_benchmark_capture_from_files(
    metadata_path: Path, event_log_path: Path, resource_log_path: Path
) -> PiBenchmarkRun:
    metadata: dict[str, Any] = json.loads(metadata_path.read_text(encoding="utf-8"))
    return assemble_pi_benchmark_capture(
        metadata,
        event_log_path.read_bytes(),
        resource_log_path.read_bytes(),
    )


def _jsonl_records(source: bytes, label: str) -> tuple[tuple[int, dict[str, Any]], ...]:
    records: list[tuple[int, dict[str, Any]]] = []
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} log is not UTF-8") from exc
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{label} line {line_number} is not valid JSON") from exc
        if not isinstance(value, dict):
            raise TypeError(f"{label} line {line_number} must be an object")
        records.append((line_number, value))
    return tuple(records)
