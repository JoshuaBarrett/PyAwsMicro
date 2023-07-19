@echo off

REM Creates template config if it does not already exist
set "CONFIG_FILE=config.py"
if not exist "%CONFIG_FILE%" (
    echo Creating config.py...
    (echo AWS_KEY = "XXXX") > "%CONFIG_FILE%"
    (echo AWS_SECRET = "XXXX") >> "%CONFIG_FILE%"
    (echo AWS_ACCOUNT_NUMBER = "XXXX") >> "%CONFIG_FILE%"
    (echo AWS_REGION = "XXXX") >> "%CONFIG_FILE%"
    (echo AWS_QUEUENAME  = "XXXX") >> "%CONFIG_FILE%"
    echo Config file has been created.
) else (
    echo config.py already exists. Skipping creation.
)

REM Checks to see if virtual environment already exists
if exist venv\ (
    echo Virtual environment already setup
    exit /b %errorlevel%
)

REM Creates virtural environment
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    exit /b %errorlevel%
)

REM Activates virtual environment in prep to instal packages
call venv/Scripts/activate
if %errorlevel% neq 0 (
    echo Failed to activate virtual environment.
    exit /b %errorlevel%
)

REM Installs packages referenced in requirements.txt
if defined VIRTUAL_ENV (
    pip install -r requirements.txt
    echo Virtual environment 'venv' has been successfully set up and packages have been installed
) else (
    echo You are not inside a virtual environment, packages NOT installed
)
