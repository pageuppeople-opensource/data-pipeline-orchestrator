# Data Pipeline Orchestrator

[![Build Status](https://travis-ci.com/PageUpPeopleOrg/data-pipeline-orchestrator.svg?branch=master)](https://travis-ci.com/PageUpPeopleOrg/data-pipeline-orchestrator)

A utility that persists state of a data pipeline execution and uses them to detect changes in models.

## Usage

```
$ python -m dpo [options] <db-connection-string> <command> [command-args]
```

- `options` include:
  - `--help | -h`: displays help menu.
  - `--log-level | -l`: choose program's logging level, from CRITICAL, ERROR, WARNING, INFO, DEBUG; default is INFO.
- `db-connection-string`: a [PostgreSQL Db Connection String](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2) of the format `postgresql+psycopg2://user:password@host:port/dbname`
- `command` is the function to be performed by the utility. The currently supported values are:
  - `init-execution`: Marks the start of a new execution. Returns an `execution-id` which is a GUID identifier of the new execution.
  - `get-last-successful-execution`: Finds the last successful execution. Returns an `execution-id` which is a GUID identifier of the new execution, if found; else returns and empty string.
  - `get-execution-completion-timestamp`: Returns the `last-updated-on` timestamp with timezone of the given `execution-id`. Raises error if given `execution-id` is invalid.
    - `execution-id`: a GUID identifier of an existing execution.
  - `init-step`: Saves models of the given `model-type` within the given `execution-id` by persisting hashed checksums of the given models.
    - `execution-id`: identifier of an existing data pipeline execution, ideally as returned by the `init` command.
    - `step-name`: name of step being processed, choose from `LOAD`, `TRANSFORM`.
    - `base-path`: absolute or relative path to the models e.g.: `./load`, `/home/local/transform`, `C:/path/to/models`
    - `model-patterns`: one or more unix-style search patterns _(relative to `base-path`)_ for model files. models within a model-type must be named uniquely regardless of their file extension. e.g.: `*.txt`, `**/*.txt`, `./relative/path/to/some_models/**/*.csv`, `relative/path/to/some/more/related/models/**/*.sql`
  - `compare-step-models`: Compares the hashed checksums of models between two executions' steps. Returns comma-separated string of changed model names.
    - `step-id`: identifier of an existing execution's step, as returned by the `init-step` command.
    - `previous-execution-id`: identifier of an existing execution, ideally as returned by the `get-last-successful-execution` command.
  - `complete-step`: Marks the completion of an existing execution's step. Returns nothing unless there's an error.
    - `step-id`: a GUID identifier of an existing execution's step as returned by the `init-step` command.
    - `rows-processed`: an optional numeric value to indicate the number of rows processed during this step. supports a postgresql BIGINT type value.
  - `complete-execution`: Marks the completion of an existing execution. Returns nothing unless there's an error.
    - `execution-id`: a GUID identifier of an existing execution as returned by the `init-execution` command.

To get help, use:

```
$ python -m dpo --help
$ python -m dpo <command> --help
```

### Usage Example

```
$ pipenv install
$ pipenv shell

$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname init-execution

$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname get-last-successful-execution
$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname get-execution-last-updated-timestamp id-as-returned-by-get-last-successful-execution-command

$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname persist-models id-as-retured-by-init-command load ./relative/path/to/load/models **/*.json
$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname compare-models id-as-retured-by-get-last-successful-execution-command id-as-retured-by-init-command load

$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname persist-models id-as-retured-by-init-command transform C:/absolute/path/to/transform/models group1/*.csv ./group2/**/*.sql
$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname compare-models id-as-retured-by-get-last-successful-execution-command id-as-retured-by-init-command transform

$ python -m dpo postgresql+psycopg2://user:password@host:port/dbname complete-execution id-as-retured-by-init-command
```

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)

### Verify Installation

Verify dependencies are installed by running the following commands:

```
$ python --version
$ pipenv --version
```

## Getting Started

### Install dependencies

To install project dependencies, run the following command:

```
$ pipenv install
```

### Activate Virtual Environment

To activate a virtual environment, run the following command:

```
$ pipenv shell
```

### Using DPO

Once the virtual environment has been activated, please refer to [usage](#Usage) for how to use DPO.

## Testing

### Unit Tests

To run unit tests, run the following command:

```
$ pytest
```

### Integration Tests

- Install PostgreSQL 9.6+
- Execute below scripts to setup test db and user
  ```
  ./tests/integration/setup-part1.sql
  ./tests/integration/setup-part2.sql
  alembic -c dpo/alembic.ini -x postgresql+psycopg2://integration_test_user:integration_test_password@localhost:5432/integration_test_db upgrade head
  ```
- To run integration tests, run either of the following commands:
  ```
  $ make test_integration
  $ ./tests/integration/test_integration.sh
  ```

#### Notes

If you do not have `make` installed, you can substitute `make` with:

```
$ ./tests/integration/test_integration.sh
```

## Alembic

### To upgrade to the latest schema

```bash
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL upgrade head
```

### Updating the schema

Ensure any new tables inherit from the same Base used in `alembic/env.py`

```python
from dpo.Shared import BaseEntity
```

Whenever you make a schema change, run

```bash
pipenv install .
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL revision -m "$REVISION_MESSAGE" --autogenerate
```

check that the new version in `alembic/versions` is correct

### Downgrading the schema

Whenever you want to downgrade the schema

```bash
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL history # see the list of revision ids
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL current # see the current revision id
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL downgrade -1 # revert back one revision
alembic -c dpo/alembic.ini -x $DESTINATION_DB_URL downgrade $revision_id # revert back to a revision id, found using the history command
```

### Inaccurate autogenerated revisions

Does your autogenerated revision not look right?

Try editing the function `use_schema` in `alembic/env.py`, this determines what alembic looks for in the database.

[Relevant Documentation](https://alembic.sqlalchemy.org/en/latest/api/runtime.html?highlight=include_schemas#alembic.runtime.environment.EnvironmentContext.configure.params.include_object)

### New models aren't showing up in upgrade section

Ensure all model classes inherit from the same Base that `alembic/env.py` imports, and that the following class
properties are set

```python
__tablename__ = 'your_mapped_table_name'
__table_args__ = {'schema': Constants.DATA_PIPELINE_EXECUTION_SCHEMA_NAME}
```

Also try importing the models into `alembic/env.py`, eg

```python
from dpo.entities import ModelChecksumEntity
from dpo.entities import DataPipelineExecutionEntity
```

### Alembic won't pick up my change

[Alembic only supports some changes](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)

Try adding raw sql in the `upgrade()` and `downgrade()` functions of your revision

```python
op.execute(RAW_SQL)
```