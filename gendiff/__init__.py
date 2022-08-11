import json
import yaml


NOT_CHANGED, DELETED, ADDED = 0, 1, 2

CHANGE_REPR = {
    NOT_CHANGED: ' ',
    DELETED: '-',
    ADDED: '+'
}

NoValue = object()


def read_file(file_path):
    with open(file_path) as f:
        if file_path.endswith('.json'):
            return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.load(f, Loader=yaml.CLoader)
    raise Exception(f'Unsuported format for file `{file_path}`')


def build_diff_tree(lhs, rhs, key=None):
    lhs_is_dict = isinstance(lhs, dict)
    rhs_is_dict = isinstance(rhs, dict)
    lhs_is_no = lhs is NoValue
    rhs_is_no = rhs is NoValue

    tree = []

    if not lhs_is_dict and not rhs_is_dict:
        if not lhs_is_no and not rhs_is_no:
            if lhs == rhs:
                return [(key, NOT_CHANGED, lhs)]
            return [
                (key, DELETED, lhs),
                (key, ADDED, rhs)
            ]

        elif rhs is NoValue:
            return [(key, DELETED, lhs_value)]
        elif lhs is NoValue:
            return [(key, ADDED, rhs_value)]



    keys = list(set(lhs.keys()).union(set(rhs.keys())))
    keys.sort()


    for key in keys:
        lhs_value = lhs.get(key, NoValue)
        rhs_value = rhs.get(key, NoValue)

        if isinstance(lhs_value, dict):
            if isinstance(rhs_value, dict):
                subtree = build_diff_tree(lhs_value, rhs_value)
                tree.append((key, NOT_CHANGED, subtree))
                continue
            if rhs_value is NoValue:
                subtree = build_diff_tree(lhs_value, {})
                tree.append((key, DELETED, subtree))
                continue
            else:
                subtree = build_diff_tree(lhs_value, {})
                tree.append((key, DELETED, subtree))
                tree.append((key, ADDED, rhs_value))
                continue

        if isinstance(rhs_value, dict):
            if lhs_value is NoValue:
                subtree = build_diff_tree({}, rhs_value)
                tree.append((key, ADDED, subtree))
                continue
            else:
                subtree = build_diff_tree({}, rhs_value)
                tree.append((key, DELETED, lhs_value))
                tree.append((key, ADDED, subtree))
                continue

        if lhs_value is not NoValue and rhs_value is not NoValue:
            if lhs_value == rhs_value:
                tree.append((key, NOT_CHANGED, lhs_value))
            else:
                tree.append((key, DELETED, lhs_value))
                tree.append((key, ADDED, rhs_value))

        elif rhs_value is NoValue:
            tree.append((key, DELETED, lhs_value))
        elif lhs_value is NoValue:
            tree.append((key, ADDED, rhs_value))

    tree.sort()
    return tree


def stylish(tree):

    def _walk(subtree, depth=0):
        if isinstance(subtree, bool):
            return str(subtree).lower()
        if not isinstance(subtree, list):
            return str(subtree)

        brace_spaces = ' ' * 2 * depth
        key_spaces = ' ' * 2 * (depth + 1)
        out = ['{']
        for node in subtree:
            key = node[0]
            change_sign = CHANGE_REPR[node[1]]
            value = _walk(node[2], depth=depth + 1)
            out.append(f'{key_spaces}{change_sign} {key}: {value}')
        out.append(brace_spaces + '}')
        return '\n'.join(out)

    return _walk(tree)


def generate_diff(file1_path, file2_path):
    lhs = read_file(file1_path)
    rhs = read_file(file2_path)

    tree = build_diff_tree(lhs, rhs)
    print(tree)
    return stylish(tree)
