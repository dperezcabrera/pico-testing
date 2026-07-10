# pico-testing

Pytest plugin for the pico ecosystem: isolated containers by default and a `make_container` fixture with automatic shutdown.

## Install

```bash
pip install pico-testing
```

Installing it activates the plugin — no conftest wiring.

## 30-second example

```python
import sys
from pico_ioc import component

@component
class Greeter:
    def greet(self) -> str:
        return "hello"

def test_greeter(make_container):
    container = make_container(sys.modules[__name__])
    assert container.get(Greeter).greet() == "hello"
```

The container is shut down automatically when the test ends, and `PICO_BOOT_AUTO_PLUGINS=false` guarantees the test does not depend on which pico plugins happen to be installed in the venv.
