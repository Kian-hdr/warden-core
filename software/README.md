# Warden observability

A small Python toolkit for recording pipeline timings, collecting Raspberry Pi resource measurements, and assessing local evidence files. It reports throughput, latency, processing gaps, CPU and memory use, temperature, and missing provenance.

The package contains no vehicle transport or actuation code. A `command` event records an output timestamp and validity flag only. Assessment results describe the supplied measurements; they do not establish VIO accuracy, vehicle integration, or flight readiness.

## Install

Python 3.11 or newer is required. The package has no external runtime dependencies.

From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Try the synthetic example

```sh
warden-record-events --output outputs/events.jsonl < examples/events.jsonl
warden-assemble examples/metadata.json outputs/events.jsonl examples/resources.jsonl \
  --capture-output outputs/capture.json \
  --assessment-output outputs/assessment.json
warden-assess outputs/capture.json
```

The example contains generated timestamps and resource values. Assembly and assessment return exit code **2** and a JSON report with `passed: false`: synthetic evidence cannot pass the measurement check. No hardware is needed for this example.

Every output path must be new. Existing files are preserved. A malformed input exits with an error on stderr; a valid non-passing assessment produces its JSON report on stdout. If event input fails partway through, the output file retains its valid prefix for inspection.

## Formats

| File | Contents |
|---|---|
| `examples/events.jsonl` | `vio` events contain `camera_capture_ns`, `output_ns`, and boolean `valid`; `command` events contain `output_ns` and boolean `valid`. |
| `examples/resources.jsonl` | Timestamped CPU/memory fractions, temperature in Celsius, and boolean throttle/power flags. |
| `examples/metadata.json` | Format version, evidence kind, device/software identifiers, and clock/calibration provenance. |

Timestamps are nonnegative integer nanoseconds in a shared monotonic domain. Each event stream must increase strictly, and VIO output must follow its capture. Booleans must be JSON booleans, not strings or numbers. Non-finite numeric values are rejected. Unavailable assessment metrics are represented by JSON `null` with explanatory failure reasons.

Assembly records a SHA-256 digest of the event bytes, a zero-byte separator, and the resource bytes. That digest identifies the input logs; it does not authenticate their origin. Device identity and clock synchronization remain supplied provenance.

## Assessment defaults

The default measurement profile is scoped to Raspberry Pi 4 captures: at least 20 minutes, VIO at 30 Hz, output timing at 50 Hz, VIO p95 latency at most 50 ms, processing gaps at most 100 ms, CPU and memory use at most 85%, and a final-quarter temperature range at most 5°C. Invalid samples, power faults, thermal throttling, or unresolved provenance produce a non-passing result.

`warden-assemble` and `warden-assess` accept `--limits limits.json` for explicit numeric overrides. Keys are the fields of `ComputeGateLimits`; omitted keys retain their defaults. For example:

```json
{"maximum_vio_p95_latency_ms": 40.0}
```

Overrides do not remove the Raspberry Pi 4 identity check or permit synthetic evidence to pass. Keep the limits file with the report when using a different measurement profile.

## Collect resource measurements

On Raspberry Pi Linux with `vcgencmd` available:

```sh
warden-record-resources --duration-seconds 1200 --interval-seconds 1 \
  --output outputs/resources.jsonl
```

The collector reads `/proc/stat`, `/proc/meminfo`, the thermal-zone file, and `vcgencmd get_throttled`. It includes current and historical power/throttle flags. It writes only the requested log. Missing platform inputs or counter discontinuities stop capture; a partially written log remains available. The offline tools and tests do not require Linux or Raspberry Pi hardware.

## Development

```sh
python -m pip install -e '.[dev]'
python -m pytest
ruff check .
```

Tests use synthetic data and cover parsing, timing validation, evidence assembly, assessment failures, strict JSON reports, and CLI output preservation. The Linux collector requires separate platform verification before making hardware measurement claims.
