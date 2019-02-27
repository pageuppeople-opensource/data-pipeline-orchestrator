# Install dependencies
install_deps:
	pip install pipenv --upgrade
	pipenv install --dev

# Run unit tests
test:
	pipenv run pytest