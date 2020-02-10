.PHONY: setup test run-0 run-1 run-2

export PYTHONPATH := $(PWD):$(PYTHONPATH)

setup:
	pipenv install

test:
	pipenv run pytest diary
	pipenv run mypy --ignore-missing-imports --strict-optional --check-untyped-defs diary

run-0:
	pipenv run python scripts/day_0.py

run-1:
	pipenv run python scripts/day_1.py

run-2:
	pipenv run python scripts/day_2.py