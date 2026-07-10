# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-10

### Added

- Pytest plugin (entry point `pytest11`) active on install, no conftest wiring.
- Autouse isolation fixture: sets `PICO_BOOT_AUTO_PLUGINS=false` for every test.
- `@pytest.mark.pico_auto_plugins` marker to opt back into plugin auto-discovery per test.
- `make_container(*modules, config=None, boot=False)` fixture with automatic container shutdown on teardown.
