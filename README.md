# Model Change Detector

## About

A utility that detects changes in models.  

## Usage

```commandline
py mcd.py <command> <db-connection-string> [--help] [--version] [--log-level]
```

- `command` is the function to be performed by the utility. The currently supported values are 
  - `NEW`: Marks the start of a new execution by creating a record for the same in the given database and returns an ID of the new execution.
- `db-connection-string` is a [PostgreSQL Db Connection String](http://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2) of the format `postgresql+psycopg2://user:password@host:port/dbname`

### As a script

- Use a local isolated/virtual python environment for this project
- Install project dependencies
- `py mcd.py <command> <db-connection-string> [--help] [--version] [--log-level]`

_Windows example:_

```commandline
py -m venv new-env --clear
new-env\scripts\activate

py -m pip install -r requirements.txt

py mcd.py NEW postgresql+psycopg2://user:password@host:port/dbname
```

### As a package

- Use/create an empty directory
- Use a local isolated/virtual python environment for this project
- [Install](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) this package
- `py -m mcd <command> <db-connection-string> [--help] [--version] [--log-level]`

_Windows example:_

```commandline
mkdir new-dir
cd new-dir

py -m venv new-env --clear
new-env\scripts\activate

pip install -e path\to\model-change-detector

py -m mcd NEW postgresql+psycopg2://user:password@host:port/dbname
```

#### _Work in Progress_

|command|arguments|returns|
|-|-|-|
|`NEW`/`START`|`db-conn-str`|`execution-id`|
|`GET_LAST_SUCCESSFULL_EXEC_ID`|`db-conn-str`|`execution-id`|
|`AUDIT`|`db-conn-str`, `last-execution-id`, `path/to/models/`|-|
|`COMPLETE`/`FINISH`|`db-conn-str`, `execution-id`|-|

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
```
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
