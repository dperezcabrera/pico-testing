import sys

from pico_fastapi import controller, get


@controller(prefix="/ping")
class PingController:
    @get("")
    async def ping(self):
        return {"ok": True}


def test_make_client_serves_app_with_lifespan(make_container, make_client):
    container = make_container("pico_fastapi", sys.modules[__name__], config={"fastapi": {"title": "t"}})
    client = make_client(container)
    assert client.get("/ping").json() == {"ok": True}


def test_make_client_teardown_survives_double_shutdown(pytester):
    pytester.makepyfile(
        """
        import sys

        from pico_fastapi import controller, get

        @controller(prefix="/ping")
        class PingController:
            @get("")
            async def ping(self):
                return {"ok": True}

        def test_request(make_container, make_client):
            container = make_container("pico_fastapi", sys.modules[__name__], config={"fastapi": {"title": "t"}})
            client = make_client(container)
            assert client.get("/ping").status_code == 200
        """
    )
    # client exit fires the pico-fastapi lifespan shutdown AND make_container
    # shuts down again on teardown; errors here would fail the run
    pytester.runpytest().assert_outcomes(passed=1)


def test_pico_module_ini_is_prepended(pytester):
    pytester.makeini(
        """
        [pytest]
        pico_module = test_pico_module_ini_is_prepended
        """
    )
    pytester.makepyfile(
        """
        from pico_ioc import component

        @component
        class Greeter:
            def greet(self):
                return "hi"

        def test_no_modules_needed(make_container):
            assert make_container().get(Greeter).greet() == "hi"
        """
    )
    pytester.runpytest().assert_outcomes(passed=1)
