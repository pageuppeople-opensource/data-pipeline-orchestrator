#!/bin/sh

# Exit on failure
set -e

# Bootstrap
## Aliases
loadModels='./tests/integration/models/load'
mcd='pipenv run python mcd.py postgresql+psycopg2://postgres:travisci@localhost:5432/postgres'

InitExecution () {
    executionId=$($mcd init)
}

CompareAndAssert () {
    echo 'Comparing load models'
    changedModels=$($mcd compare $executionId load $loadModels *.json)

    echo 'Assert changed load models'
    if [ $changedModels != "$1" ]
    then
        echo 'ERROR: expected '$1', actual '$changedModels''
        exit 1
    fi
}

CompleteAndAssert () {
    echo 'Completing execution'
    $mcd complete $executionId

    echo 'Asserting last successful execution'
    lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
    if [ $lastSuccessfulExecutionId != $executionId ]
    then
        echo 'ERROR: expected '$executionId', actual '$lastSuccessfulExecutionId''
        exit 1
    fi
}

## Create stub load models
echo 'Creating stub load models'
mkdir -p $loadModels
echo 'load_model_1' > "$loadModels/load_model_1.json"
echo 'load_model_2' > "$loadModels/load_model_2.json"

# Execution 1
echo 'Beginning execution #1'
InitExecution
CompareAndAssert 'testfailure'
CompleteAndAssert

# Execution 2
echo 'Beginning execution #2'
InitExecution
echo 'Modifying load_model_1'
echo '' > "$loadModels/load_model_1.json"
CompareAndAssert 'load_model_1'
CompleteAndAssert

# debug
rm -rf $loadModels