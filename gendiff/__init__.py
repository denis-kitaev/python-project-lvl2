import json
import yaml


class Diff:
    __slots__ = ('_key', '_value', '_type')

    def __init__(self, key, value, type_=0):
        self._key = key
        self._value = value
        self._type = type_

    def __str__(self):
        if self._type == 0:
            return f'    {self.key_value}'
        elif self._type == 1:
            return f'  + {self.key_value}'
        elif self._type == -1:
            return f'  - {self.key_value}'

    @property
    def key_value(self):
        return f'{self._key}: {self.value_string}'

    @property
    def value_string(self):
        if isinstance(self._value, bool):
            return json.dumps(self._value)
        return self._value


def read_file(file_path):
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.load(f, Loader=yaml.CLoader)
    raise Exception(f'Unsuported format for file `{file_path}`')


def generate_diff(file1_path, file2_path):
    lhs = read_file(file1_path)
    rhs = read_file(file2_path)

    keys = list(set(lhs.keys()).union(set(rhs.keys())))
    keys.sort()

    diffs = []
    for key in keys:
        if key in lhs and key in rhs and lhs[key] == rhs[key]:
            diffs.append(Diff(key, lhs[key]))
        elif key in lhs and key not in rhs:
            diffs.append(Diff(key, lhs[key], -1))
        elif key not in lhs and key in rhs:
            diffs.append(Diff(key, rhs[key], +1))
        elif key in lhs and key in rhs and lhs[key] != rhs[key]:
            diffs.append(Diff(key, lhs[key], -1))
            diffs.append(Diff(key, rhs[key], +1))

    return '{\n' + '\n'.join(map(str, diffs)) + '\n}'
