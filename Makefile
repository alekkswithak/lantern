install:
		poetry install --no-root

dev:
	  poetry run fastapi dev src/main.py

test:
	  poetry run python src/tests/

.PHONY: install dev
