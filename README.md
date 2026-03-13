# Python Hardware Test Automation Framework

Simulated hardware validation stack that runs automated checks against virtual components (voltage regulator, temperature sensor, and signal module), validates measurements against operational limits, and logs timestamped results.

## Quick start

```bash
PYTHONPATH=src python -m hwtest.runner
```

You should see each test stream to stdout and a log file created under `logs/`. Alternatively, install in editable mode with `pip install -e .` and then run `python -m hwtest.runner`.

## Project layout

- `src/hwtest/hardware.py` – simple component simulators (regulator, sensor, signal module, current sensor).
- `src/hwtest/models.py` – data classes for limits, measurements, and test results.
- `src/hwtest/tests/` – modular test cases (voltage output, sensor drift, signal integrity).
- `src/hwtest/runner.py` – orchestrates test sequences, logging, and summary.
- `logs/` – run artifacts with timestamped filenames (created on first run).

## How it works

1. Each test subclasses `HardwareTest` and returns a `TestResult` populated with measurements.
2. Measurements carry inclusive limits; pass/fail is derived automatically.
3. `runner.py` builds a default suite, executes in sequence, and prints a concise summary.
4. Logging writes both to console and a timestamped file for later analysis.

## Extending

- Add new simulated hardware in `hardware.py`.
- Create a new test module in `src/hwtest/tests/` and subclass `HardwareTest`.
- Register your test in `default_suite()` inside `runner.py`.

### Sample Test Run

```text
2026-03-12 21:17:06 [INFO] Running Voltage Regulator Output -> FAIL
2026-03-12 21:17:06 [INFO] Running Temperature Sensor Drift -> PASS
2026-03-12 21:17:06 [INFO] Running Signal Integrity -> PASS
2026-03-12 21:17:06 [INFO] Running Current Sensor Accuracy -> PASS
Summary: 4 total, 3 passed, 1 failed
```

### Sample Log Artifact

- See `examples/sample_run.txt` for a captured log from a seeded run.
