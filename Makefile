IMAGE_NAME := whyemetl
CONTAINER_NAME := whyemetl_server
TAG := latest

init:
	pipenv install --dev
	pipenv run pre-commit install

flake8:
	pipenv run flake8 .

black:
	pipenv run black --check .

check-deps:
	pipenv check

bandit:
	pipenv run bandit -r -q .

isort:
	pipenv run isort -rc .

test:
	pipenv run pytest --disable-pytest-warnings -v .

build-package: clean
	pipenv install --dev
	pipenv lock --requirements > requirements.txt
	pipenv run python setup.py bdist_wheel

docker-image:
	#docker rmi $(IMAGE_NAME):$(TAG)
	$(MAKE) build-package
	docker build --rm -t $(IMAGE_NAME):$(TAG) .
	$(MAKE) clean

docker-run:
	docker run -d --name $(IMAGE_NAME) -p 5000:5000 $(CONTAINER_NAME)

compose-up:
	docker-compose -f docker-compose.yaml up

compose-stop:
	docker-compose -f docker-compose.yaml stop

compose-down:
	docker-compose -f docker-compose.yaml down

clean:
	rm -f requirements.txt
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
