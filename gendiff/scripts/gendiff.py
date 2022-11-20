from gendiff import generate_diff
from gendiff.cli import build_args


def main():
    args = build_args()
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main()
