import re

from mgo_metric_service.types import MetricTags

from .base import MetricFormatter
from .exceptions import InvalidFormat

_VALID_METRIC_KEY_REGEX = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)*$")


class StatsDFormatter(MetricFormatter):
    def format(
        self,
        name: str,
        *,
        tags: MetricTags | None = None,
    ) -> str:
        if not tags:
            key = name
        else:
            tag_part = ".".join(f"{key}.{value}" for key, value in tags)
            key = f"{name}.{tag_part}"

        if not _VALID_METRIC_KEY_REGEX.fullmatch(key):
            raise InvalidFormat(f"Invalid metric key: {key}")

        return key
