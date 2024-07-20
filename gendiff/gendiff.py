import json
import yaml

from gendiff.tree import build_diff_tree
from gendiff.formatters import get_formatter, DEFAULT_FORMAT


FILE_LOADERS = {
    'json': json.load,
    'yaml': lambda f: yaml.load(f, Loader=yaml.CLoader),
    'yml': lambda f: yaml.load(f, Loader=yaml.CLoader),
}


def parse_file(file_path):
    file_ext = file_path.split('.')[-1]
    file_loader = FILE_LOADERS[file_ext]

    with open(file_path) as f:
        return file_loader(f)


def generate_diff(file1_path, file2_path, format_=DEFAULT_FORMAT):
    lhs = parse_file(file1_path)
    rhs = parse_file(file2_path)

    tree = build_diff_tree(lhs, rhs)
    formatter = get_formatter(format_)
    return ''
    return formatter(tree)
