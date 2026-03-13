from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from hwtest.models import Measurement, TestResult

logger = logging.getLogger(__name__)


class HardwareTest(ABC):
    """Abstract base for any hardware validation test."""

    name: str

    @abstractmethod
    def run(self) -> TestResult:
        raise NotImplementedError

    def _complete(self, result: TestResult) -> TestResult:
        result.ended_at = datetime.utcnow()
        logger.debug("Completed %s with status %s", result.name, result.status)
        return result

    @staticmethod
    def _status(measurements: List[Measurement], details: str | None = None) -> TestResult:
        status = "PASS" if all(m.passed for m in measurements) else "FAIL"
        return TestResult(
            name="",
            status=status,
            measurements=measurements,
            details=details,
        )

