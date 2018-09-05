# Model Change Detector

## About

_TODO_

## Usage

_TODO_

```commandline
py mcd.py --help
py mcd.py --version
py mcd.py NEW --log-level ERROR --verbose
py mcd.py NEW -l ERROR -V
```

## Setup

### Pre-requisites

#### Python 3

Install from [here](https://www.python.org/) _(or your choice of safe software provider)_. During installation, choose the option to _Add to PATH_ and _Custom Installation_ so you can provide the install path to not be the default `C:\Program Files\Python37\` and be outside the `Program Files` directory to say, `C:\Python37\`. This is just a suggestion since there have been issues with updating key python packages once Python is installed within `Program Files` on Windows.

Verify your installation by running the below commands.

```powershell
py --version
python --version
pip --version
```

If you end up with multiple accidental/purposeful python installations, use the below in Windows Command Prompt to figure out where the executables are located.

```cmd
where py
where python
where pip
```

#### Virtualenv

Install `virtualenv`, which is a tool to create isolated Python environments.
```bash
pip install virtualenv
```
###Post-pre-requisites? / the real setup

#### Create a local virtual python environment for this projects development

`virtualenv <environment-name>` _e.g._ `virtualenv .env`
Or `py -m virtualenv <environment-name>` _e.g._ `py -m virtualenv .env`

If you build with `virtualenv --system-site-packages .env`, your virtual environment will inherit packages from your global site-packages directory. Although, if you want isolation from the global system, do not use this flag.

#### Activate the virtual environment

On Windows:

`path/to/environment/scripts/activate` _e.g._ `.env/scripts/activate`

On Linux / Mac OS

 `source path/to/environment/bin/activate`_e.g._ `source .env/bin/activate`

You should see the name of your virtual environment in brackets on your terminal line e.g. `(.env) C:\path\to\working\dir\`. Any python commands you use will now work with your virtual environment

#### Deactivate the virtual environment

```powershell
decativate
```
