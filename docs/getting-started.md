# Getting Started

## Prerequisites

- Python >= 3.11 (tested on 3.11, 3.12, 3.13 and 3.14)
- pytest >= 8
- pico-ioc >= 2.3.3 (pico-boot only if you use `boot=True`; pico-fastapi only for `make_client`)

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
| `pico_module` (ini) | The package under test, prepended to every `make_container(...)` call |
| `make_client` | FastAPI `TestClient` over a container's app; lifespan runs, closed on teardown |

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

## Declaring the module under test

```toml
# pyproject.toml
[tool.pytest.ini_options]
pico_module = "my_package"
```

With this set, `make_container()` boots `my_package` alone and `make_container(other)` boots both — no test repeats the package name.

## Testing HTTP endpoints

```python
def test_endpoint(make_container, make_client):
    container = make_container("pico_fastapi", config={"fastapi": {"title": "t"}})
    client = make_client(container)
    assert client.get("/ping").status_code == 200
```

`make_client(container)` resolves the container's `FastAPI` app and enters a `TestClient` context, so the lifespan (and pico-fastapi's shutdown wiring) really runs. Closing it plus the fixture's own shutdown is a double `container.shutdown()` — safe on pico-ioc >= 2.3.3, which made it idempotent.

## Re-enabling auto-discovery

```python
import pytest

@pytest.mark.pico_auto_plugins
def test_full_boot(make_container):
    container = make_container(boot=True)
```

Use this only for tests that genuinely verify entry-point discovery — everything else should list its modules.
