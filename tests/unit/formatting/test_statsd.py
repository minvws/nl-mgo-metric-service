import pytest

from mgo_metric_service.formatting import InvalidFormat, StatsDFormatter


class TestStatsDFormatter:
    def test_format_without_tags(self) -> None:
        formatter = StatsDFormatter()
        assert formatter.format("http_request") == "http_request"

    def test_format_with_tags(self) -> None:
        formatter = StatsDFormatter()
        assert (
            formatter.format(
                "http_request",
                tags=(("route", "health"), ("status", "200")),
            )
            == "http_request.route.health.status.200"
        )

    def test_rejects_invalid_keys(self) -> None:
        formatter = StatsDFormatter()

        with pytest.raises(InvalidFormat, match="Invalid metric key: Http.Request"):
            formatter.format("Http.Request")

        with pytest.raises(InvalidFormat, match="Invalid metric key:"):
            formatter.format(
                "http_request",
                tags=(("route", "bad-key"),),
            )

    def test_raises_invalid_format_for_invalid_metric_key(
        self,
    ) -> None:
        formatter = StatsDFormatter()
        with pytest.raises(InvalidFormat, match="Invalid metric key: Http.Request"):
            formatter.format("Http.Request")
