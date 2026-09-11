from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from warden_observability.cli import record_resources

EXAMPLES = Path(__file__).parents[1] / "examples"


def run_cli(name: str, *args: object, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", f"warden_observability.cli.{name}", *map(str, args)],
        check=False,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_synthetic_pipeline_and_no_clobber(tmp_path: Path) -> None:
    events = tmp_path / "events.jsonl"
    result = run_cli(
        "record_events", "--output", events, stdin=(EXAMPLES / "events.jsonl").read_text()
    )
    assert result.returncode == 0, result.stderr
    original = events.read_bytes()
    assert run_cli("record_events", "--output", events, stdin="").returncode != 0
    assert events.read_bytes() == original
    capture = tmp_path / "capture.json"
    assessment = tmp_path / "assessment.json"
    result = run_cli(
        "assemble",
        EXAMPLES / "metadata.json",
        events,
        EXAMPLES / "resources.jsonl",
        "--capture-output",
        capture,
        "--assessment-output",
        assessment,
    )
    assert result.returncode == 2, result.stderr
    report = json.loads(result.stdout)
    assert not report["passed"]
    assert report["evidence_kind"] == "synthetic"
    assert json.loads(assessment.read_text()) == report
    result = run_cli("assess", capture)
    assert result.returncode == 2
    assert json.loads(result.stdout) == report
    original_capture = capture.read_bytes()
    result = run_cli(
        "assemble",
        EXAMPLES / "metadata.json",
        events,
        EXAMPLES / "resources.jsonl",
        "--capture-output",
        capture,
    )
    assert result.returncode != 0
    assert not result.stdout
    assert capture.read_bytes() == original_capture
    original_assessment = assessment.read_bytes()
    assert run_cli("assess", capture, "--output", assessment).returncode != 0
    assert assessment.read_bytes() == original_assessment


def test_duplicate_outputs_fail_before_creation(tmp_path: Path) -> None:
    output = tmp_path / "same.json"
    result = run_cli(
        "assemble",
        EXAMPLES / "metadata.json",
        EXAMPLES / "events.jsonl",
        EXAMPLES / "resources.jsonl",
        "--capture-output",
        output,
        "--assessment-output",
        output,
    )
    assert result.returncode != 0
    assert not output.exists()


def test_all_cli_help_commands_are_available() -> None:
    for name in ("record_events", "record_resources", "assemble", "assess"):
        assert run_cli(name, "--help").returncode == 0


def test_resource_collector_rejects_nonfinite_duration(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "record-resources",
            "--duration-seconds",
            "nan",
            "--output",
            str(tmp_path / "resource.jsonl"),
        ],
    )
    with pytest.raises(SystemExit) as error:
        record_resources.main()
    assert error.value.code == 2
    assert not (tmp_path / "resource.jsonl").exists()


def test_package_import_does_not_load_control_or_transport() -> None:
    for name in ("compute_gate", "pi_capture", "pi_events", "pi_resources"):
        importlib.import_module(f"warden_observability.{name}")
    assert "warden_core" not in sys.modules
    assert "pymavlink" not in sys.modules
    assert "serial" not in sys.modules
    assert not any(name.startswith("warden_observability.controllers") for name in sys.modules)


def test_resource_collector_with_mock_linux_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from types import SimpleNamespace

    from warden_observability.pi_resources import CpuCounters

    sources = {}
    for name, contents in {
        "/proc/stat": "cpu counters supplied by test",
        "/proc/meminfo": "MemTotal: 1000 kB\nMemAvailable: 600 kB\n",
        "/sys/class/thermal/thermal_zone0/temp": "55000\n",
    }.items():
        path = tmp_path / name.replace("/", "_")
        path.write_text(contents)
        sources[name] = path
    real_path = Path
    monkeypatch.setattr(
        record_resources, "Path", lambda value: sources.get(str(value), real_path(value))
    )
    monkeypatch.setattr(record_resources.sys, "platform", "linux")
    monkeypatch.setattr(record_resources.shutil, "which", lambda _: "/example/vcgencmd")
    invocations = []

    def command(args: list[str], **kwargs: object) -> SimpleNamespace:
        invocations.append((args, kwargs))
        return SimpleNamespace(stdout="throttled=0x0\n")

    monkeypatch.setattr(record_resources.subprocess, "run", command)
    counters = iter([CpuCounters(800, 1000), CpuCounters(880, 1100), CpuCounters(960, 1200)])
    monkeypatch.setattr(record_resources, "parse_proc_stat", lambda _: next(counters))
    seconds = iter([0.0, 1.0, 2.0])
    timestamps = iter([1_000_000_000, 2_000_000_000])
    monkeypatch.setattr(record_resources.time, "monotonic", lambda: next(seconds))
    monkeypatch.setattr(record_resources.time, "monotonic_ns", lambda: next(timestamps))
    output = tmp_path / "measured.jsonl"
    monkeypatch.setattr(
        sys, "argv", ["record-resources", "--duration-seconds", "1", "--output", str(output)]
    )
    assert record_resources.main() == 0
    records = [json.loads(line) for line in output.read_text().splitlines()]
    assert len(records) == 2
    assert records[0]["cpu_utilization_fraction"] == 0.2
    assert records[1]["temperature_c"] == 55.0
    assert all(args == ["/example/vcgencmd", "get_throttled"] for args, _ in invocations)
    assert all(kwargs["timeout"] == 2.0 and "shell" not in kwargs for _, kwargs in invocations)
