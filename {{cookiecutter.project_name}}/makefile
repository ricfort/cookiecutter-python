# https://www.gnu.org/software/make/manual/make.html
SHELL=bash
.PHONY: default
default:

py_source=./src
py_tests=./tests

docker=docker


.PHONY: poetry-install
poetry-install:
	python -m pip install --require-hashes --requirement requirements-poetry.txt

.PHONY: test
test:
	poetry run pytest --junitxml=test-results.xml --cov-config=.coveragerc --cov=$(py_source)/{{cookiecutter.org_name}} --cov-report=xml $(py_tests)

.PHONY: validate-static
validate-static:
	poetry check
	poetry run python -m isort --check-only $(py_source) $(py_tests)
	poetry run python -m black --config ./pyproject.toml --check $(py_source) $(py_tests)
	poetry run flake8 $(py_source) $(py_tests)
	poetry run mypy --show-error-codes --show-error-context --pretty $(py_source) $(py_tests)

.PHONY: validate-fix
validate-fix:
	poetry run python -m isort $(py_source) $(py_tests)
	poetry run python -m black --config ./pyproject.toml $(py_source) $(py_tests)


.PHONY: poetry-generate-dependencies
poetry-generate-dependencies:
	$(docker) pull docker.io/library/python:$(python_image_digest) || exit 1
	$(docker) run docker.io/library/python:$(python_image_digest) /bin/bash -c "python -m pip -qq install pip-tools && echo poetry==$(poetry_version) | pip-compile --quiet --generate-hashes - --output-file -" &> ./poetry-requirements.txt
