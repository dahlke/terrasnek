SHELL := /bin/bash
CWD := $(shell pwd)

##########################
# DEV HELPERS
##########################
.PHONY: note
note:
	@ag "NOTE" --ignore Makefile

.PHONY: remote-test
remote-test:
	python3 -m unittest test/*.py

.PHONY: coverage
coverage:
	coverage run -m unittest test/*_test.py; \
	coverage report -m; \
	coverage-badge -o coverage.svg

# .PHONY: coverage
# coverage:
	# coverage run -m unittest test/*.py

.PHONY: lint-lib
lint-lib:
	pylint terrasnek terrasnek

.PHONY: lint-tests
lint-tests:
	pylint terrasnek test
