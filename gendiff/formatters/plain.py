import json

from gendiff.tree import DELETED, ADDED, CHANGED, NESTED


def format_value(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"

    return json.dumps(value)


def get_line_prefix(key_prefix):
    return f"Property '{'.'.join(key_prefix)}' was"


def get_added_line(key_prefix, values):
    value = format_value(values[0])
    return f"{get_line_prefix(key_prefix)} added with value: {value}"


def get_removed_line(key_prefix, values):
    return f"{get_line_prefix(key_prefix)} removed"


def get_updated_line(key_prefix, values):
    value1 = format_value(values[0])
    value2 = format_value(values[1])
    return f"{get_line_prefix(key_prefix)} updated. From {value1} to {value2}"


STATUS_HANDLERS = {
    ADDED: get_added_line,
    DELETED: get_removed_line,
    CHANGED: get_updated_line
}


def _walk(value, prefix=None):
    if not isinstance(value, list):
        return format_value(value)

    prefix = prefix or []
    lines = []
    for status, key, *values in value:
        key_prefix = prefix + [key]
        if status == NESTED:
            lines.extend(_walk(values[0], key_prefix))
        elif status in STATUS_HANDLERS:
            handler = STATUS_HANDLERS[status]
            lines.append(handler(key_prefix, values))

    return lines


def plain(tree):
    lines = _walk(tree)
    return '\n'.join(lines)
