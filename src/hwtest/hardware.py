from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Tuple 


@dataclass
class VoltageRegulator:
    nominal: float = 5.0
    noise: float = 0.03
    drift_per_hour: float = 0.01

    def measure(self, hours_of_runtime: float = 0.0) -> float:
        """Simulate output voltage with drift and gaussian noise."""
        drift = self.drift_per_hour * hours_of_runtime
        noise = random.gauss(0, self.noise)
        return self.nominal + drift + noise


@dataclass
class TemperatureSensor:
    bias_c: float = 0.2
    noise_c: float = 0.5

    def read(self, ambient_c: float) -> float:
        return ambient_c + self.bias_c + random.gauss(0, self.noise_c)


@dataclass
class SignalModule:
    target_frequency_hz: float = 1_000.0
    jitter: float = 2.5  # Hz
    distortion_percent: float = 0.3

    def measure_frequency(self) -> float:
        return self.target_frequency_hz + random.gauss(0, self.jitter)

    def measure_thd(self) -> float:
        """Total harmonic distortion as a percent."""
        base = self.distortion_percent
        # Slightly correlated with jitter to keep results interesting
        perturb = abs(random.gauss(0, 0.05))
        return base + perturb


def simulate_environment() -> Tuple[float, float]:
    """Return ambient temperature (C) and hours of runtime."""
    ambient = random.uniform(20.0, 35.0)
    runtime = random.uniform(0, 8)
    return ambient, runtime

