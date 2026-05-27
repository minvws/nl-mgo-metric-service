from mgo_metric_service.types import MetricTags

from .base import MetricFormatter


class InMemoryFormatter(MetricFormatter):
    def format(
        self,
        name: str,
        *,
        tags: MetricTags | None = None,
    ) -> str:
        if not tags:
            return name

        tag_part = ",".join(f"{key}={value}" for key, value in tags)
        return f"{name}|tags=[{tag_part}]"
