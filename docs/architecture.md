# Architecture

```
pip install pico-testing
        |
entry point pytest11 -> plugin active in every pytest run (no conftest)
        |
        +-- pico_isolation (autouse fixture)
        |     sets PICO_BOOT_AUTO_PLUGINS=false per test
        |     unless @pytest.mark.pico_auto_plugins is present
        |
        +-- make_container (factory fixture)
              init(modules=[...], config=...) via pico_ioc or pico_boot
              teardown: shutdown() newest-first
```

## Design decisions

- **Plugin, not conftest snippets**: the isolation fixture and the container
  factory were being copy-pasted into every pico repo's conftest. A `pytest11`
  entry point ships them once and activates on install — deleting code from
  every consumer.
- **Isolation is the default, discovery the exception**: a test suite must
  not change behavior because an unrelated pico plugin is installed in the
  venv (the shared-venv trap). Auto-discovery is opt-in per test via the
  marker, because only tests that verify entry-point discovery need it.
- **Local overrides win**: a `make_container` defined in a project's conftest
  shadows the plugin's — projects with special needs lose nothing.
- **Teardown newest-first**: containers created later may depend on earlier
  ones; unwinding in reverse creation order mirrors nested resources.
- **pico-boot optional**: the default path uses `pico_ioc.init`; `pico_boot`
  imports only when `boot=True` is requested, keeping the dependency floor at
  pico-ioc + pytest.
