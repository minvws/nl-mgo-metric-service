from pytest_mock import MockerFixture

from mgo_metric_service.backend.statsd import StatsDBackend
from mgo_metric_service.formatting import StatsDFormatter


class TestStatsDBackend:
    def test_delegates_to_statsd_client(self, mocker: MockerFixture) -> None:
        stats_client_cls = mocker.patch(
            "mgo_metric_service.backend.statsd.StatsClient",
            autospec=True,
        )
        stats_client = stats_client_cls.return_value

        backend = StatsDBackend(host="localhost", port=8125, prefix="svc")
        backend.incr("requests", 3)
        backend.gauge("cpu", 0.7)
        backend.timing("latency", 12.5)

        stats_client_cls.assert_called_once_with(
            host="localhost", port=8125, prefix="svc"
        )
        stats_client.incr.assert_called_once_with(stat="requests", count=3)
        stats_client.gauge.assert_called_once_with(stat="cpu", value=0.7)
        stats_client.timing.assert_called_once_with(stat="latency", delta=12.5)
        assert isinstance(backend.create_formatter(), StatsDFormatter)

    def test_omits_prefix_when_not_provided(self, mocker: MockerFixture) -> None:
        stats_client_cls = mocker.patch(
            "mgo_metric_service.backend.statsd.StatsClient",
            autospec=True,
        )

        StatsDBackend(host="localhost", port=8125)

        stats_client_cls.assert_called_once_with(
            host="localhost", port=8125, prefix=None
        )
