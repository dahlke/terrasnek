SHELL := /bin/bash
CWD := $(shell pwd)

DOCKER_HUB_USER=eklhad
DOCKER_TEST_IMAGE_NAME=terrasnek-gh-actions-amd64
DOCKER_TEST_IMAGE_VERSION=0.1

##########################
# DEV HELPERS
##########################
.PHONY: test
test:
	python3 -m unittest test/*.py

# coverage run -m unittest test/*_test.py;
.PHONY: coverage
coverage:
	coverage run --omit 'venv/*,test/*' -m unittest test/*_test.py;
	coverage json -o coverage.tfc.json --pretty-print;
	coverage report -m;

# coverage run -m unittest test/*_test.py;
.PHONY: coverage_tfe
coverage_tfe:
	coverage run --omit 'venv/*' -m unittest test/*_test.py;
	coverage json -o coverage.tfe.json --pretty-print;
	coverage report -m;

.PHONY: coverage_report
coverage_report:
	coverage report -m

.PHONY: lint
lint:
	pylint terrasnek test | tee lint_output.txt;

.PHONY: docs
docs:
	cd docs/ && rm -rf _build/ && make html

.PHONY: open_docs
open_docs:
	open docs/_build/html/index.html;

.PHONY: todo
todo:
	@ag "TODO" --ignore Makefile

.PHONY: note
note:
	@ag "NOTE" --ignore Makefile

.PHONY: fixme
fixme:
	@ag "FIXME" --ignore Makefile

.PHONY: api_comparison
api_comparison:
	python3 scripts/python/api_comparison.py

.PHONY: codecov
codecov:
	bash <(curl -s https://codecov.io/bash)

.PHONY: pip_package
pip_package: lint api_comparison contributor_check
	python3 setup.py sdist bdist_wheel;

.PHONY: pip_publish
pip_publish: pip_package
	python3 -m twine upload dist/* --verbose --skip-existing

.PHONY: pip_test_publish
pip_test_publish: pip_package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose --skip-existing

.PHONY: contributor_check
contributor_check:
	python3 scripts/python/contributor_check.py

.PHONY: pre_release
pre_release:
	make lint;
	make api_comparison;
	make docs;
	make coverage;
	make codecov;

.PHONY: release_check
release_check:
	python3 scripts/python/contributor_check.py --release-check

.PHONY: release
release: lint api_comparison docs release_check pip_package
	make codecov;
	make pip_publish;

.PHONY: release-test
release-test: lint api_comparison docs coverage release_check pip_package
	make codecov;
	make pip_test_publish;

##########################
# DOCKER TEST IMAGE HELPERS
##########################
# GitHub Actions requires that the image be linux/amd64
docker_build:
	cp pip-reqs.txt .github/workflows/pip-reqs.txt;
	docker buildx build --platform linux/amd64 -t ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) .github/workflows/ && \
	docker tag ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) && \
	docker tag ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):latest

docker_push:
	docker push ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION)
	docker push ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):latest
