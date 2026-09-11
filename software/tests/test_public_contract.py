from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from warden_observability.compute_gate import (
    ComputeGateLimits,
    PiBenchmarkRun,
    assess_pi_compute_gate,
)
from warden_observability.pi_capture import assemble_pi_benchmark_capture_from_files
from warden_observability.pi_events import parse_pipeline_event_json
from warden_observability.pi_resources import parse_proc_stat

EXAMPLES = Path(__file__).parents[1] / "examples"


def capture() -> dict:
    return assemble_pi_benchmark_capture_from_files(
        EXAMPLES / "metadata.json", EXAMPLES / "events.jsonl", EXAMPLES / "resources.jsonl"
    ).to_dict()


@pytest.mark.parametrize("value", ["false", 0, 1, None])
def test_loaded_capture_rejects_coerced_booleans(value: object) -> None:
    data = capture()
    data["provenance"]["clock_sync_verified"] = value
    with pytest.raises(TypeError, match="boolean"):
        PiBenchmarkRun.from_dict(data)
    data = capture()
    data["command_samples"][0]["valid"] = value
    with pytest.raises(TypeError, match="boolean"):
        PiBenchmarkRun.from_dict(data)


@pytest.mark.parametrize("value", [True, "2", 2.0])
def test_schema_version_requires_integer(value: object) -> None:
    data = capture()
    data["schema_version"] = value
    with pytest.raises(TypeError, match="integer"):
        PiBenchmarkRun.from_dict(data)


@pytest.mark.parametrize("value", [True, -1, "100"])
def test_timestamps_require_nonnegative_integers(value: object) -> None:
    data = capture()
    data["command_samples"][0]["output_ns"] = value
    with pytest.raises((ValueError, TypeError)):
        PiBenchmarkRun.from_dict(data)


def test_event_rejects_negative_camera_capture() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        parse_pipeline_event_json(
            '{"kind":"vio","camera_capture_ns":-1,"output_ns":10,"valid":true}'
        )


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True])
def test_resource_values_reject_nonfinite_and_boolean(value: object) -> None:
    data = capture()
    data["resource_samples"][0]["temperature_c"] = value
    with pytest.raises((TypeError, ValueError)):
        PiBenchmarkRun.from_dict(data)


def test_failed_assessment_is_strict_json_with_unavailable_metrics() -> None:
    data = copy.deepcopy(capture())
    for sample in data["vio_samples"] + data["command_samples"]:
        sample["valid"] = False
    assessment = assess_pi_compute_gate(PiBenchmarkRun.from_dict(data))
    payload = json.dumps(assessment.to_dict(), allow_nan=False)
    parsed = json.loads(payload)
    assert not parsed["passed"]
    assert parsed["vio_p95_latency_ms"] is None
    assert parsed["maximum_vio_gap_ms"] is None
    assert parsed["maximum_command_gap_ms"] is None
    assert parsed["maximum_processing_gap_ms"] is None
    assert parsed["failures"]


def test_cpu_guest_columns_do_not_double_count_user_time() -> None:
    counters = parse_proc_stat("cpu 100 20 30 400 5 6 7 8 10 2\n")
    assert counters.total == 576
    assert counters.idle == 405


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf"), True])
def test_limits_are_positive_finite_numbers(value: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        ComputeGateLimits(minimum_vio_hz=value)
