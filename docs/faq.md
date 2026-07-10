# FAQ

## Why does my suite behave differently after installing pico-testing?

Because that is the point: the plugin sets `PICO_BOOT_AUTO_PLUGINS=false` for every test. If a test relied on auto-discovered plugins, mark it with `@pytest.mark.pico_auto_plugins` — or better, pass its modules explicitly to `make_container`.

## Do I still need my own conftest fixtures?

If your conftest only contained the isolation fixture and a container factory, you can delete both. Project-specific fixtures stay where they are; a local fixture named `make_container` overrides the plugin's.

## Does it work without pico-boot?

Yes. The default path uses `pico_ioc.init`. `pico_boot` is imported only when you call `make_container(boot=True)`.

## Why is shutdown newest-first?

Containers created later may depend on state from earlier ones; tearing down in reverse creation order mirrors how nested resources unwind.
