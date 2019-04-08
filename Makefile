# Install dependencies
install_deps:
	pip install pipenv --upgrade
	pipenv install --dev
	alembic -c dpo/alembic.ini -x postgresql+psycopg2://postgres:travisci@localhost:5432/postgres upgrade head

# Run unit tests
test_unit:
	pipenv run pytest

# Run integration tests
test_integration:
	./tests/integration/test_integration.sh
