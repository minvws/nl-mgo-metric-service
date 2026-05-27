import pytest

from mgo_metric_service import FakeMetricsClient


class TestFakeMetricsClient:
    def test_tracks_calls_and_reset(self) -> None:
        client = FakeMetricsClient()
        assert client.call_count == 0

        client.incr("a.b", 2)
        client.gauge("a.c", 1.5)
        client.timing("a.d", 10.0)
        assert client.call_count == 3

        client.assert_incr("a.b", 2)
        client.assert_gauge("a.c", 1.5)
        client.assert_timing("a.d", 10.0)

        client.reset()
        assert client.call_count == 0

        with pytest.raises(AssertionError):
            client.assert_incr("a.b", 2)

    def test_assert_metric_call_matches_incr_gauge_and_timing(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 3)
        client.gauge("gauge", 1.5)
        client.timing("timer", 42.0)

        client.assert_metric_call({"type": "incr", "key": "counter", "count": 3})
        client.assert_metric_call({"type": "gauge", "key": "gauge", "value": 1.5})
        client.assert_metric_call(
            {"type": "timing", "key": "timer", "duration_ms": 42.0}
        )

    def test_assert_metric_call_matches_with_partial_expected_fields(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 3)

        client.assert_metric_call({"type": "incr"})
        client.assert_metric_call({"key": "counter"})

    def test_assert_metric_call_ignores_unrelated_calls(self) -> None:
        client = FakeMetricsClient()
        client.incr("other", 1)
        client.incr("target", 2)
        client.gauge("noise", 0.0)

        client.assert_metric_call({"type": "incr", "key": "target", "count": 2})

    def test_assert_metric_call_times_matches_duplicate_calls(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 1)
        client.incr("counter", 1)

        client.assert_metric_call({"type": "incr", "key": "counter"}, times=2)

    def test_assert_metric_call_raises_when_no_match(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 1)

        with pytest.raises(AssertionError, match="Expected 1 metric call"):
            client.assert_metric_call({"type": "gauge", "key": "counter"})

    def test_assert_metric_call_raises_when_match_count_differs(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 1)

        with pytest.raises(AssertionError, match="Expected 2 metric call"):
            client.assert_metric_call({"type": "incr", "key": "counter"}, times=2)

    def test_assert_metric_call_raises_when_field_value_does_not_match(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 1)

        with pytest.raises(AssertionError, match="found 0 among"):
            client.assert_metric_call({"type": "incr", "key": "counter", "count": 2})

    def test_assert_metric_call_error_message_includes_expected_and_recorded_calls(
        self,
    ) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 1)
        expected = {"type": "gauge", "key": "counter"}

        with pytest.raises(AssertionError) as exc_info:
            client.assert_metric_call(expected)

        message = str(exc_info.value)
        assert "Expected 1 metric call(s) matching" in message
        assert repr(expected) in message
        assert "'counter'" in message
        assert "'incr'" in message

    def test_typed_assertion_helpers_for_incr_gauge_and_timing(self) -> None:
        client = FakeMetricsClient()
        client.incr("counter", 2)
        client.incr("counter", 2)
        client.gauge("gauge", 1.5)
        client.timing("timer", 42.0)

        client.assert_incr("counter", 2, times=2)
        client.assert_gauge("gauge", 1.5)
        client.assert_timing("timer", 42.0)
