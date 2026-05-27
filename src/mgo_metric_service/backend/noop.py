from typing import final

from mgo_metric_service.formatting import MetricFormatter, NoopFormatter

from .base import MetricsBackend


class NoopBackend(MetricsBackend):
    def incr(self, key: str, count: int = 1) -> None: ...

    def gauge(self, key: str, value: float) -> None: ...

    def timing(self, key: str, duration_ms: float) -> None: ...

    @final
    def create_formatter(self) -> MetricFormatter:
        return NoopFormatter()
