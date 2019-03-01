# Model Change Detector

[![Build Status](https://travis-ci.com/PageUpPeopleOrg/model-change-detector.svg?branch=master)](https://travis-ci.com/PageUpPeopleOrg/model-change-detector)

A utility that persists state of a data pipeline execution and uses them to detect changes in models.

## Usage

```
$ python mcd.py [options] {db-connection-string} <command> [command-parameters]
```

- `options` include:
  - `--help | -h`: displays help menu.
  - `--log-level | -l`: choose program's logging level, from CRITICAL, ERROR, WARNING, INFO, DEBUG; default is INFO.
- `db-connection-string`: a [PostgreSQL Db Connection String](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2) of the format `postgresql+psycopg2://user:password@host:port/dbname`
- `command` is the function to be performed by the utility. The currently supported values are:
  - `init-execution`: Marks the start of a new execution by creating a record for the same in the given database. Returns an `execution-id` which is a GUID identifier of the new execution.
  - `get-last-successful-execution`: Finds the last successful data pipeline execution. Returns an `execution-id` which is a GUID identifier of the new execution, if found; else returns and empty string.
  - `get-execution-last-updated-timestamp`: Returns the `last-updated-on` timestamp with timezone of the given `execution-id`. Raises error if given `execution-id` is invalid.
    - `execution-id`: a GUID identifier of an existing data pipeline execution.
  - `persist-models`: Saves models of the given `model-type` within the given `execution-id` by persisting hashed checksums of the given models.
    - `execution-id`: identifier of an existing data pipeline execution, ideally as returned by the `init` command.
    - `model-type`: type of models being processed, choose from `LOAD`, `TRANSFORM`.
    - `base-path`: absolute or relative path to the models e.g.: `./load`, `/home/local/transform`, `C:/path/to/models`
    - `model-patterns`: one or more unix-style search patterns _(relative to `base-path`)_ for model files. models within a model-type must be named uniquely regardless of their file extension. e.g.: `*.txt`, `**/*.txt`, `./relative/path/to/some_models/**/*.csv`, `relative/path/to/some/more/related/models/**/*.sql`
  - `compare-models`: Compares the hashed checksums of models between two executions. Returns comma-separated string of changed model names.
    - `previous-execution-id`: identifier of an existing data pipeline execution, ideally as returned by the `get-last-successful-execution` command.
    - `current-execution-id`: identifier of an existing data pipeline execution, ideally as returned by the `init` command.
    - `model-type`: type of models being processed, choose from `LOAD`, `TRANSFORM`.
  - `complete-execution`: Marks the completion of an existing execution by updating a record for the same in the given database. Returns nothing unless there's an error.
    - `execution-id`: a GUID identifier of an existing data pipeline execution as returned by the `init` command.

To get help, use:

```
$ python mcd.py --help
$ python mcd.py <command> --help
```

### Usage Example

```
$ pipenv install
$ pipenv shell

$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname init-execution

$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname get-last-successful-execution
$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname get-execution-last-updated-timestamp id-as-returned-by-get-last-successful-execution-command

$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname persist-models id-as-retured-by-init-command load ./relative/path/to/load/models **/*.json
$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname compare-models id-as-retured-by-get-last-successful-execution-command id-as-retured-by-init-command load

$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname persist-models id-as-retured-by-init-command transform C:/absolute/path/to/transform/models group1/*.csv ./group2/**/*.sql
$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname compare-models id-as-retured-by-get-last-successful-execution-command id-as-retured-by-init-command transform

$ python mcd.py postgresql+psycopg2://user:password@host:port/dbname complete-execution id-as-retured-by-init-command
```

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv) (recommended but not required)

### Verify Installation

Verify dependencies are installed by running the following commands:

```
$ python --version
$ pipenv --version
```

## Getting Started

There are two approaches to getting started with using MCD:

- Pipenv
- Pip

Pipenv is the recommended approach, however, you can still use `pip` to install dependencies.

### Pipenv (recommended)

#### Install dependencies

To install project dependencies, run the following command:

```
$ pipenv install
```

#### Activate Virtual Environment

To activate a virtual environment, run the following command:

```
$ pipenv shell
```

### Pip (traditional)

#### Activate Virtual Environment

To create and activate a virtual environment, please refer to the following [guide](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

#### Install dependencies

To install project dependencies, run the following command:

```
$ pip install -r requirements.txt
```

### Using MCD

Once the virtual environment has been activated, please refer to [usage](#Usage) for how to use MCD.

## Testing

To run integration tests locally, it is highly recommended that [Docker](https://www.docker.com/) is installed.

### Unit Tests

To run unit tests, run the following command:

```
$ python pytest
```

### Integration Tests

To run integration tests, please ensure the following information is configured correctly:

- `tests/integration/test_integration.sh:9`

Please ensure that the database connection string points to a valid PostgreSQL instance.

#### Docker

If Docker is installed, running tests is as simple as running the following commands:

```
$ docker pull postgres
$ docker run --name stubdatabase -p 5432:5432 -e POSTGRES_PASSWORD=travisci -d postgres
$ make test_integration
$ docker stop stubdatabase
$ docker remove stubdatabase
```

#### Local PostgreSQL

If a local instance of PostgreSQL is installed, run integration tests with the following command:

```
$ make test_integration
```

#### Notes

If you do not have `make` installed, you can substitute `make` with:

```
$ ./tests/integration/test_integration.sh
```
