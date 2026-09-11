from warden_observability.compute_gate import (
    CaptureProvenance,
    CommandSample,
    ComputeEvidenceKind,
    PiBenchmarkRun,
    ResourceSample,
    VioSample,
    assess_pi_compute_gate,
)

SECOND = 1_000_000_000


def passing_run(*, evidence_kind: ComputeEvidenceKind) -> PiBenchmarkRun:
    duration_s = 20 * 60
    vio = tuple(
        VioSample(
            camera_capture_ns=index * SECOND // 30,
            output_ns=index * SECOND // 30 + 20_000_000,
            valid=True,
        )
        for index in range(duration_s * 30 + 1)
    )
    commands = tuple(
        CommandSample(output_ns=index * SECOND // 50 + 20_000_000, valid=True)
        for index in range(duration_s * 50 + 1)
    )
    resources = tuple(
        ResourceSample(
            monotonic_ns=index * SECOND,
            cpu_utilization_fraction=0.60,
            memory_utilization_fraction=0.50,
            temperature_c=60.0,
            thermal_throttled=False,
        )
        for index in range(duration_s + 1)
    )
    return PiBenchmarkRun(
        schema_version=2,
        run_id="pi-gate-test",
        evidence_kind=evidence_kind,
        device_model="Raspberry Pi 4B",
        os_version="test",
        vio_implementation="test",
        policy_id="test",
        provenance=CaptureProvenance(
            device_inventory_id="pi4b-test",
            source_data_sha256="a" * 64,
            pipeline_manifest_id="pipeline-test",
            camera_calibration_id="camera-test",
            camera_to_body_extrinsics_id="extrinsics-test",
            timestamp_domain="monotonic_raw",
            clock_sync_method="hardware timestamp correlation",
            clock_sync_verified=True,
            power_supply_id="supply-test",
        ),
        vio_samples=vio,
        command_samples=commands,
        resource_samples=resources,
    )


def test_real_pi_capture_passes_when_every_threshold_is_met() -> None:
    result = assess_pi_compute_gate(
        passing_run(evidence_kind=ComputeEvidenceKind.REAL_PI_RECORDED_REPLAY)
    )
    assert result.passed
    assert result.vio_hz >= 30.0
    assert result.command_hz >= 50.0


def test_synthetic_capture_can_never_pass() -> None:
    result = assess_pi_compute_gate(passing_run(evidence_kind=ComputeEvidenceKind.SYNTHETIC))
    assert not result.passed
    assert any("synthetic evidence" in failure for failure in result.failures)


def test_invalid_samples_and_throttling_fail() -> None:
    run = passing_run(evidence_kind=ComputeEvidenceKind.REAL_PI_PROPS_OFF_MOTION)
    vio = run.vio_samples[:-1] + (
        VioSample(
            camera_capture_ns=run.vio_samples[-1].camera_capture_ns,
            output_ns=run.vio_samples[-1].output_ns,
            valid=False,
        ),
    )
    resources = run.resource_samples[:-1] + (
        ResourceSample(
            monotonic_ns=run.resource_samples[-1].monotonic_ns,
            cpu_utilization_fraction=0.60,
            memory_utilization_fraction=0.50,
            temperature_c=60.0,
            thermal_throttled=True,
        ),
    )
    result = assess_pi_compute_gate(
        PiBenchmarkRun(
            schema_version=run.schema_version,
            run_id=run.run_id,
            evidence_kind=run.evidence_kind,
            device_model=run.device_model,
            os_version=run.os_version,
            vio_implementation=run.vio_implementation,
            policy_id=run.policy_id,
            provenance=run.provenance,
            vio_samples=vio,
            command_samples=run.command_samples,
            resource_samples=resources,
        )
    )
    assert not result.passed
    assert result.invalid_vio_samples == 1
    assert result.thermal_throttle_samples == 1


def test_short_vio_and_command_streams_cannot_borrow_resource_duration() -> None:
    run = passing_run(evidence_kind=ComputeEvidenceKind.REAL_PI_RECORDED_REPLAY)
    result = assess_pi_compute_gate(
        PiBenchmarkRun(
            schema_version=run.schema_version,
            run_id=run.run_id,
            evidence_kind=run.evidence_kind,
            device_model=run.device_model,
            os_version=run.os_version,
            vio_implementation=run.vio_implementation,
            policy_id=run.policy_id,
            provenance=run.provenance,
            vio_samples=run.vio_samples[:31],
            command_samples=run.command_samples[:51],
            resource_samples=run.resource_samples,
        )
    )
    assert not result.passed
    assert any("VIO stream does not cover" in failure for failure in result.failures)
    assert any("command stream does not cover" in failure for failure in result.failures)


def test_vio_gap_power_fault_and_unverified_clock_each_fail() -> None:
    run = passing_run(evidence_kind=ComputeEvidenceKind.REAL_PI_PROPS_OFF_MOTION)
    vio = list(run.vio_samples)
    midpoint = len(vio) // 2
    for index in range(midpoint, len(vio)):
        sample = vio[index]
        vio[index] = VioSample(
            camera_capture_ns=sample.camera_capture_ns + 150_000_000,
            output_ns=sample.output_ns + 150_000_000,
            valid=sample.valid,
        )
    resources = run.resource_samples[:-1] + (
        ResourceSample(
            monotonic_ns=run.resource_samples[-1].monotonic_ns,
            cpu_utilization_fraction=0.6,
            memory_utilization_fraction=0.5,
            temperature_c=60.0,
            thermal_throttled=False,
            undervoltage_observed=True,
        ),
    )
    provenance = CaptureProvenance(
        device_inventory_id=run.provenance.device_inventory_id,
        source_data_sha256=run.provenance.source_data_sha256,
        pipeline_manifest_id=run.provenance.pipeline_manifest_id,
        camera_calibration_id=run.provenance.camera_calibration_id,
        camera_to_body_extrinsics_id=run.provenance.camera_to_body_extrinsics_id,
        timestamp_domain=run.provenance.timestamp_domain,
        clock_sync_method=run.provenance.clock_sync_method,
        clock_sync_verified=False,
        power_supply_id=run.provenance.power_supply_id,
    )
    result = assess_pi_compute_gate(
        PiBenchmarkRun(
            schema_version=run.schema_version,
            run_id=run.run_id,
            evidence_kind=run.evidence_kind,
            device_model=run.device_model,
            os_version=run.os_version,
            vio_implementation=run.vio_implementation,
            policy_id=run.policy_id,
            provenance=provenance,
            vio_samples=tuple(vio),
            command_samples=run.command_samples,
            resource_samples=resources,
        )
    )
    assert not result.passed
    assert result.maximum_vio_gap_ms > 100.0
    assert result.power_fault_samples == 1
    assert not result.provenance_valid


def test_all_invalid_vio_samples_fail_without_crashing() -> None:
    run = passing_run(evidence_kind=ComputeEvidenceKind.REAL_PI_RECORDED_REPLAY)
    invalid = tuple(
        VioSample(
            camera_capture_ns=sample.camera_capture_ns,
            output_ns=sample.output_ns,
            valid=False,
        )
        for sample in run.vio_samples
    )
    result = assess_pi_compute_gate(
        PiBenchmarkRun(
            schema_version=run.schema_version,
            run_id=run.run_id,
            evidence_kind=run.evidence_kind,
            device_model=run.device_model,
            os_version=run.os_version,
            vio_implementation=run.vio_implementation,
            policy_id=run.policy_id,
            provenance=run.provenance,
            vio_samples=invalid,
            command_samples=run.command_samples,
            resource_samples=run.resource_samples,
        )
    )
    assert not result.passed
    assert result.vio_hz == 0.0
    assert result.vio_duration_minutes == 0.0
    assert result.invalid_vio_samples == len(invalid)
