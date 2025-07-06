from inspect import cleandoc
import os
from pathlib import Path

import pytest
import configat
import configat.casting
from configat.exceptions import NotFoundError
from configat.main import default_configat


def test_resolve(tmp_path: Path):
    p = tmp_path / "db_password"
    p.write_text("mysecret")

    os.environ["DB_PASSWORD"] = f"@file:{p}"

    assert configat.resolve("@env:DB_PASSWORD") == "mysecret"


def test_resource_errors():
    with pytest.raises(ValueError) as e:
        assert configat.resolve("@no_such_loader:mysecret")
    assert e.value.args == ("Loader 'no_such_loader' is not found",)

    with pytest.raises(ValueError) as e:
        assert configat.resolve("xxx")
    assert e.value.args == ("Invalid expression",)


def test_resolve_default_value():
    assert configat.resolve("@env:NO_EXISTING", default="mysecret") == "mysecret"


def test_add_loader_errors():
    with pytest.raises(ValueError) as e:
        default_configat.add_loader("", lambda _: _)
    assert e.value.args == ("Loader name '' is not a valid identifier",)

    with pytest.raises(ValueError) as e:
        default_configat.add_loader("file", lambda _: _)
    assert e.value.args == ("Loader 'file' already exists",)


def test_series_loader(tmp_path: Path):
    p = tmp_path / "db_password"
    p.write_text("mysecret\n")
    assert configat.resolve(f"@file:{p}") == "mysecret\n"
    assert configat.resolve(f"@file-strip:{p}") == "mysecret"


def test_env_loader():
    with pytest.raises(NotFoundError) as e:
        assert configat.resolve("@env:NO_EXISTING")
    assert e.value.args == ("Environment variable not found: 'NO_EXISTING'",)


def test_file_loader():
    with pytest.raises(NotFoundError) as e:
        assert configat.resolve("@file:no_existing")
    assert e.value.args == ("File not found: 'no_existing'",)


def test_json_loader():
    assert configat.resolve('@json:{"a": 1}') == {"a": 1}


def test_cast():
    os.environ["DEBUG"] = "0"
    assert configat.resolve("@env:DEBUG", cast=configat.casting.boolean) is False

    os.environ["DEBUG"] = "1"
    assert configat.resolve("@env:DEBUG", cast=configat.casting.boolean) is True

    os.environ["DEBUG"] = "xxx"
    with pytest.raises(ValueError) as e:
        assert configat.resolve("@env:DEBUG", cast=configat.casting.boolean)
    assert e.value.args == ("Not a boolean value: 'xxx'",)


class TestParser:

    def test_walk_python_files(self):
        from configat.parser import walk_python_files

        assert walk_python_files(".") == [
            "./check_typing.py",
            "./tests.py",
            "./src/configat/loaders.py",
            "./src/configat/__init__.py",
            "./src/configat/casting.py",
            "./src/configat/exceptions.py",
            "./src/configat/main.py",
            "./src/configat/parser/__init__.py",
            "./src/configat/parser/__main__.py",
        ]

    def test_parse_code(self):
        from configat.parser import parse_code

        assert (
            list(
                parse_code(
                    cleandoc(
                        """
                configat.resolve('@env:ENV_VARIABLE1')
                VAR = configat.resolve('@env:ENV_VARIABLE2', help="help text")
                configat.resolve('@env:ENV_VARIABLE3', default=1)
                configat.not_existed('@env:ENV_VARIABLE3', default=1)
                configat.resolve('@env:ENV_VARIABLE4', help=help_text) # help text is not a constant
                configat.resolve(expr) # expr is not a constant
                """
                    )
                )
            )
            == [
                (
                    "@env:ENV_VARIABLE1",
                    "",
                ),
                (
                    "@env:ENV_VARIABLE2",
                    "help text",
                ),
                (
                    "@env:ENV_VARIABLE3",
                    "",
                ),
                (
                    "@env:ENV_VARIABLE4",
                    "",
                ),
            ]
        )
