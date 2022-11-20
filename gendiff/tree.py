UNCHANGED, DELETED, ADDED, CHANGED, NESTED = 0, 1, 2, 3, 4


def build_diff_tree(lhs, rhs):
    tree = []

    keys = set(lhs.keys() | rhs.keys())
    for key in keys:
        lhs_value = lhs.get(key)
        rhs_value = rhs.get(key)

        if isinstance(lhs_value, dict) and isinstance(rhs_value, dict):
            tree.append((NESTED, key, build_diff_tree(lhs_value, rhs_value)))
            continue

        if key not in lhs.keys():
            tree.append((ADDED, key, rhs_value))
        elif key not in rhs.keys():
            tree.append((DELETED, key, lhs_value))
        elif lhs_value != rhs_value:
            tree.append((CHANGED, key, lhs_value, rhs_value))
        else:
            tree.append((UNCHANGED, key, lhs_value))

    tree.sort(key=lambda n: (n[1], n[0]))
    return tree
