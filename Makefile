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