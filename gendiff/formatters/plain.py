from gendiff.tree import DELETED, ADDED, CHANGED, NESTED


def plain(tree):

    def _walk(value, prefix=None):
        prefix = prefix or []

        if isinstance(value, dict):
            return '[complex value]'
        if isinstance(value, bool):
            return str(value).lower()
        if value is None:
            return 'null'
        if isinstance(value, str):
            return f"'{value}'"
        if isinstance(value, int):
            return str(value)

        lines = []
        for status, key, *values in value:
            key_prefix = prefix + [key]
            key_prefix_path = '.'.join(key_prefix)
            if status == ADDED:
                lines.append(f"Property '{key_prefix_path}' was added with value: {_walk(values[0], key_prefix)}")
            elif status == DELETED:
                lines.append(f"Property '{key_prefix_path}' was removed")
            elif status == CHANGED:
                value1, value2 = values
                lines.append(f"Property '{key_prefix_path}' was updated. From {_walk(value1, key_prefix)} to {_walk(value2, key_prefix)}")
            elif status == NESTED:
                lines.extend(_walk(values[0], key_prefix))

        return lines

    lines = _walk(tree)
    return '\n'.join(lines)
