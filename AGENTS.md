# pico-testing

Pytest plugin for the pico ecosystem: isolated containers by default and a make_container fixture.

## Commands

```bash
pip install -e ".[dev]"
pytest tests/ -v
pytest --cov=pico_testing --cov-report=term-missing tests/
mkdocs serve -f mkdocs.yml
```

## Project Structure

```
src/pico_testing/
  __init__.py       # Re-exports AUTO_PLUGINS_MARKER
  plugin.py         # pytest11 entry point: pico_isolation (autouse) + make_container
```

## Key Concepts

- Entry point `pytest11` -> active on install, no conftest wiring.
- `pico_isolation` (autouse) sets PICO_BOOT_AUTO_PLUGINS=false per test; opt back in with `@pytest.mark.pico_auto_plugins`.
- `make_container(*modules, config=dict|configuration, boot=False)`; teardown shuts containers newest-first.
- A local conftest `make_container` overrides the plugin's.
- Coverage of the plugin itself needs `coverage run -m pytest` (plugins import before pytest --cov starts).

## Boundaries

- pico-boot import stays lazy (only `boot=True`)
- Never auto-enable plugin discovery
- Do not modify `_version.py`
