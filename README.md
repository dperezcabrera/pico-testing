# pico-testing

[![PyPI](https://img.shields.io/pypi/v/pico-testing.svg)](https://pypi.org/project/pico-testing/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/dperezcabrera/pico-testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![CI (tox matrix)](https://github.com/dperezcabrera/pico-testing/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/dperezcabrera/pico-testing/branch/main/graph/badge.svg)](https://codecov.io/gh/dperezcabrera/pico-testing)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-testing&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-testing)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-testing&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-testing)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dperezcabrera_pico-testing&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dperezcabrera_pico-testing)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pico-testing)](https://pypi.org/project/pico-testing/)
[![Docs](https://img.shields.io/badge/Docs-pico--testing-blue?style=flat&logo=readthedocs&logoColor=white)](https://dperezcabrera.github.io/pico-testing/)
[![Interactive Lab](https://img.shields.io/badge/Learn-online-green?style=flat&logo=python&logoColor=white)](https://dperezcabrera.github.io/pico-learn/)

Pytest plugin for the [pico ecosystem](https://github.com/dperezcabrera/pico-ioc): isolated containers by default and a `make_container` fixture with automatic shutdown.

## Why

Any `pico_boot.init()` in a test auto-discovers every pico plugin installed in the venv — so a test suite passes or fails depending on what else happens to be installed. Every pico project ends up copying the same two conftest fixtures. This plugin ships them once:

- **Isolation by default**: `PICO_BOOT_AUTO_PLUGINS=false` is set for every test. Opt back in per-test with `@pytest.mark.pico_auto_plugins`.
- **`make_container`**: builds containers from explicit modules and config, and shuts them all down on teardown.

## Installation

```bash
pip install pico-testing
```

No conftest wiring — installing it activates the plugin.

## Quick start

```python
import sys

def test_my_service(make_container):
    container = make_container(
        "my_package",
        config={"my_prefix": {"key": "value"}},
    )
    service = container.get(MyService)
    assert service.do_something() == "expected"
```

`make_container(*modules, config=None, boot=False)`:

- `modules`: module objects or import strings, passed to `init(modules=[...])`.
- `config`: a plain dict (wrapped in `configuration(DictSource(...))`) or a ready `configuration(...)` object.
- `boot=True`: use `pico_boot.init` instead of `pico_ioc.init` (plugin auto-discovery still off unless the test is marked).

Re-enable plugin auto-discovery for a single test:

```python
import pytest

@pytest.mark.pico_auto_plugins
def test_full_boot(make_container):
    container = make_container(boot=True)
```

## Documentation

Full documentation: https://dperezcabrera.github.io/pico-testing/

## AI Coding Skills

Install [Claude Code](https://code.claude.com) or [OpenAI Codex](https://openai.com/index/introducing-codex/) skills for AI-assisted development with pico-testing:

```bash
curl -sL https://raw.githubusercontent.com/dperezcabrera/pico-skills/main/install.sh | bash
```

The `pico-conventions` skill teaches the assistant this module's API surface and invariants; `/add-component` and `/add-tests` scaffold components and tests that use it.

## License

MIT
