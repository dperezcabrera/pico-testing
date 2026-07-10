import sys

from pico_ioc import component

from pico_testing import plugin


@component
class Greeter:
    def greet(self) -> str:
        return "hello"


def test_isolation_env_is_set_by_default(pytester, monkeypatch):
    monkeypatch.delenv("PICO_BOOT_AUTO_PLUGINS", raising=False)
    pytester.makepyfile(
        """
        import os

        def test_env():
            assert os.environ["PICO_BOOT_AUTO_PLUGINS"] == "false"
        """
    )
    pytester.runpytest().assert_outcomes(passed=1)


def test_marker_allows_auto_plugins(pytester, monkeypatch):
    monkeypatch.delenv("PICO_BOOT_AUTO_PLUGINS", raising=False)
    pytester.makepyfile(
        """
        import os
        import pytest

        @pytest.mark.pico_auto_plugins
        def test_env():
            assert "PICO_BOOT_AUTO_PLUGINS" not in os.environ
        """
    )
    pytester.runpytest().assert_outcomes(passed=1)


def test_marker_is_registered(pytester):
    result = pytester.runpytest("--markers")
    result.stdout.fnmatch_lines(["*pico_auto_plugins*"])


def test_make_container_resolves_components(make_container):
    container = make_container(sys.modules[__name__])
    assert container.get(Greeter).greet() == "hello"


def test_make_container_accepts_config_dict(make_container):
    container = make_container(sys.modules[__name__], config={"app": {"name": "x"}})
    assert container.get(Greeter).greet() == "hello"


def test_make_container_accepts_configuration_object(make_container):
    from pico_ioc import DictSource, configuration

    container = make_container(sys.modules[__name__], config=configuration(DictSource({})))
    assert container.get(Greeter).greet() == "hello"


def test_make_container_boot_mode(make_container):
    container = make_container(sys.modules[__name__], boot=True)
    assert container.get(Greeter).greet() == "hello"


class _FakeConfig:
    def __init__(self):
        self.lines = []

    def addinivalue_line(self, name, line):
        self.lines.append((name, line))


def test_pytest_configure_registers_marker():
    config = _FakeConfig()
    plugin.pytest_configure(config)
    name, line = config.lines[0]
    assert name == "markers"
    assert plugin.AUTO_PLUGINS_MARKER in line


class _FakeRequest:
    def __init__(self, marker):
        self.node = type("Node", (), {"get_closest_marker": staticmethod(lambda name: marker)})


class _FakeMonkeypatch:
    def __init__(self):
        self.env = {}

    def setenv(self, key, value):
        self.env[key] = value


def test_isolation_fixture_sets_env_without_marker():
    mp = _FakeMonkeypatch()
    plugin.pico_isolation.__wrapped__(_FakeRequest(marker=None), mp)
    assert mp.env == {"PICO_BOOT_AUTO_PLUGINS": "false"}


def test_isolation_fixture_skips_env_with_marker():
    mp = _FakeMonkeypatch()
    plugin.pico_isolation.__wrapped__(_FakeRequest(marker=object()), mp)
    assert mp.env == {}


def test_make_container_teardown_shuts_down_newest_first():
    gen = plugin.make_container.__wrapped__()
    factory = next(gen)
    order = []
    for label in ("first", "second"):
        container = factory(sys.modules[__name__])
        original = container.shutdown
        container.shutdown = lambda label=label, orig=original: (order.append(label), orig())
    try:
        next(gen)
    except StopIteration:
        pass
    assert order == ["second", "first"]


def test_containers_are_shut_down_on_teardown(pytester):
    pytester.makepyfile(
        """
        import sys

        shutdowns = []

        def test_creates_two_containers(make_container):
            for _ in range(2):
                container = make_container(sys.modules[__name__])
                original = container.shutdown
                container.shutdown = lambda orig=original: (shutdowns.append(1), orig())
            assert shutdowns == []

        def test_both_were_shut_down():
            assert shutdowns == [1, 1]
        """
    )
    pytester.runpytest().assert_outcomes(passed=2)
