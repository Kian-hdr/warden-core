from __future__ import annotations

from pathlib import Path

import pytest

from warden_observability.pi_capture import assemble_pi_benchmark_capture
from warden_observability.pi_events import (
    CommandPipelineEvent,
    PipelineEventWriter,
    VioPipelineEvent,
    parse_pipeline_event_json,
)


def test_event_parser_requires_causal_strict_types() -> None:
    event = parse_pipeline_event_json(
        '{"kind":"vio","camera_capture_ns":100,"output_ns":120,"valid":true}'
    )
    assert event == VioPipelineEvent(camera_capture_ns=100, output_ns=120, valid=True)
    with pytest.raises(ValueError, match="precedes"):
        parse_pipeline_event_json(
            '{"kind":"vio","camera_capture_ns":120,"output_ns":100,"valid":true}'
        )
    with pytest.raises(TypeError, match="boolean"):
        parse_pipeline_event_json('{"kind":"command","output_ns":100,"valid":1}')


def test_writer_is_exclusive_and_enforces_each_stream_order(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    with PipelineEventWriter(path) as writer:
        writer.write(VioPipelineEvent(100, 120, True))
        writer.write(CommandPipelineEvent(121, True))
        writer.write(VioPipelineEvent(200, 220, True))
        with pytest.raises(ValueError, match="strictly increasing"):
            writer.write(CommandPipelineEvent(121, True))
    with pytest.raises(FileExistsError):
        PipelineEventWriter(path)
    assert len(path.read_text(encoding="utf-8").splitlines()) == 3


def test_canonical_event_log_is_consumed_by_benchmark_assembler(tmp_path: Path) -> None:
    events_path = tmp_path / "events.jsonl"
    with PipelineEventWriter(events_path) as writer:
        writer.write(VioPipelineEvent(100, 120, True))
        writer.write(CommandPipelineEvent(125, True))
        writer.write(VioPipelineEvent(200, 220, True))
        writer.write(CommandPipelineEvent(225, True))
    resources = b"""{"monotonic_ns":100,"cpu_utilization_fraction":0.5,"memory_utilization_fraction":0.4,"temperature_c":50.0,"thermal_throttled":false,"undervoltage_observed":false,"frequency_capped":false}
{"monotonic_ns":1000000100,"cpu_utilization_fraction":0.5,"memory_utilization_fraction":0.4,"temperature_c":50.0,"thermal_throttled":false,"undervoltage_observed":false,"frequency_capped":false}
"""
    metadata = {
        "schema_version": 1,
        "run_id": "event-integration",
        "evidence_kind": "real_pi_recorded_replay",
        "device_model": "Raspberry Pi 4B",
        "os_version": "test",
        "vio_implementation": "test",
        "policy_id": "test",
        "provenance": {
            "device_inventory_id": "pi-test",
            "pipeline_manifest_id": "pipeline-test",
            "camera_calibration_id": "camera-test",
            "camera_to_body_extrinsics_id": "extrinsics-test",
            "timestamp_domain": "monotonic_raw",
            "clock_sync_method": "hardware correlation",
            "clock_sync_verified": True,
            "power_supply_id": "supply-test",
        },
    }
    run = assemble_pi_benchmark_capture(metadata, events_path.read_bytes(), resources)
    assert len(run.vio_samples) == 2
    assert len(run.command_samples) == 2
