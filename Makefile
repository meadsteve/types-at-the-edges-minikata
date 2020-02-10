.PHONY: test run-0

export PYTHONPATH := $(PWD):$(PYTHONPATH)

test:
	pipenv run pytest diary
	pipenv run mypy --ignore-missing-imports --strict-optional --check-untyped-defs diary

run-0:
	pipenv run python scripts/day_0.py