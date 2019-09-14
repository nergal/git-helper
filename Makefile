.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python ./git_helper/main.py

.PHONY: lint
lint:
	poetry run flake8 || true

.PHONY: test
test:
	poetry run pytest --cov=./ server/tests || true