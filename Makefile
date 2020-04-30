SHELL := /bin/bash
CWD := $(shell pwd)

##########################
# DEV HELPERS
##########################
.PHONY: todo
todo:
	@ag "TODO" --ignore Makefile

.PHONY: note
note:
	@ag "NOTE" --ignore Makefile

.PHONY: test
test:
	python3 -m unittest test/*.py

.PHONY: coverage
coverage:
	coverage run -m unittest test/*_test.py; \
	coverage report -m; \
	rm coverage.svg; \
	coverage-badge -o coverage.svg

.PHONY: lint-lib
lint-lib:
	pylint terrasnek terrasnek

.PHONY: lint-tests
lint-tests:
	pylint terrasnek test

.PHONY: pip-package
pip-package:
	python3 setup.py sdist bdist_wheel;

.PHONY: pip-publish
pip-publish: pip-package
	python3 -m twine upload dist/*

.PHONY: pip-test-publish
pip-test-publish: pip-package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
