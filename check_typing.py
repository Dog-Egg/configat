from typing import assert_type
import typing
import configat

assert_type(configat.resolve(""), typing.Any)
assert_type(configat.resolve("", default=True), bool | typing.Any)
assert_type(configat.resolve("", cast=int), int)
assert_type(configat.resolve("", cast=int, default=None), int | None)
assert_type(configat.resolve("", cast=int, default=True), int | bool)
