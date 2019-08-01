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

.PHONY: lint
lint:
	pylint terrasnek test