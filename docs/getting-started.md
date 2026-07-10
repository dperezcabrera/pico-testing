# Getting Started

## Prerequisites

- Python >= 3.11
- pytest >= 8
- pico-ioc >= 2.2.0 (pico-boot only if you use `boot=True`)

## Install

```bash
pip install pico-testing
```

## Key concepts

| Piece | What it does |
|---|---|
| Isolation fixture (autouse) | Sets `PICO_BOOT_AUTO_PLUGINS=false` for every test so `pico_boot.init()` loads only explicit modules |
| `@pytest.mark.pico_auto_plugins` | Opts a single test back into plugin auto-discovery |
| `make_container` | Builds containers from explicit modules and config; shuts them all down on teardown |

## make_container

```python
def test_service(make_container):
    container = make_container(
        "my_package",                          # module objects or import strings
        config={"my_prefix": {"key": "value"}},  # dict or configuration(...) object
    )
    service = container.get(MyService)
```

Signature: `make_container(*modules, config=None, boot=False)`

- `modules` — passed to `init(modules=[...])`. Explicit is the point: list what the test needs.
- `config` — a plain dict is wrapped in `configuration(DictSource(...))`; a prepared `configuration(...)` passes through.
- `boot=True` — uses `pico_boot.init` instead of `pico_ioc.init`. Auto-discovery stays off unless the test carries the marker.

Every container created through the fixture is shut down on teardown, newest first.

## Re-enabling auto-discovery

```python
import pytest

@pytest.mark.pico_auto_plugins
def test_full_boot(make_container):
    container = make_container(boot=True)
```

Use this only for tests that genuinely verify entry-point discovery — everything else should list its modules.
