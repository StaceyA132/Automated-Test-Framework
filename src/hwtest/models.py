from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class Limit:
    """Inclusive bounds for a measurement."""

    low: float
    high: float

    def check(self, value: float) -> bool:
        return self.low <= value <= self.high


@dataclass
class Measurement:
    """Represents a captured measurement and its bounds."""

    name: str
    value: float
    limit: Limit
    unit: str = ""

    @property
    def passed(self) -> bool:
        return self.limit.check(self.value)


@dataclass
class TestResult:
    name: str
    status: str
    measurements: List[Measurement] = field(default_factory=list)
    details: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    def as_dict(self) -> Dict:
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "started_at": self.started_at.isoformat() + "Z",
            "ended_at": self.ended_at.isoformat() + "Z" if self.ended_at else None,
            "measurements": [
                {
                    "name": m.name,
                    "value": m.value,
                    "unit": m.unit,
                    "low": m.limit.low,
                    "high": m.limit.high,
                    "passed": m.passed,
                }
                for m in self.measurements
            ],
        }

