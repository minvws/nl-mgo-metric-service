from typing import final

from statsd import StatsClient

from mgo_metric_service.formatting import MetricFormatter, StatsDFormatter

from .base import MetricsBackend


class StatsDBackend(MetricsBackend):
    def __init__(self, host: str, port: int, prefix: str | None = None) -> None:
        self._client = StatsClient(host=host, port=port, prefix=prefix)

    def incr(self, key: str, count: int = 1) -> None:
        self._client.incr(stat=key, count=count)

    def gauge(self, key: str, value: float) -> None:
        self._client.gauge(stat=key, value=value)

    def timing(self, key: str, duration_ms: float) -> None:
        self._client.timing(stat=key, delta=duration_ms)

    @final
    def create_formatter(self) -> MetricFormatter:
        return StatsDFormatter()
