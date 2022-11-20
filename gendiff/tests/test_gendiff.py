import os

from gendiff import generate_diff


def test_flat_json():
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')

    file1_path = os.path.join(fixtures_path, 'src/flat_file1.json')
    file2_path = os.path.join(fixtures_path, 'src/flat_file2.json')
    result_path = os.path.join(fixtures_path, 'result/flat_diff_stylish')
    with open(result_path) as f:
        expected_result = f.read()
    assert generate_diff(file1_path, file2_path) == expected_result


def test_flat_yaml():
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')

    file1_path = os.path.join(fixtures_path, 'src/flat_file1.yaml')
    file2_path = os.path.join(fixtures_path, 'src/flat_file2.yaml')
    result_path = os.path.join(fixtures_path, 'result/flat_diff_stylish')
    with open(result_path) as f:
        expected_result = f.read()
    assert generate_diff(file1_path, file2_path) == expected_result


def test_nested_json():
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')

    file1_path = os.path.join(fixtures_path, 'src/nested_file1.json')
    file2_path = os.path.join(fixtures_path, 'src/nested_file2.json')
    result_path = os.path.join(fixtures_path, 'result/nested_diff_stylish')
    with open(result_path) as f:
        expected_result = f.read().strip()
    assert generate_diff(file1_path, file2_path) == expected_result


def test_nested_yaml():
    fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')

    file1_path = os.path.join(fixtures_path, 'src/nested_file1.yaml')
    file2_path = os.path.join(fixtures_path, 'src/nested_file2.yaml')
    result_path = os.path.join(fixtures_path, 'result/nested_diff_stylish')
    with open(result_path) as f:
        expected_result = f.read().strip()
    assert generate_diff(file1_path, file2_path) == expected_result
