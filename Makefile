# Install dependencies
init:
	pip install pipenv --upgrade
	pipenv install --dev

# Run unit tests
test:
	pipenv run pytest