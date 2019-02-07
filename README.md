# Model Change Detector

## About

A utility that persists state of a data pipeline execution and uses them to detect changes in models.

## Usage

```commandline
py mcd.py [options] <command> [command-parameters]
```

- `options` include:
  - `--help | -h`: displays help menu.
  - `--log-level | -l`: choose program's logging level, from CRITICAL, ERROR, WARNING, INFO, DEBUG; default is INFO.
- `db-connection-string`: a [PostgreSQL Db Connection String](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2) of the format `postgresql+psycopg2://user:password@host:port/dbname`
- `command` is the function to be performed by the utility. The currently supported values are:
  - `init`: Marks the start of a new execution by creating a record for the same in the given database. Returns an `execution-id` which is a GUID identifier of the new execution.
  - `compare`: Compares & persists SHA256-hashed checksums of the given models against those of the last successful execution. Returns comma-separated string of changed model names.
    - `execution-id`: a GUID identifier of an existing data pipeline execution as returned by the `init` command.
    - `model-type`: type of models being processed e.g.: `load`, `transform`, etc. this `model-type` is used to group the model checksums by and used to find and compare older ones.
    - `base-path`: absolute or relative path to the models e.g.: `./load`, `/home/local/load`, `C:/path/to/load`
    - `model-patterns`: path-based patterns _(relative to `base-path`)_ to different models with extensions. models within a model-type must be named uniquely regardless of their file extension. e.g.: `*.txt`, `**/*.txt`, `./relative/path/to/some_models/**/*.csv`, `relative/path/to/some/more/related/models/**/*.sql`
  - `complete`: Marks the completion of an existing execution by updating a record for the same in the given database. Returns nothing unless there's an error.
    - `execution-id`: a GUID identifier of an existing data pipeline execution as returned by the `init` command.

To get help,use:

```commandline
py mcd.py --help
py mcd.py <command> --help
```

### As a script

- Use a local isolated/virtual python environment for this project
- Install project dependencies
- `py mcd.py [options] <command> [command-parameters]`

_Windows example:_

```commandline
py -m venv new-env --clear
new-env\scripts\activate

py -m pip install -r requirements.txt

py mcd.py postgresql+psycopg2://user:password@host:port/dbname init
py mcd.py postgresql+psycopg2://user:password@host:port/dbname compare execution-id-as-retured-by-init-command load ./relative/path/to/load/models **/*.json
py mcd.py postgresql+psycopg2://user:password@host:port/dbname compare execution-id-as-retured-by-init-command transform C:/absolute/path/to/transform/models group1/*.csv ./group2/**/*.sql
py mcd.py postgresql+psycopg2://user:password@host:port/dbname complete execution-id-as-retured-by-init-command
```

### As a package

- Use/create an empty directory
- Use a local isolated/virtual python environment for this project
- [Install](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) this package
  - `pip install -e path/to/ProjectX`
  - `pip install -e git+git://github.com/ProjectX.git#egg=ProjectX`
- `py -m mcd [options] <command> <command-options>`

_Windows example:_

```commandline
mkdir new-dir
cd new-dir

py -m venv new-env --clear
new-env\scripts\activate

pip install -e git+git://github.com/PageUpPeopleOrg/model-change-detector.git#egg=mcd

py -m mcd postgresql+psycopg2://user:password@host:port/dbname init
py -m mcd postgresql+psycopg2://user:password@host:port/dbname compare execution-id-as-retured-by-init-command load ./relative/path/to/load/models **/*.json
py -m mcd postgresql+psycopg2://user:password@host:port/dbname compare execution-id-as-retured-by-init-command transform C:/absolute/path/to/transform/models group1/*.csv ./group2/**/*.sql
py -m mcd postgresql+psycopg2://user:password@host:port/dbname complete execution-id-as-retured-by-init-command
```

## Setup

1. Install pre-requisites
2. Use a local isolated/virtual python environment for this project
3. Install project dependencies
4. Develop and test code changes
5. Once done, deactivate the virtual environment

### Install pre-requisites

#### Python 3

Install from [here](https://www.python.org/) _(or your choice of safe software provider)_. During installation, choose the option to _Add to PATH_ and _Custom Installation_ so you can provide the install path to not be the default `C:\Program Files\Python37\` and be outside the `Program Files` directory to say, `C:\Python37\`. This is just a suggestion since there have been issues with updating key python packages once Python is installed within `Program Files` on Windows.

Verify your installation by running the below commands.

```powershell
py --version
python --version
pip --version
```

If you end up with multiple accidental/purposeful python installations, use the below in Windows Commandline to figure out where the executables are located.

```cmd
where py
where python
where pip
```

### Use a local isolated/virtual python environment for this project

`py -m venv /path/to/new/virtual/environment` _e.g._ `py -m venv new-env`

If you build with `--system-site-packages` directory, your virtual environment will be allowed access to packages from your global site-packages directory. Although, if you want isolation from the global system, do not use this flag. Once you've created a new environment, you need to activate the same.

On Windows:

`path\to\environment\scripts\activate` _e.g._ `new-env\scripts\activate`

On Linux / Mac OS

`source path/to/environment/bin/activate` _e.g._ `source new-env/bin/activate`

You should see the name of your virtual environment in brackets on your terminal line, e.g.:

```commandline
C:\path\to\working\dir: new-env\scripts\activate
(new-env) C:\path\to\working\dir: _
```

Any python commands you use will now, work within your virtual environment only.

### Install project dependencies

```powershell
pip install -r requirements.txt
```

### Deactivate the virtual environment

Once done, deactivate the virtual environment with a simple `decativate` command, e.g.:

```commandline
(new-env) C:\path\to\working\dir: deactivate
C:\path\to\working\dir: _
```
