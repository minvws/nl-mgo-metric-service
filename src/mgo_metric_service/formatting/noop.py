from mgo_metric_service.types import MetricTags

from .base import MetricFormatter


class NoopFormatter(MetricFormatter):
    def format(
        self,
        name: str,
        *,
        tags: MetricTags | None = None,
    ) -> str:
        return "noop.metric"
