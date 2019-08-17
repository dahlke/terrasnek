SHELL := /bin/bash
CWD := $(shell pwd)

##########################
# DEV HELPERS
##########################
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
	coverage-badge -o coverage.svg

.PHONY: lint-lib
lint-lib:
	pylint terrasnek terrasnek

.PHONY: lint-tests
lint-tests:
	pylint terrasnek test
