from __future__ import annotations

import pytest

from warden_observability.pi_resources import (
    CpuCounters,
    build_resource_sample,
    cpu_utilization,
    parse_get_throttled,
    parse_meminfo_utilization,
    parse_proc_stat,
    parse_temperature_c,
)


def test_linux_cpu_and_memory_parsers_produce_fractions() -> None:
    previous = parse_proc_stat("cpu  100 0 50 850 0 0 0 0\n")
    current = parse_proc_stat("cpu  120 0 60 920 0 0 0 0\n")
    assert previous == CpuCounters(idle=850, total=1000)
    assert cpu_utilization(previous, current) == pytest.approx(0.3)
    assert parse_meminfo_utilization("MemTotal: 1000 kB\nMemAvailable: 400 kB\n") == pytest.approx(
        0.6
    )


def test_temperature_accepts_millicelsius_and_rejects_implausible_values() -> None:
    assert parse_temperature_c("55000\n") == 55.0
    assert parse_temperature_c("55.5\n") == 55.5
    with pytest.raises(ValueError, match="outside"):
        parse_temperature_c("200000")


def test_throttle_mask_includes_current_and_historical_fault_bits() -> None:
    assert parse_get_throttled("throttled=0x0") == (False, False, False)
    assert parse_get_throttled("throttled=0x50005") == (True, False, True)
    assert parse_get_throttled("throttled=0x20002") == (False, True, False)


def test_resource_sample_combines_all_read_only_sources() -> None:
    sample = build_resource_sample(
        previous_cpu=CpuCounters(idle=80, total=100),
        current_cpu=CpuCounters(idle=160, total=200),
        meminfo_text="MemTotal: 1000 kB\nMemAvailable: 750 kB\n",
        temperature_text="60000",
        throttled_text="throttled=0x10001",
        monotonic_ns=123,
    )
    assert sample.cpu_utilization_fraction == pytest.approx(0.2)
    assert sample.memory_utilization_fraction == pytest.approx(0.25)
    assert sample.temperature_c == 60.0
    assert sample.undervoltage_observed
    assert not sample.frequency_capped
    assert not sample.thermal_throttled


def test_nonmonotonic_cpu_counters_are_rejected() -> None:
    with pytest.raises(ValueError, match="not monotonic"):
        cpu_utilization(CpuCounters(10, 20), CpuCounters(9, 19))
