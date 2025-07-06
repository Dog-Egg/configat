import os

from configat.exceptions import NotFoundError


def env_loader(name: str):
    if name not in os.environ:
        raise NotFoundError("Environment variable not found: {!r}".format(name))
    return os.environ[name]


def file_loader(path: str):
    if not os.path.isfile(path):
        raise NotFoundError("File not found: {!r}".format(path))
    with open(path, "r") as f:
        return f.read()


def strip_loader(text: str):
    return text.strip()


def json_loader(text: str):
    import json

    return json.loads(text)
