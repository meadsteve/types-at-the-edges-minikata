.PHONY: test

test:
	pipenv run pytest diary
	pipenv run mypy --ignore-missing-imports --strict-optional --check-untyped-defs diary