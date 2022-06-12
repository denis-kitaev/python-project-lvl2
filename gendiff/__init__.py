import json


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


def generate_diff(file1_path, file2_path):
    with open(file1_path) as f:
        d1 = json.load(f)

    with open(file2_path) as f:
        d2 = json.load(f)

    keys = list(set(d1.keys()).union(set(d2.keys())))
    keys.sort()

    diffs = []
    for key in keys:
        if key in d1 and key in d2 and d1[key] == d2[key]:
            diffs.append(Diff(key, d1[key]))
        elif key in d1 and key not in d2:
            diffs.append(Diff(key, d1[key], -1))
        elif key not in d1 and key in d2:
            diffs.append(Diff(key, d2[key], +1))
        elif key in d1 and key in d2 and d1[key] != d2[key]:
            diffs.append(Diff(key, d1[key], -1))
            diffs.append(Diff(key, d2[key], +1))

    return '{\n' + '\n'.join(map(str, diffs)) + '\n}'
