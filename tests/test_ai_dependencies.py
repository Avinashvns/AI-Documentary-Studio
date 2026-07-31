import importlib


def test_langchain_installed():
    assert importlib.import_module("langchain")


def test_langgraph_installed():
    assert importlib.import_module("langgraph")


def test_langchain_core_installed():
    assert importlib.import_module("langchain_core")


def test_langchain_community_installed():
    assert importlib.import_module("langchain_community")


def test_langchain_ollama_installed():
    assert importlib.import_module("langchain_ollama")