import warnings as _warnings

_warnings.warn(
    "This module is deprecated and will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)

_BOOL_VALUES = [
    ("True", "False"),
    ("true", "false"),
    ("1", "0"),
    (1, 0),
    ("Yes", "No"),
    ("yes", "no"),
]

TRUTH_VALUES = set(v[0] for v in _BOOL_VALUES)
FALSE_VALUES = set(v[1] for v in _BOOL_VALUES)


def boolean(value):
    if value in TRUTH_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    raise ValueError("Not a boolean value: {!r}".format(value))
