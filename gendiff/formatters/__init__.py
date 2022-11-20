from .stylish import stylish
from .plain import plain
from .json import json_


FORMATTERS = {
    'stylish': stylish,
    'plain': plain,
    'json': json_
}

DEFAULT_FORMAT = 'stylish'


def get_formatter(format_):
    return FORMATTERS[format_]
