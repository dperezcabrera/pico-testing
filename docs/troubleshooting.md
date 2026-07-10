# Troubleshooting

## Installing pico-testing changed my suite's behavior

That is the feature: `PICO_BOOT_AUTO_PLUGINS=false` is now set for every
test. A test that relied on auto-discovered plugins needs
`@pytest.mark.pico_auto_plugins` — or better, list its modules explicitly in
`make_container`.

## ProviderNotFoundError inside make_container

The component's module is not in the `modules` list. Pass module objects or
import strings for everything the test resolves: `make_container("my_pkg",
sys.modules[__name__])`.

## My conftest already defines make_container

Keep it — a local fixture overrides the plugin's. Delete it when it no longer
does anything the plugin doesn't.

## make_container(boot=True) raises ImportError

`boot=True` uses `pico_boot.init`; install pico-boot in the test env.

## Coverage misses the plugin's own lines (plugin authors)

pytest plugins load before `pytest --cov` starts coverage. Measure with
`coverage run -m pytest tests` instead — that is how this repo's own cov env
works.
