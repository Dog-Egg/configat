from __future__ import annotations

import re
import typing

from . import loaders
from .exceptions import NotFoundError


_AT_LOADER_EXPR_PATTERN = re.compile(r"^@(?P<name>.*?):(?P<variable>.+)$")


_missing = object()

T = typing.TypeVar("T")
P = typing.TypeVar("P")


class ConfigAt:
    def __init__(self):
        self.__loaders: dict[str, typing.Callable[[str], typing.Any]] = {}

    def add_loader(self, name: str, func: typing.Callable[[str], typing.Any]):
        if name in self.__loaders:
            raise ValueError(f"Loader {name!r} already exists")
        if not name.isidentifier():
            raise ValueError(f"Loader name {name!r} is not a valid identifier")
        self.__loaders[name] = func

    def __resolve(self, expr: str | typing.Any, strict: bool):
        if not isinstance(expr, str):
            return expr

        match = _AT_LOADER_EXPR_PATTERN.match(expr)
        if match is None:
            if strict:
                raise ValueError("Invalid expression")
            return expr

        name = match.group("name")
        variable = match.group("variable")

        for loader in self._get_loaders(name):
            variable = loader(variable)
        return self.__resolve(variable, False)

    def _get_loaders(self, name: str):
        for n in name.split("-"):
            if n not in self.__loaders:
                raise ValueError(f"Loader {n!r} is not found")
        return [self.__loaders[n] for n in name.split("-")]

    @typing.overload
    def resolve(self, expr: str, /, *, help: str | None = None) -> typing.Any: ...

    @typing.overload
    def resolve(
        self,
        expr: str,
        /,
        default: T,
        *,
        help: str | None = None,
    ) -> typing.Any | T: ...

    @typing.overload
    def resolve(
        self,
        expr: str,
        /,
        *,
        cast: typing.Callable[[typing.Any], T],
        help: str | None = None,
    ) -> T: ...

    @typing.overload
    def resolve(
        self,
        expr: str,
        /,
        default: T,
        cast: typing.Callable[[typing.Any], P],
        help: str | None = None,
    ) -> T | P: ...

    def resolve(
        self,
        expr,
        /,
        default=_missing,
        cast=None,
        help: str | None = None,
    ):
        try:
            value = self.__resolve(expr, True)
        except NotFoundError:
            if default is _missing:
                raise
            return default
        if cast is not None:
            return cast(value)
        return value


default_configat = ConfigAt()
default_configat.add_loader("env", loaders.env_loader)
default_configat.add_loader("file", loaders.file_loader)
default_configat.add_loader("strip", loaders.strip_loader)
default_configat.add_loader("json", loaders.json_loader)
