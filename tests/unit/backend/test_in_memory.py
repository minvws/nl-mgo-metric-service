from mgo_metric_service.backend.in_memory import InMemoryBackend
from mgo_metric_service.formatting import InMemoryFormatter


class TestInMemoryBackend:
    def test_tracks_calls_and_reset(self) -> None:
        backend = InMemoryBackend()
        backend.incr("a.b", 2)
        backend.gauge("a.c", 1.5)
        backend.timing("a.d", 10.0)

        assert backend.calls == [
            {"type": "incr", "key": "a.b", "count": 2},
            {"type": "gauge", "key": "a.c", "value": 1.5},
            {"type": "timing", "key": "a.d", "duration_ms": 10.0},
        ]

        backend.reset()
        assert backend.calls == []
        assert isinstance(backend.create_formatter(), InMemoryFormatter)
