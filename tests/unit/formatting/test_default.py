from mgo_metric_service.formatting import InMemoryFormatter


class TestDefaultFormatter:
    def test_format_without_tags(self) -> None:
        formatter = InMemoryFormatter()
        assert formatter.format("api.call") == "api.call"
        assert formatter.format("api.call", tags=()) == "api.call"

    def test_format_with_tags(self) -> None:
        formatter = InMemoryFormatter()
        assert (
            formatter.format(
                "api.call",
                tags=(("route", "health"), ("status", "200")),
            )
            == "api.call|tags=[route=health,status=200]"
        )
