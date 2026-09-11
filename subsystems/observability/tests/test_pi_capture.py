from __future__ import annotations

import hashlib

import pytest

from warden_observability.pi_capture import assemble_pi_benchmark_capture


def metadata() -> dict[str, object]:
    return {
        "schema_version": 1,
        "run_id": "pi-capture-test",
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


EVENTS = b"""{"kind":"vio","camera_capture_ns":100,"output_ns":120,"valid":true}
{"kind":"command","output_ns":125,"valid":true}
{"kind":"vio","camera_capture_ns":200,"output_ns":220,"valid":true}
{"kind":"command","output_ns":225,"valid":true}
"""

RESOURCES = b"""{"monotonic_ns":100,"cpu_utilization_fraction":0.5,"memory_utilization_fraction":0.4,"temperature_c":50.0,"thermal_throttled":false,"undervoltage_observed":false,"frequency_capped":false}
{"monotonic_ns":1000000100,"cpu_utilization_fraction":0.6,"memory_utilization_fraction":0.4,"temperature_c":51.0,"thermal_throttled":false,"undervoltage_observed":false,"frequency_capped":false}
"""


def test_assembler_builds_versioned_capture_and_hashes_raw_logs() -> None:
    run = assemble_pi_benchmark_capture(metadata(), EVENTS, RESOURCES)
    assert run.schema_version == 2
    assert len(run.vio_samples) == 2
    assert len(run.command_samples) == 2
    assert len(run.resource_samples) == 2
    assert (
        run.provenance.source_data_sha256 == hashlib.sha256(EVENTS + b"\0" + RESOURCES).hexdigest()
    )
    assert run.to_dict()["evidence_kind"] == "real_pi_recorded_replay"


def test_assembler_rejects_unknown_events_and_non_boolean_validity() -> None:
    unknown = b'{"kind":"motor","output_ns":1,"valid":true}\n'
    with pytest.raises(ValueError, match="unknown pipeline event"):
        assemble_pi_benchmark_capture(metadata(), unknown, RESOURCES)
    invalid = b'{"kind":"command","output_ns":1,"valid":1}\n'
    with pytest.raises(ValueError, match="valid must be boolean"):
        assemble_pi_benchmark_capture(metadata(), invalid, RESOURCES)


def test_assembler_rejects_non_json_and_missing_resource_fields() -> None:
    with pytest.raises(ValueError, match="not valid JSON"):
        assemble_pi_benchmark_capture(metadata(), b"not-json\n", RESOURCES)
    with pytest.raises(ValueError, match="cpu_utilization_fraction"):
        assemble_pi_benchmark_capture(metadata(), EVENTS, b'{"monotonic_ns":1}\n')
