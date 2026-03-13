from __future__ import annotations

import logging

from hwtest.hardware import SignalModule
from hwtest.models import Limit, Measurement
from hwtest.tests.base import HardwareTest

logger = logging.getLogger(__name__)


class SignalIntegrityTest(HardwareTest):
    name = "Signal Integrity"

    def __init__(self, module: SignalModule, freq_tolerance_hz: float = 5.0, max_thd_percent: float = 1.0):
        self.module = module
        self.freq_tolerance_hz = freq_tolerance_hz
        self.max_thd_percent = max_thd_percent

    def run(self):
        freq = self.module.measure_frequency()
        thd = self.module.measure_thd()

        freq_limit = Limit(
            low=self.module.target_frequency_hz - self.freq_tolerance_hz,
            high=self.module.target_frequency_hz + self.freq_tolerance_hz,
        )
        thd_limit = Limit(low=0, high=self.max_thd_percent)

        measurements = [
            Measurement(name="Frequency", value=freq, unit="Hz", limit=freq_limit),
            Measurement(name="THD", value=thd, unit="%", limit=thd_limit),
        ]
        result = self._status(measurements, details="Frequency and distortion check")
        result.name = self.name
        return self._complete(result)

