from typing import Any, final

from mgo_metric_service.formatting import InMemoryFormatter, MetricFormatter

from .base import MetricsBackend


class InMemoryBackend(MetricsBackend):
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def incr(self, key: str, count: int = 1) -> None:
        self.calls.append({"type": "incr", "key": key, "count": count})

    def gauge(self, key: str, value: float) -> None:
        self.calls.append({"type": "gauge", "key": key, "value": value})

    def timing(self, key: str, duration_ms: float) -> None:
        self.calls.append({"type": "timing", "key": key, "duration_ms": duration_ms})

    def reset(self) -> None:
        self.calls.clear()

    @final
    def create_formatter(self) -> MetricFormatter:
        return InMemoryFormatter()
