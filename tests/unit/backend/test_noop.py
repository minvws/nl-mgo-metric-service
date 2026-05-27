from mgo_metric_service.backend.noop import NoopBackend
from mgo_metric_service.formatting import NoopFormatter


class TestNoopBackend:
    def test_methods_do_not_raise(self) -> None:
        backend = NoopBackend()
        backend.incr("a.b")
        backend.gauge("a.c", 1.0)
        backend.timing("a.d", 1.0)
        assert isinstance(backend.create_formatter(), NoopFormatter)
