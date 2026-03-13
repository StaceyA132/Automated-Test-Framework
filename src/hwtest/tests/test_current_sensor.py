from __future__ import annotations

from hwtest.hardware import CurrentSensor
from hwtest.models import Limit, Measurement
from hwtest.tests.base import HardwareTest


class CurrentSensorTest(HardwareTest):
    name = "Current Sensor Accuracy"

    def __init__(self, sensor: CurrentSensor, tolerance_ma: float = 20.0):
        self.sensor = sensor
        self.tolerance_ma = tolerance_ma

    def run(self):
        reading = self.sensor.read()
        limit = Limit(
            low=self.sensor.nominal_ma - self.tolerance_ma,
            high=self.sensor.nominal_ma + self.tolerance_ma,
        )
        measurement = Measurement(name="Current", value=reading, unit="mA", limit=limit)
        result = self._status([measurement], details="Check sensor output vs nominal")
        result.name = self.name
        return self._complete(result)
