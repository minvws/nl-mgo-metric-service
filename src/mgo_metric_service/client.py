import logging
from typing import Callable

from .backend import MetricsBackend
from .types import MetricTags

logger = logging.getLogger(__name__)


class MetricsClient:
    def __init__(self, backend: MetricsBackend) -> None:
        self._backend = backend
        self._formatter = backend.create_formatter()

    def incr(
        self,
        name: str,
        count: int = 1,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        key = self._formatter.format(name, tags=tags)
        logger.debug("metric incr: %s count=%d", key, count)
        self._safe_emit(
            key,
            "incr",
            lambda key: self._backend.incr(key, count),
        )

    def gauge(
        self,
        name: str,
        value: float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        key = self._formatter.format(name, tags=tags)
        logger.debug("metric gauge: %s value=%s", key, value)
        self._safe_emit(
            key,
            "gauge",
            lambda key: self._backend.gauge(key, value),
        )

    def timing(
        self,
        name: str,
        duration_ms: float,
        *,
        tags: MetricTags | None = None,
    ) -> None:
        key = self._formatter.format(name, tags=tags)
        logger.debug("metric timing: %s duration_ms=%s", key, duration_ms)
        self._safe_emit(
            key,
            "timing",
            lambda key: self._backend.timing(key, duration_ms),
        )

    def _safe_emit(
        self,
        key: str,
        metric_type: str,
        emit: Callable[[str], None],
    ) -> None:
        try:
            emit(key)
        except Exception:
            logger.exception(
                "Failed to emit %s metric %r",
                metric_type,
                key,
            )

    def __repr__(self) -> str:
        return (
            f"MetricsClient(backend={self._backend!r}, formatter={self._formatter!r})"
        )
