from __future__ import annotations

import logging

from hwtest.hardware import VoltageRegulator, simulate_environment
from hwtest.models import Limit, Measurement
from hwtest.tests.base import HardwareTest

logger = logging.getLogger(__name__)


class VoltageRegulatorTest(HardwareTest):
    name = "Voltage Regulator Output"

    def __init__(self, regulator: VoltageRegulator, tolerance: float = 0.05):
        self.regulator = regulator
        self.tolerance = tolerance

    def run(self):
        ambient, runtime = simulate_environment()
        logger.debug("Voltage test at ambient=%.1fC runtime=%.1fh", ambient, runtime)
        reading = self.regulator.measure(hours_of_runtime=runtime)
        limit = Limit(
            low=self.regulator.nominal - self.tolerance,
            high=self.regulator.nominal + self.tolerance,
        )
        measurement = Measurement(name="Vout", value=reading, unit="V", limit=limit)
        result = self._status([measurement])
        result.name = self.name
        result.details = f"Ambient {ambient:.1f}C, runtime {runtime:.1f}h"
        return self._complete(result)

