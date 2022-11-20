import json

from gendiff.tree import UNCHANGED, DELETED, ADDED, CHANGED, NESTED


REPLACER = ' '


def get_key_spaces(depth):
    return REPLACER * ((depth * 4) + 2)


def get_quote_spaces(depth):
    return REPLACER * (depth * 4)


def format_value(value, depth):
    if isinstance(value, dict):
        key_spaces = get_key_spaces(depth)
        quote_spaces = get_quote_spaces(depth)
        lines = ['{']
        for k, v in value.items():
            lines.append(f'{key_spaces}  {k}: {format_value(v, depth + 1)}')
        lines.append(f'{quote_spaces}}}')
        return lines

    return json.dumps(value)


def get_unchanged_line(depth, key, values):
    key_spaces = get_key_spaces(depth)
    value = format_value(values[0], depth)
    return f'{key_spaces}  {key}: {value}'


def get_added_line(depth, key, values):
    key_spaces = get_key_spaces(depth)
    value = format_value(values[0], depth + 1)
    return f'{key_spaces}+ {key}: {value}'


def get_deleted_line(depth, key, values):
    key_spaces = get_key_spaces(depth)
    value = format_value(values[0], depth + 1)
    return f'{key_spaces}- {key}: {value}'


def get_changed_line(depth, key, values):
    value1 = format_value(values[0], depth + 1)
    value2 = format_value(values[1], depth + 1)
    key_spaces = get_key_spaces(depth)
    return (
        f'{key_spaces}- {key}: {value1}\n'
        f'{key_spaces}+ {key}: {value2}'
    )


STATUS_HANDLERS = {
    UNCHANGED: get_unchanged_line,
    ADDED: get_added_line,
    DELETED: get_deleted_line,
    CHANGED: get_changed_line
}


def stylish(tree):

    def _walk(value, depth=0):
        lines = []
        for status, key, *values in value:
            if status in STATUS_HANDLERS:
                handler = STATUS_HANDLERS[status]
                lines.append(handler(depth, key, values))
            elif status == NESTED:
                key_spaces = get_key_spaces(depth)
                lines.append(f'{key_spaces}  {key}: {{')
                lines.extend(_walk(values[0], depth + 1))
                # lines.append(
                #     f'{key_spaces}  {key}: {_walk(values[0], depth + 1)}')
                quote_spaces = get_quote_spaces(depth + 1)
                lines.append(f'{quote_spaces}}}')

        # quote_spaces = get_quote_spaces(depth)
        # lines.append(f'{quote_spaces}}}')
        return lines

    return '{' + '\n'.join(_walk(tree)) + '}'
