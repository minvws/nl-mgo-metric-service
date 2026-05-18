import logging

import pytest
from mgo_metric_service.client import MetricsClient
from pytest_mock import MockerFixture

from mgo_metric_service.backend.base import MetricsBackend
from mgo_metric_service.formatting.base import MetricFormatter


class TestMetricsClient:
    def test_uses_backend_formatter_by_default(self, mocker: MockerFixture) -> None:
        backend = mocker.Mock(spec=MetricsBackend)
        formatter = mocker.Mock(spec=MetricFormatter)
        backend.create_formatter.return_value = formatter
        formatter.format.return_value = "formatted.metric"

        client = MetricsClient(backend=backend)
        client.incr("request", count=2)
        client.gauge("request", value=1.2)
        client.timing("request", duration_ms=5.4)

        assert formatter.format.call_count == 3
        formatter.format.assert_any_call("request", tags=None)
        backend.incr.assert_called_once_with("formatted.metric", 2)
        backend.gauge.assert_called_once_with("formatted.metric", 1.2)
        backend.timing.assert_called_once_with("formatted.metric", 5.4)

    def test_passes_tags_to_formatter(self, mocker: MockerFixture) -> None:
        backend = mocker.Mock(spec=MetricsBackend)
        formatter = mocker.Mock(spec=MetricFormatter)
        backend.create_formatter.return_value = formatter
        formatter.format.return_value = "k"

        client = MetricsClient(backend=backend)
        tags = (("a", "1"), ("b", "2"))
        client.incr("m", tags=tags)

        formatter.format.assert_called_once_with("m", tags=tags)

    def test_repr(self, mocker: MockerFixture) -> None:
        backend = mocker.Mock(spec=MetricsBackend)
        formatter = mocker.Mock(spec=MetricFormatter)
        backend.create_formatter.return_value = formatter
        client = MetricsClient(backend=backend)

        assert repr(client) == (
            f"MetricsClient(backend={backend!r}, formatter={formatter!r})"
        )

    def test_logs_debug_on_emit(
        self,
        mocker: MockerFixture,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        caplog.set_level(logging.DEBUG, logger="mgo_metric_service.client")
        backend = mocker.Mock(spec=MetricsBackend)
        formatter = mocker.Mock(spec=MetricFormatter)
        backend.create_formatter.return_value = formatter
        formatter.format.return_value = "metric.key"

        client = MetricsClient(backend=backend)
        client.incr("request", count=2)
        client.gauge("request", value=1.2)
        client.timing("request", duration_ms=5.4)

        assert [record.getMessage() for record in caplog.records] == [
            "metric incr: metric.key count=2",
            "metric gauge: metric.key value=1.2",
            "metric timing: metric.key duration_ms=5.4",
        ]
