from gendiff.tree import DELETED, ADDED, CHANGED, NESTED


def _format(value):
    if isinstance(value, dict):
        return "[complex value]"
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, int):
        return str(value)


def _walk(value, prefix=None):  # noqa: C901
    prefix = prefix or []
    if not isinstance(value, list):
        return _format(value)

    lines = []
    for status, key, *values in value:
        key_prefix = prefix + [key]
        property_ = '.'.join(key_prefix)
        if status == ADDED:
            value = _walk(values[0], key_prefix)
            lines.append(
                f"Property '{property_}' was added with value: {value}")
        elif status == DELETED:
            lines.append(
                f"Property '{property_}' was removed")
        elif status == CHANGED:
            value1, value2 = values
            from_ = _walk(value1, key_prefix)
            to_ = _walk(value2, key_prefix)
            lines.append(
                f"Property '{property_}' was updated. From {from_} to {to_}")
        elif status == NESTED:
            lines.extend(_walk(values[0], key_prefix))

    return lines


def plain(tree):
    lines = _walk(tree)
    return '\n'.join(lines)
