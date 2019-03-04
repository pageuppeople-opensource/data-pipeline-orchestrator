#!/bin/sh

# Exit on failure
set -e

# Bootstrap
## Aliases
loadModelDirectory="./tests/integration/models/load"
mcd="pipenv run python -m mcd postgresql+psycopg2://postgres:travisci@localhost:5432/postgres"

InitExecution () {
    executionId=$($mcd init-execution)
}

CompareAndAssert () {
    echo "Comparing load models"
    $($mcd persist-models $executionId load $loadModelDirectory "*.json")
    lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
    changedModels=$($mcd compare-models $lastSuccessfulExecutionId $executionId load)

    echo "Assert changed load models"
    if [ "$changedModels" != "$1" ]
    then
        echo "ERROR: expected "$1", actual "$changedModels""
        exit 1
    fi
}

CompleteAndAssert () {
    echo "Completing execution"
    $mcd complete-execution $executionId

    echo "Asserting last successful execution"
    lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
    if [ $lastSuccessfulExecutionId != $executionId ]
    then
        echo "ERROR: expected \"$executionId\", actual '$lastSuccessfulExecutionId'"
        exit 1
    fi
}

## Create stub load models
echo "Creating stub load models: load_model_1.json, load_model_2.json"
mkdir -p $loadModelDirectory
echo "load_model_1" > "$loadModelDirectory/load_model_1.json"
echo "load_model_2" > "$loadModelDirectory/load_model_2.json"

# Execution 1
echo "Beginning execution #1"
InitExecution
CompareAndAssert "load_model_1 load_model_2"
CompleteAndAssert

# Modify load_model_1
echo "Modifying load_model_1"
echo "" > "$loadModelDirectory/load_model_1.json"

# Execution 2
echo "Beginning execution #2"
InitExecution
CompareAndAssert "load_model_1"
CompleteAndAssert
