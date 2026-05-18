from mgo_metric_service.formatting import NoopFormatter


class TestNoopFormatter:
    def test_format_always_returns_noop_metric(self) -> None:
        formatter = NoopFormatter()

        assert formatter.format("api.call") == "noop.metric"
        assert (
            formatter.format(
                "api.call",
                tags=(("route", "health"), ("status", "200")),
            )
            == "noop.metric"
        )
