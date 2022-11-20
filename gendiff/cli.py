import argparse

from gendiff.formatters import FORMATTERS, DEFAULT_FORMAT


def build_args():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('--format', default=DEFAULT_FORMAT, choices=FORMATTERS.keys())

    return parser.parse_args()
