import json

from gendiff.tree import UNCHANGED, DELETED, ADDED, CHANGED, NESTED


def stylish(tree):
    replacer = ' '

    def _walk(value, depth=0):
        if isinstance(value, (bool, str, int)) or value is None:
            return json.dumps(value)

        key_spaces = replacer * ((depth * 4) + 2)
        quote_spaces = replacer * (depth * 4)

        lines = ['{']

        if isinstance(value, dict):
            for k, v in value.items():
                lines.append(f'{key_spaces}  {k}: {_walk(v, depth + 1)}')

        else:
            for status, key, *values in value:
                value1 = _walk(values[0], depth + 1)

                if status == UNCHANGED:
                    lines.append(f'{key_spaces}  {key}: {value1}')
                elif status == ADDED:
                    lines.append(f'{key_spaces}+ {key}: {value1}')
                elif status == DELETED:
                    lines.append(f'{key_spaces}- {key}: {value1}')
                elif status == CHANGED:
                    value2 = _walk(values[1], depth + 1)
                    lines.append(f'{key_spaces}- {key}: {value1}')
                    lines.append(f'{key_spaces}+ {key}: {value2}')
                elif status == NESTED:
                    lines.append(f'{key_spaces}  {key}: {value1}')

        lines.append(f'{quote_spaces}}}')
        return '\n'.join(lines)

    return _walk(tree)
