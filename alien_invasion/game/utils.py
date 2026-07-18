from typing import Any, ClassVar, TypeVar, cast

T = TypeVar("T")


class Singleton(type):
    _instances: ClassVar[dict[type, object]] = {}

    def __call__(cls: type[T], *args: Any, **kwargs: Any) -> T:  # ruff:ignore[any-type]
        if cls not in Singleton._instances:
            Singleton._instances[cls] = super().__call__(*args, **kwargs)  # type: ignore[misc]
        return cast("T", Singleton._instances[cls])
