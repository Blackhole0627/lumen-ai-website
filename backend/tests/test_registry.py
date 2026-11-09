import pytest

from app.config import Settings
from app.providers.base import LLMS
from app.registry import Registry


def test_create_known_provider():
    llm = LLMS.create("mock", settings=Settings(_env_file=None))
    assert llm.__class__.__name__ == "MockLLM"


def test_unknown_provider_lists_options():
    with pytest.raises(LookupError, match="Unknown llm provider 'nope'. Registered: mock"):
        LLMS.create("nope", settings=Settings(_env_file=None))


def test_duplicate_registration_rejected():
    reg: Registry[object] = Registry("thing")
    reg.register("a")(object)
    with pytest.raises(ValueError):
        reg.register("a")(object)
