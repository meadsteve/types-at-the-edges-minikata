.PHONY: setup test run-0 run-1 run-2 run-3

export PYTHONPATH := $(PWD):$(PYTHONPATH)

setup:
	pipenv install

test:
	pipenv run mypy --config-file mypy.ini --warn-unused-configs diary
	pipenv run pytest diary

run-0:
	pipenv run python scripts/day_0.py

run-1:
	pipenv run python scripts/day_1.py

run-2:
	pipenv run python scripts/day_2.py

run-3:
	pipenv run python scripts/day_3.py