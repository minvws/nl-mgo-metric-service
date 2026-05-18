from typing import Any

from .backend.in_memory import InMemoryBackend
from .client import MetricsClient


class FakeMetricsClient(MetricsClient):
    """Metrics client backed by in-memory recording for tests."""

    def __init__(self) -> None:
        self._recording_backend = InMemoryBackend()
        super().__init__(self._recording_backend)

    def reset(self) -> None:
        self._recording_backend.reset()

    @property
    def call_count(self) -> int:
        return len(self._recording_backend.calls)

    def assert_metric_call(
        self,
        expected: dict[str, Any],
        *,
        times: int = 1,
    ) -> None:
        calls = self._recording_backend.calls
        matches = [
            call
            for call in calls
            if all(call.get(key) == value for key, value in expected.items())
        ]

        if len(matches) != times:
            msg = (
                f"Expected {times} metric call(s) matching {expected!r}, "
                f"found {len(matches)} among {calls!r}"
            )
            raise AssertionError(msg)

    def assert_incr(self, key: str, count: int = 1, *, times: int = 1) -> None:
        self.assert_metric_call(
            {"type": "incr", "key": key, "count": count},
            times=times,
        )

    def assert_gauge(self, key: str, value: float, *, times: int = 1) -> None:
        self.assert_metric_call(
            {"type": "gauge", "key": key, "value": value},
            times=times,
        )

    def assert_timing(self, key: str, duration_ms: float, *, times: int = 1) -> None:
        self.assert_metric_call(
            {"type": "timing", "key": key, "duration_ms": duration_ms},
            times=times,
        )
