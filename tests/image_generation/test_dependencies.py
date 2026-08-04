import importlib


def test_pillow_installed():
    module = importlib.import_module("PIL")

    assert module is not None


def test_httpx_installed():
    module = importlib.import_module("httpx")

    assert module is not None