from __future__ import annotations

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from hwtest.hardware import CurrentSensor, SignalModule, TemperatureSensor, VoltageRegulator
from hwtest.models import TestResult
from hwtest.tests.test_current_sensor import CurrentSensorTest
from hwtest.tests.test_signal_module import SignalIntegrityTest
from hwtest.tests.test_temperature_sensor import TemperatureSensorDriftTest
from hwtest.tests.test_voltage_regulator import VoltageRegulatorTest

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def configure_logging() -> None:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    logfile = LOG_DIR / f"test_run_{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(logfile), logging.StreamHandler()],
    )
    logging.getLogger("hwtest").setLevel(logging.DEBUG)
    logging.info("Logging initialized at %s", logfile)


def default_suite() -> List:
    regulator = VoltageRegulator()
    sensor = TemperatureSensor()
    signal = SignalModule()
    current = CurrentSensor()

    return [
        VoltageRegulatorTest(regulator),
        TemperatureSensorDriftTest(sensor),
        SignalIntegrityTest(signal),
        CurrentSensorTest(current),
    ]


def run_suite(tests: Iterable) -> List[TestResult]:
    results: List[TestResult] = []
    for test in tests:
        logging.info("Running %s", test.name)
        result = test.run()
        results.append(result)
        status = "PASS" if result.status == "PASS" else "FAIL"
        logging.info("%s -> %s", test.name, status)
        for m in result.measurements:
            logging.debug(
                "  %s: %.3f%s (limits %.3f..%.3f) => %s",
                m.name,
                m.value,
                m.unit,
                m.limit.low,
                m.limit.high,
                "PASS" if m.passed else "FAIL",
            )
    return results


def summarize(results: List[TestResult]) -> None:
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = total - passed
    logging.info("Summary: %d total, %d passed, %d failed", total, passed, failed)
    for res in results:
        logging.info("%s [%s]", res.name, res.status)


def main():
    configure_logging()
    suite = default_suite()
    results = run_suite(suite)
    summarize(results)


if __name__ == "__main__":
    main()
