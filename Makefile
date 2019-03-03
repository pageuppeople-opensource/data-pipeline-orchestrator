# Install dependencies
install_deps:
	pip install pipenv --upgrade
	pipenv install --dev

# Run unit tests
test_unit:
	pipenv run pytest

# Run integration tests
test_integration:
	./tests/integration/test_integration.sh
	
