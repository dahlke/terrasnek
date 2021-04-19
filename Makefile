SHELL := /bin/bash
CWD := $(shell pwd)

DOCKER_HUB_USER=eklhad
DOCKER_TEST_IMAGE_NAME=terrasnek-circleci
DOCKER_TEST_IMAGE_VERSION=0.3

##########################
# DEV HELPERS
##########################
.PHONY: test
test:
	python3 -m unittest test/*.py

.PHONY: coverage
coverage:
	coverage run -m unittest test/*_test.py;
	coverage report -m;

.PHONY: coverage_report
coverage_report:
	coverage report -m;

.PHONY: lint
lint:
	pylint terrasnek test | tee lint_output.txt;

.PHONY: docs
docs:
	cd docs/ && rm -rf _build/ && make html

.PHONY: api_comparison
api_comparison:
	python3 scripts/python/api_comparison.py

.PHONY: circleci_env
circleci_env:
	bash scripts/shell/upload_circleci_env_vars.sh

.PHONY: codecov
codecov:
	bash <(curl -s https://codecov.io/bash)

.PHONY: pip-package
pip-package: lint api_comparison contributor_check
	python3 setup.py sdist bdist_wheel;

.PHONY: pip-publish
pip-publish: pip-package
	python3 -m twine upload dist/* --verbose --skip-existing

.PHONY: pip-test-publish
pip-test-publish: pip-package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose --skip-existing

.PHONY: contributor_check
contributor_check:
	python3 scripts/python/contributor_check.py

.PHONY: release_check
release_check:
	python3 scripts/python/contributor_check.py --release-check

.PHONY: release
release: lint api_comparison docs release_check pip-package
	make codecov;
	make pip-publish;

.PHONY: release-test
release-test: lint api_comparison docs coverage release_check pip-package
	make codecov;
	make pip-test-publish;

##########################
# DOCKER TEST IMAGE HELPERS
##########################
docker_build:
	cp pip-reqs.txt .circleci/pip-reqs.txt;
	docker build -t ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) .circleci/ && \
	docker tag ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) && \
	docker tag ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION) ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):latest

docker_push:
	docker push ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):$(DOCKER_TEST_IMAGE_VERSION)
	docker push ${DOCKER_HUB_USER}/$(DOCKER_TEST_IMAGE_NAME):latest