from mgo_metric_service.backend.base import MetricsBackend
from mgo_metric_service.client import MetricsClient
from mgo_metric_service.formatting.base import MetricFormatter
from mgo_metric_service.types import MetricTags


class CustomFormatter(MetricFormatter):
    def format(
        self,
        name: str,
        *,
        tags: MetricTags | None = None,
    ) -> str:
        return f"custom:{name}"


class RecordingBackend(MetricsBackend):
    def __init__(self) -> None:
        self.keys: list[str] = []

    def create_formatter(self) -> MetricFormatter:
        return CustomFormatter()

    def incr(self, key: str, count: int = 1) -> None:
        self.keys.append(key)

    def gauge(self, key: str, value: float) -> None:
        self.keys.append(key)

    def timing(self, key: str, duration_ms: float) -> None:
        self.keys.append(key)


class TestMetricsBackend:
    def test_subclass_can_define_custom_formatter(self) -> None:
        backend = RecordingBackend()

        client = MetricsClient(backend=backend)
        client.incr("request")

        assert backend.keys == ["custom:request"]
        assert isinstance(backend.create_formatter(), CustomFormatter)
