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
	coverage report -m;

.PHONY: tfc_coverage
tfc_coverage:
	coverage run -m unittest test/*_test.py -o tfc_coverage.xml; \
	coverage report -m;

.PHONY: lint
lint:
	pylint terrasnek test

.PHONY: docs
docs:
	cd docs/ && make html

.PHONY: api_comparison
api_comparison:
	python3 scripts/python/api_comparison.py

.PHONY: codecov
codecov:
	bash <(curl -s https://codecov.io/bash)

.PHONY: pip-package
pip-package:
	python3 setup.py sdist bdist_wheel;

.PHONY: pip-publish
pip-publish: pip-package
	python3 -m twine upload dist/*

.PHONY: pip-test-publish
pip-test-publish: pip-package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
