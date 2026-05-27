from mgo_metric_service import FakeMetricsClient, InMemoryBackend, MetricsClient


class TestMetricsClient:
    def test_fake_client_records_calls(self) -> None:
        client = FakeMetricsClient()

        client.incr("x", tags=(("a", "1"), ("b", "2")))

        client.assert_incr("x|tags=[a=1,b=2]")

    def test_metrics_client_with_in_memory_backend_records_calls(self) -> None:
        backend = InMemoryBackend()
        client = MetricsClient(backend=backend)

        client.incr("x", tags=(("a", "1"), ("b", "2")))

        assert backend.calls[0]["key"] == "x|tags=[a=1,b=2]"
