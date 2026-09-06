# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `__all__` declares the public API and `tests/test_exports.py` pins it, per the ecosystem stability policy (ADR-014 in pico-ioc).

### Documentation
- `docs/architecture.md` links the ADR-014 stability and deprecation policy.

## [0.2.0] - 2026-07-11

### Added

- `pico_module` ini option: declare the package under test once in pytest config; `make_container()` prepends it to every modules list.
- `make_client(container)` fixture: FastAPI `TestClient` over the container's app, lifespan running, closed on teardown.

### Changed

- pico-ioc floor raised to 2.3.3: `make_client` teardown triggers the pico-fastapi lifespan shutdown plus the fixture's own shutdown, which needs the idempotent `PicoContainer.shutdown()`.

## [0.1.0] - 2026-07-10

### Added

- Pytest plugin (entry point `pytest11`) active on install, no conftest wiring.
- Autouse isolation fixture: sets `PICO_BOOT_AUTO_PLUGINS=false` for every test.
- `@pytest.mark.pico_auto_plugins` marker to opt back into plugin auto-discovery per test.
- `make_container(*modules, config=None, boot=False)` fixture with automatic container shutdown on teardown.
