# Python Hardware Test Automation Framework

Simulated hardware validation stack that runs automated checks against virtual components (voltage regulator, temperature sensor, and signal module), validates measurements against operational limits, and logs timestamped results.

## Quick start

```bash
PYTHONPATH=src python -m hwtest.runner
```

You should see each test stream to stdout and a log file created under `logs/`. Alternatively, install in editable mode with `pip install -e .` and then run `python -m hwtest.runner`.

## Project layout

- `src/hwtest/hardware.py` – simple component simulators (regulator, sensor, signal module).
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

## Requirements

Python 3.11+; uses only the standard library.
