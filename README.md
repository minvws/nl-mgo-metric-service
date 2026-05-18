# mgo-metric-service

A metrics client for Python, to register metrics with support for various
backends (e.g., StatsD) while keeping application code decoupled from metrics
implementation details.

This library offers a minimal, composable interface for emitting application
metrics (counters, gauges, timings) with flexible formatting and tagging
support.

---

## Installation

```bash
uv add "mgo-metric-service @ git+https://github.com/minvws/nl-mgo-metric-service.git"
```

---

## How it Works

The core of `mgo-metric-service` is the `MetricsClient`, which delegates metric
emission to a backend. You provide a backend instance (such as `StatsDBackend`,
`InMemoryBackend`, or `NoopBackend`). Each built-in backend uses a fixed
formatter; custom formatters are only supported on backends you define by
subclassing `MetricsBackend`.

The structure is:

- **Backends**: Handle communication with the actual metrics server or transport
  (e.g., StatsD), in-memory recording, or no-op for ignored metrics.
- **Formatters**: Define how metric names and tags are turned into the final key
  for transmission.
- **MetricsClient**: The high-level API your app uses (`incr`, `gauge`,
  `timing`), delegating formatting and transport.

---

## Usage

### Basic Example with the StatsD Backend

```python
from mgo_metric_service import MetricsClient, StatsDBackend

# Set up your backend; point to the StatsD server (defaults shown)
backend = StatsDBackend(host="localhost", port=8125)

# Create your metrics client
client = MetricsClient(backend=backend)

# Emit a counter increment (with optional tags)
client.incr("api.request", count=1, tags=(("route", "health"), ("status", "200")))

# Emit a gauge metric
client.gauge("db.connections", value=5)

# Measure timing (in milliseconds)
client.timing("process.time_ms", duration_ms=42.3)
```

### No-Op Backend for Testing

```python
from mgo_metric_service import MetricsClient, NoopBackend

client = MetricsClient(backend=NoopBackend())
client.incr("any.metric")  # Does nothing
```

### Fake Metrics Client for Testing

For tests where you want to assert that specific metrics were emitted, use
`FakeMetricsClient` and its assertion helpers.

```python
from mgo_metric_service import FakeMetricsClient

client = FakeMetricsClient()

client.incr("request.count", count=2)
client.gauge("memory.usage", value=123.4)
client.timing("db.latency", duration_ms=7.89)

# Assert that a matching metric was emitted
client.assert_metric_call({"type": "gauge", "key": "memory.usage", "value": 123.4})

# You can partially match fields
client.assert_metric_call({"type": "incr"})

# Or require that a metric was called multiple times
client.incr("request.count")
client.assert_metric_call({"type": "incr", "key": "request.count"}, times=2)

# Convenience helpers for exact typed assertions
client.assert_incr("request.count", count=2)
client.assert_gauge("memory.usage", value=123.4)
client.assert_timing("db.latency", duration_ms=7.89)
client.assert_incr("request.count", count=1, times=1)
```

---

### Customizing Metric Formatting

Built-in backends (`StatsDBackend`, `InMemoryBackend`, `NoopBackend`) ship with
a fixed formatter and cannot be overridden. To use a custom formatter, subclass
`MetricsBackend` and implement `create_formatter()`:

```python
from mgo_metric_service import MetricsBackend, MetricsClient
from mgo_metric_service.formatting import MetricFormatter
from your_app.formatter import CustomFormatter


class CustomBackend(MetricsBackend):
    def create_formatter(self) -> MetricFormatter:
        return CustomFormatter()

    def incr(self, key: str, count: int = 1) -> None:
        ...

    def gauge(self, key: str, value: float) -> None:
        ...

    def timing(self, key: str, duration_ms: float) -> None:
        ...


client = MetricsClient(backend=CustomBackend())
```

---

## Running Tests with Coverage

```bash
make test
```
