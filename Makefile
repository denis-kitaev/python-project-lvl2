install:
	poetry install

gen_diff:
	poetry run gendiff

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run flake8 gendiff

test:
	poetry run pytest

check:
	make lint && make test
