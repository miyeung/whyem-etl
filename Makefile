IMAGE_NAME := whyemetl
CONTAINER_NAME := whyemetl_server
TAG := latest

# -----------------------------------------
# Python project setup
# -----------------------------------------

# Init pipenv local dev env and install precommit hooks
init:
	$(info *****  Installating Python pipenv local dev environment *****)
	pipenv install --dev
	$(info *****  Installing git precommit hooks *****)
	pipenv run pre-commit install

.PHONY: init

# -----------------------------------------
# Python code quality tooling
# -----------------------------------------

# Linter
flake8:
	pipenv run flake8 .

# Formatter
black:
	pipenv run black --check .

# Library dependencies check
check-deps:
	pipenv check

# Code vulnerability check
bandit:
	pipenv run bandit -r -q .

# Libraries import re-order
isort:
	pipenv run isort -rc .

# Unit tests
tests:
	pipenv run pytest --disable-pytest-warnings -v --cov-report=xml --cov=whyemetl .

# Code coverage
tests-cov:
	pipenv run codecov

# Typing check
mypy:
	pipenv run mypy whyemetl/ --ignore-missing-imports --pretty

.PHONY: flake8 black check-deps bandit isort tests tests-cov mypy

# -----------------------------------------
# Application and docker packaging
# -----------------------------------------

# Install all dependencies, generate a lock file and generated a wheel distribution
build-package: clean
	$(info *****  Installing Python dependencies *****)
	pipenv install
	$(info *****  Locking dependencies and export to a requirements.txt file *****)
	pipenv lock --requirements > requirements.txt
	$(info *****  Generating wheel dist file *****)
	pipenv run python setup.py bdist_wheel

# Generate Python wheel dist and build the docker image containing the Python web app
docker-image:
	$(info ***** Building Python package  *****)
	#docker rmi $(IMAGE_NAME):$(TAG) # TODO: do not crash if no images when
	#trying to delete it
	$(MAKE) build-package
	$(info *****  Building docker image*****)
	docker build --rm -t $(IMAGE_NAME):$(TAG) .
	$(info *****  Cleaning build dir *****)
	$(MAKE) clean

clean:
	rm -f requirements.txt
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

.PHONY: build-package docker-image clean
# -----------------------------------------
# Running application
# -----------------------------------------

docker-run:
	docker run -d --name $(IMAGE_NAME) -p 5000:5000 $(CONTAINER_NAME)

# Run Python webapp, database and BI tools altogether
compose-up:
	docker-compose -f docker-compose.yaml up

compose-stop:
	docker-compose -f docker-compose.yaml stop

compose-down:
	docker-compose -f docker-compose.yaml down

.PHONY: docker-run compose-up compose-stop compose-down
# -----------------------------------------
# Running SQL transformations in dbt/ (database has to be up)
# -----------------------------------------

dbt-check-config:
	$(info ***** Checking dbt project setup and connectivity with db *****)
	cd dbt; \
	pipenv run dbt debug

# Init the tables/views forming the data pipelines to transform data
dbt-run: dbt-check-config
	$(info ***** Running all dbt models over db *****)
	cd dbt; \
	pipenv run dbt run

# Run dbt SQL tests against data pipelines in database
dbt-tests: dbt-check-config
	$(info ***** Running dbt tests against db *****)
	cd dbt; \
	pipenv run dbt test

# Generate data pipelines documentation and create a local documentation server
# on 8080 port
dbt-docs: dbt-check-config
	$(info *****  Generate dbt docs and run docs server on localhost:8080/ *****)
	cd dbt; \
	pipenv run dbt docs generate; \
	pipenv run dbt docs serve

.PHONY: dbt-check-config dbt-run dbt-tests dbt-docs
