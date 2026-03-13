from __future__ import annotations

import logging

from hwtest.hardware import TemperatureSensor, simulate_environment
from hwtest.models import Limit, Measurement
from hwtest.tests.base import HardwareTest

logger = logging.getLogger(__name__)


class TemperatureSensorDriftTest(HardwareTest):
    name = "Temperature Sensor Drift"

    def __init__(self, sensor: TemperatureSensor, tolerance_c: float = 1.5):
        self.sensor = sensor
        self.tolerance_c = tolerance_c

    def run(self):
        ambient, _ = simulate_environment()
        reading = self.sensor.read(ambient_c=ambient)
        limit = Limit(low=ambient - self.tolerance_c, high=ambient + self.tolerance_c)
        measurement = Measurement(name="Reported Temp", value=reading, unit="C", limit=limit)
        result = self._status([measurement])
        result.name = self.name
        result.details = f"Ambient {ambient:.1f}C"
        return self._complete(result)

