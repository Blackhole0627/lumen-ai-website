"""A tiny registry: maps a name (from config) to a class that implements an interface.

    LLMS = Registry[LanguageModel]("llm")

    @LLMS.register("mock")
    class MockLLM(LanguageModel): ...

    llm = LLMS.create(settings.llm_provider, settings=settings)

Swapping a vendor is then a config change (LLM_PROVIDER=myvendor), not a code change
in the services that use it.
"""
from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    def __init__(self, kind: str) -> None:
        self.kind = kind
        self._factories: dict[str, Callable[..., T]] = {}

    def register(self, name: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
        def decorator(factory: Callable[..., T]) -> Callable[..., T]:
            if name in self._factories:
                raise ValueError(f"{self.kind} provider '{name}' is already registered")
            self._factories[name] = factory
            return factory

        return decorator

    def create(self, name: str, **kwargs: Any) -> T:
        try:
            factory = self._factories[name]
        except KeyError:
            known = ", ".join(self.names()) or "none"
            raise LookupError(f"Unknown {self.kind} provider '{name}'. Registered: {known}") from None
        return factory(**kwargs)

    def names(self) -> list[str]:
        return sorted(self._factories)

    def __contains__(self, name: str) -> bool:
        return name in self._factories
