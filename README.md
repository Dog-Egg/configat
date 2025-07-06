# ConfigAt

[![codecov](https://codecov.io/gh/Dog-Egg/configat/graph/badge.svg?token=GmvbsZ2dBW)](https://codecov.io/gh/Dog-Egg/configat)

A simple recursive loader.

Loader syntax: `@<loader_name>[-loader_name...]:<loader_variable>`

## Installation

```sh
pip install git+https://github.com/Dog-Egg/configat.git
```

## Usage

config.py

```python
import configat 

DB_PASSWORD = configat.resolve("@env:DB_PASSWORD")
print(DB_PASSWORD)
```

```sh
$ export DB_PASSWORD=my_password

$ python config.py
my_password
```

No need to change the code. To load the password from a file, simply change the DB_PASSWORD environment.

```sh
$ echo "my_secret_password" > $(pwd)/db_password
$ export DB_PASSWORD=@file-strip:$(pwd)/db_password # A series loader is used here

$ python config.py
my_secret_password
```

## Default Loaders

* `env` - Load from a environment variable.
* `file` - Load from a file.
* `strip` - It is usually used together with other loaders, strip the whitespace characters on both sides of the content.
* `json` - Load from a JSON string.

## Type Casting

```python
import configat

PORT = configat.resolve("@env:PORT", cast=int)
```


## Configat Parser

`configat` provides a parser to extract the config expressions from the code. It is useful to generate documentation for the config.

### Installation

```sh
pip install "git+https://github.com/Dog-Egg/configat.git#egg=configat[parser]"
```

### Usage

```sh
python -m configat.parser .
```
