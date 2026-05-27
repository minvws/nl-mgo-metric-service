import mgo_metric_service
from mgo_metric_service import (
    FakeMetricsClient,
    InMemoryBackend,
    MetricFormatter,
    MetricsBackend,
    MetricsClient,
    NoopBackend,
    StatsDBackend,
)


class TestPackageExports:
    def test_public_api(self) -> None:
        assert mgo_metric_service.__all__ == [
            "MetricsBackend",
            "MetricFormatter",
            "InMemoryBackend",
            "NoopBackend",
            "StatsDBackend",
            "MetricsClient",
            "FakeMetricsClient",
        ]
        assert MetricsBackend is not None
        assert MetricFormatter is not None
        assert InMemoryBackend is not None
        assert NoopBackend is not None
        assert StatsDBackend is not None
        assert MetricsClient is not None
        assert FakeMetricsClient is not None
