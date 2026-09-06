"""The public API is exactly what ``__all__`` declares (stability contract)."""

import pico_testing


def test_public_api_is_declared_and_importable():
    assert set(pico_testing.__all__) == {"AUTO_PLUGINS_MARKER"}
    for name in pico_testing.__all__:
        assert getattr(pico_testing, name) is not None
