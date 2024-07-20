import os

import pytest

from gendiff import generate_diff


FIXTURES_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


def src_file1_path(type_, input_format):
    return os.path.join(FIXTURES_PATH, f'src/{type_}_file1.{input_format}')


def src_file2_path(type_, input_format):
    return os.path.join(FIXTURES_PATH, f'src/{type_}_file2.{input_format}')


def result(type_, output_format):
    path = os.path.join(FIXTURES_PATH, f'result/{type_}_diff_{output_format}')
    with open(path) as f:
        return f.read().strip()


@pytest.mark.parametrize('type_', ['flat', 'nested'])
@pytest.mark.parametrize('input_format', ['json', 'yaml'])
@pytest.mark.parametrize('output_format', ['stylish', 'plain'])
def test_generate_diff(type_, input_format, output_format):
    file1_path = src_file1_path(type_, input_format)
    file2_path = src_file2_path(type_, input_format)

    expected = result(type_, output_format)
    assert generate_diff(
        file1_path, file2_path, format_=output_format) == expected
