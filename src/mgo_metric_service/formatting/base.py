from typing import Protocol

from mgo_metric_service.types import MetricTags


class MetricFormatter(Protocol):
    def format(
        self,
        name: str,
        *,
        tags: MetricTags | None = None,
    ) -> str: ...
