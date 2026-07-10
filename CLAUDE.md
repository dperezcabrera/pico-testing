Read and follow ./AGENTS.md for project conventions.

## Pico Ecosystem Context

pico-testing — Pytest plugin for the pico ecosystem: isolated containers by default and a make_container fixture. Active on install via the `pytest11` entry point (NOT a pico_boot module). See it wired with the whole ecosystem in the flagship use case (pico-boot docs).

## Key Reminders

- pico-ioc dependency: `>= 2.2.0`; pytest `>= 8`
- The tox cov env MUST keep `coverage run -m pytest` (import-time lines)
- **NEVER change `version_scheme`** in pyproject.toml. It MUST remain `"post-release"`.
- requires-python >= 3.11
- Commit messages: one line only
