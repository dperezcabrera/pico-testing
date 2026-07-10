"""Pytest plugin: isolated pico containers by default.

Installed as a ``pytest11`` entry point — active in any venv that has
pico-testing, no conftest wiring needed.
"""

import pytest

AUTO_PLUGINS_MARKER = "pico_auto_plugins"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        f"{AUTO_PLUGINS_MARKER}: allow pico-boot plugin auto-discovery in this test "
        "(by default pico-testing sets PICO_BOOT_AUTO_PLUGINS=false)",
    )


@pytest.fixture(autouse=True)
def pico_isolation(request, monkeypatch):
    """Tests must not depend on which pico plugins happen to be installed
    in the venv — auto-discovery is opt-in via the pico_auto_plugins marker."""
    if request.node.get_closest_marker(AUTO_PLUGINS_MARKER) is None:
        monkeypatch.setenv("PICO_BOOT_AUTO_PLUGINS", "false")


@pytest.fixture
def make_container():
    """Factory for pico containers with automatic shutdown on teardown.

    Usage::

        def test_service(make_container):
            container = make_container("my_pkg", config={"my": {"key": "value"}})
            svc = container.get(MyService)
    """
    created = []

    def _make(*modules, config=None, boot=False):
        from pico_ioc import DictSource, configuration

        if config is None or isinstance(config, dict):
            config = configuration(DictSource(config or {}))
        if boot:
            from pico_boot import init
        else:
            from pico_ioc import init
        container = init(modules=list(modules), config=config)
        created.append(container)
        return container

    yield _make
    for container in reversed(created):
        container.shutdown()
