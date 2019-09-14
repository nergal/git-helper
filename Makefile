.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python ./git_helper/main.py create

.PHONY: lint
lint:
	poetry run flake8

.PHONY: test
test:
	poetry run pytest tests

.PHONY: clean
clean:
	find . -type f -name *.pyc | xargs rm -f
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name *.egg-info | xargs rm -rf