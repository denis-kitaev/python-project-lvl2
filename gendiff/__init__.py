import json
import yaml
from enum import Enum, auto


class Change(Enum):
    NO = auto(),
    ADDED = auto(),
    DELETED = auto()


class Node:
    def __init__(self, key, value, change=Change.NO, level=0):
        self._key = key
        self._value = value
        self._change = change
        self._children = []
        self.level = level

    def __str__(self):
        out = '  ' * (self.level + 1)
        if self._change == Change.NO:
            out += f'  {self.key_value}'
        elif self._change == Change.ADDED:
            out += f'+ {self.key_value}'
        elif self._change == Change.DELETED:
            out += f'- {self.key_value}'
        return out

    @property
    def key_value(self):
        return f'{self._key}: {self.value_string}'

    @property
    def value_string(self):
        if isinstance(self._value, bool):
            return json.dumps(self._value)
        return self._value

    def add_child(self, node):
        self._children.append(node)

    def to_string(self):
        # return str(self)
        return '{\n' + '\n'.join(map(str, self._children)) + '\n}'


def read_file(file_path):
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.load(f, Loader=yaml.CLoader)
    raise Exception(f'Unsuported format for file `{file_path}`')


def generate_diff_item(lhs, rhs, tree=None):
    keys = list(set(lhs.keys()).union(set(rhs.keys())))
    keys.sort()

    tree = tree or Node(None, None)
    for key in keys:
        if isinstance(lhs.get(key), dict) and isinstance(rhs.get(key), dict):
            subtree = Node(key, None, level=tree.level + 1)
            tree.add_child(subtree)
            generate_diff_item(lhs.get(key, {}), rhs.get(key, {}), subtree)
        if key in lhs and key in rhs and lhs[key] == rhs[key]:
            tree.add_child(Node(key, lhs[key]))
        elif key in lhs and key not in rhs:
            tree.add_child(Node(key, lhs[key], Change.DELETED))
        elif key not in lhs and key in rhs:
            tree.add_child(Node(key, rhs[key], Change.ADDED))
        elif key in lhs and key in rhs and lhs[key] != rhs[key]:
            tree.add_child(Node(key, lhs[key], Change.DELETED))
            tree.add_child(Node(key, rhs[key], Change.ADDED))

    return tree


def generate_diff(file1_path, file2_path):
    lhs = read_file(file1_path)
    rhs = read_file(file2_path)

    diff = generate_diff_item(lhs, rhs)
    return diff.to_string()
