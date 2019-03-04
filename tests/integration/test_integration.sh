#!/bin/sh

# Exit on failure
set -e

# Bootstrap
## Aliases
modelDirectory="./tests/integration/models"
loadModelDirectory="$modelDirectory/load"
transformModelDirectory="$modelDirectory/transform"
mcd="pipenv run python -m mcd postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

InitExecution () {
    local executionId=$($mcd init-execution)

    if [ ${#executionId} -ne 36 ]
    then
        echo "ERROR: expected a non-empty guid-length execution identifier, actual "$executionId""
        exit 1
    fi

    # local  __resultvar=$1
    # if [[ "$__resultvar" ]]; then
    #     eval $__resultvar="'$executionId'"
    # else
    echo "$executionId"
    # fi
}

GetLastSuccessfulExecution () {
    local executionId=$($mcd get-last-successful-execution)

    if [ ${#executionId} != 36 ] && [ $executionId != 'NO_LAST_SUCCESSFUL_EXECUTION' ]
    then
        echo "ERROR: expected a non-empty guid-length execution identifier or known constant when no matching execution found, actual "$executionId""
        exit 1
    fi

    echo "$executionId"
}

GetExecutionLastUpdatedTimestamp () {
    local executionId=$1
    local executionLastUpdatedTimestamp=$($mcd get-execution-last-updated-timestamp $executionId)

    if ! [[ $executionLastUpdatedTimestamp =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}[\+,-][0-9]{2}:[0-9]{2}$ ]]
    then
        echo "ERROR: expected a non-empty ISO 8601 datetime with timezone, actual "$executionLastUpdatedTimestamp""
        exit 1
    fi

    echo "$executionLastUpdatedTimestamp"
}

PersistModels () {
    local executionId=$1
    local modelType=$2
    local basePath=$3
    $mcd persist-models $executionId $modelType $basePath "**/*.json" "**/*.csv" "**/*.sql"
}

CompareModels () {
    local previousExecutionId=$1
    local currentExecutionId=$2
    local modelType=$3

    local result=$($mcd compare-models $previousExecutionId $currentExecutionId $modelType)

    echo "$result"
}

CompleteExecution () {
    local executionId=$1
    $mcd complete-execution $executionId
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

## Setup
rm -rf $modelDirectory

## Create stub load models
echo "Creating stub LOAD models: load_model_1.json, load_model_2.json"
mkdir -p $loadModelDirectory
echo "load_model_1" > "$loadModelDirectory/load_model_1.json"
echo "load_model_2" > "$loadModelDirectory/load_model_2.json"

## Create stub transform models
echo "Creating stub TRANSFORM models: transform_model_1.csv, transform_model_2.sql, transform_model_3.sql"
mkdir -p $transformModelDirectory
echo "transform_model_1" > "$transformModelDirectory/transform_model_1.csv"
echo "transform_model_2" > "$transformModelDirectory/transform_model_2.sql"
echo "transform_model_3" > "$transformModelDirectory/transform_model_3.sql"

# Execution 1
echo "Beginning execution #1"

iter1_ExecId=$(InitExecution)
echo "iter1_ExecId = $iter1_ExecId"

iter1_lastSuccessfulExecId=$(GetLastSuccessfulExecution)
echo "iter1_lastSuccessfulExecId = $iter1_lastSuccessfulExecId"

iter1_lastSuccessfulExecCompletionTimestamp=$(GetExecutionLastUpdatedTimestamp $iter1_lastSuccessfulExecId)
echo "iter1_lastSuccessfulExecCompletionTimestamp = $iter1_lastSuccessfulExecCompletionTimestamp"
# GetExecutionLastUpdatedTimestamp $iter1_lastSuccessfulExecId

PersistModels $iter1_ExecId LOAD $loadModelDirectory
iter1_comparedLoadModels=$(CompareModels $iter1_lastSuccessfulExecId $iter1_ExecId LOAD)
echo "iter1_comparedLoadModels = '$iter1_comparedLoadModels'"

# Assert
iter1_compareLoadModels_expected="load_model_1 load_model_2"
if [ "$iter1_comparedLoadModels" != "$iter1_compareLoadModels_expected" ]
then
    echo "ERROR: expected '"$iter1_compareLoadModels_expected"', actual '"$iter1_comparedLoadModels"'"
    exit 1
fi

PersistModels $iter1_ExecId TRANSFORM $transformModelDirectory
iter1_comparedTransformModels=$(CompareModels $iter1_lastSuccessfulExecId $iter1_ExecId TRANSFORM)
echo "iter1_comparedTransformModels = '$iter1_comparedTransformModels'"

# Assert
iter1_compareTransformModels_expected="transform_model_1 transform_model_2 transform_model_3"
if [ "$iter1_comparedTransformModels" != "$iter1_compareTransformModels_expected" ]
then
    echo "ERROR: expected '"$iter1_compareTransformModels_expected"', actual '"$iter1_comparedTransformModels"'"
    exit 1
fi

CompleteExecution $iter1_ExecId

# Execution 2
echo "Beginning execution #2"

iter2_ExecId=$(InitExecution)
echo "iter2_ExecId = $iter2_ExecId"

iter2_lastSuccessfulExecId=$(GetLastSuccessfulExecution)
echo "iter2_lastSuccessfulExecId = $iter2_lastSuccessfulExecId"
if [ "$iter2_lastSuccessfulExecId" != "$iter1_ExecId" ]
then
    echo "ERROR: expected '"$iter1_ExecId"', actual '"$iter2_lastSuccessfulExecId"'"
    exit 1
fi

iter2_lastSuccessfulExecCompletionTimestamp=$(GetExecutionLastUpdatedTimestamp $iter1_ExecId)
echo "iter2_lastSuccessfulExecCompletionTimestamp = $iter2_lastSuccessfulExecCompletionTimestamp"

PersistModels $iter2_ExecId LOAD $loadModelDirectory
iter2_comparedLoadModels=$(CompareModels $iter1_ExecId $iter2_ExecId LOAD)
echo "iter2_comparedLoadModels = '$iter2_comparedLoadModels'"

# Assert
iter2_compareLoadModels_expected=""
if [ "$iter2_comparedLoadModels" != "$iter2_compareLoadModels_expected" ]
then
    echo "ERROR: expected '"$iter2_compareLoadModels_expected"', actual '"$iter2_comparedLoadModels"'"
    exit 1
fi


echo "Modifying transform_model_2"
echo "Modified transform_model_2" > "$transformModelDirectory/transform_model_2.sql"
echo "Deleting transform_model_3"
rm -f "$transformModelDirectory/transform_model_3.sql"
echo "Adding transform_model_2"
echo "transform_model_4" > "$transformModelDirectory/transform_model_4.sql"

PersistModels $iter2_ExecId TRANSFORM $transformModelDirectory
iter2_comparedTransformModels=$(CompareModels $iter1_ExecId $iter2_ExecId TRANSFORM)
echo "iter2_comparedTransformModels = '$iter2_comparedTransformModels'"

# Assert
iter2_compareTransformModels_expected="transform_model_2 transform_model_4"
if [ "$iter2_comparedTransformModels" != "$iter2_compareTransformModels_expected" ]
then
    echo "ERROR: expected '"$iter2_compareTransformModels_expected"', actual '"$iter2_comparedTransformModels"'"
    exit 1
fi

CompleteExecution $iter2_ExecId


# CompareAndAssert "load_model_1 load_model_2"
# CompleteAndAssert

# Modify load_model_1
# echo "Modifying load_model_1"
# echo "" > "$loadModelDirectory/load_model_1.json"

# Execution 2
# echo "Beginning execution #2"
# InitExecution
# CompareAndAssert "load_model_1"
# CompleteAndAssert
