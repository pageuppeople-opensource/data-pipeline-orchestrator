# Install dependencies
install_deps:
	pip install pipenv --upgrade
	pipenv install --dev
	alembic -c dpo/alembic.ini -x postgresql+psycopg2://integration_test_user:integration_test_password@localhost:5432/integration_test_db upgrade head

# Run unit tests
test_unit:
	pipenv run pytest

# Run integration tests
test_integration:
	./tests/integration/test_integration.sh

test_downgrade_schema:
	alembic -c dpo/alembic.ini -x postgresql+psycopg2://integration_test_user:integration_test_password@localhost:5432/integration_test_db downgrade base
