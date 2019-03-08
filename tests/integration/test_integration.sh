#!/bin/bash

# Exit on failure
set -e

# Bootstrap
mcd="pipenv run python -m mcd postgresql+psycopg2://postgres:password@localhost:5432/postgres"
modelDirectory="./tests/integration/models"
loadModelDirectory="$modelDirectory/load"
transformModelDirectory="$modelDirectory/transform"

# Generate a pseudo UUID
# https://gist.github.com/markusfisch/6110640
NewUUID () {
    local N B C='89ab'

    for (( N=0; N < 16; ++N ))
    do
        B=$(( $RANDOM%256 ))

        case $N in
            6)
                printf '4%x' $(( B%16 ))
                ;;
            8)
                printf '%c%x' ${C:$RANDOM%${#C}:1} $(( B%16 ))
                ;;
            3 | 5 | 7 | 9)
                printf '%02x-' $B
                ;;
            *)
                printf '%02x' $B
                ;;
        esac
    done

    echo
}

LogErrorAndExit () {
    local errorText=$1
    local errorCode=1

    >&2 echo ${errorText}
    exit $errorCode
}

AssertAreEqual () {
    local subject=$1
    local actual=$2
    local expected=$3
    if [ "$actual" == "$expected" ]
    then
        echo "PASS: "$subject" as expected"
    else
        LogErrorAndExit "ERROR: "$subject" was expected to be "$expected", actual was "$actual""
    fi
}

InitExecution () {
    local executionId=$($mcd init-execution)

    if [ ${#executionId} -ne 36 ]
    then
        LogErrorAndExit "ERROR: expected a non-empty guid-length execution identifier, actual "$executionId""
    fi

    echo "$executionId"
}

GetLastSuccessfulExecution () {
    local executionId=$($mcd get-last-successful-execution)

    if [ ${#executionId} != 36 ] && [ $executionId != 'NO_LAST_SUCCESSFUL_EXECUTION' ]
    then
        LogErrorAndExit "ERROR: expected a non-empty guid-length execution identifier or known constant when no matching execution found, actual "$executionId""
    fi

    echo "$executionId"
}

GetExecutionLastUpdatedTimestamp () {
    local executionId=$1
    local executionLastUpdatedTimestamp=$($mcd get-execution-last-updated-timestamp $executionId)

    if ! [[ $executionLastUpdatedTimestamp =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}[\+,-][0-9]{2}:[0-9]{2}$ ]]
    then
        LogErrorAndExit "ERROR: expected a non-empty ISO 8601 datetime with timezone, actual "$executionLastUpdatedTimestamp""
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

    local lastSuccessfulExecId=$(GetLastSuccessfulExecution)
    AssertAreEqual "ExecutionID $executionId completed successfully; next LastSuccessfulExecutionID" "$lastSuccessfulExecId" "$executionId"
}

ExecuteAndAssert () {
    # Arrange
    local iter_no=$1
    local expected_lastSuccessfulExecId=$2
    local expected_changedLoadModels=$3
    local expected_changedTransformModels=$4
    local __resultvar=$5

    # Act
    local execId=$(InitExecution)
    echo "  iter$iter_no execId                                = $execId"

    local lastSuccessfulExecId=$(GetLastSuccessfulExecution)
    echo "  iter$iter_no lastSuccessfulExecId                  = $lastSuccessfulExecId"

    local lastSuccessfulExecCompletionTimestamp=$(GetExecutionLastUpdatedTimestamp $lastSuccessfulExecId)
    echo "  iter$iter_no lastSuccessfulExecCompletionTimestamp = $lastSuccessfulExecCompletionTimestamp"

    PersistModels $execId LOAD $loadModelDirectory
    local changedLoadModels=$(CompareModels $lastSuccessfulExecId $execId LOAD)
    echo "  iter$iter_no changedLoadModels                     = '$changedLoadModels'"

    PersistModels $execId TRANSFORM $transformModelDirectory
    local changedTransformModels=$(CompareModels $lastSuccessfulExecId $execId TRANSFORM)
    echo "  iter$iter_no changedTransformModels                = '$changedTransformModels'"

    CompleteExecution $execId

    # Assert
    if [ ! -z "$expected_lastSuccessfulExecId" ]
    then
        AssertAreEqual "Iteration $iter_no's LastSuccessfulExecutionID" "$lastSuccessfulExecId" "$expected_lastSuccessfulExecId"
    fi
    AssertAreEqual "Iteration $iter_no's ChangedLoadModels" "$changedLoadModels" "$expected_changedLoadModels"
    AssertAreEqual "Iteration $iter_no's ChangedTransformModels" "$changedTransformModels" "$expected_changedTransformModels"

    if [[ "$__resultvar" ]]; then
        eval $__resultvar="'$execId'"
    fi
}

load_model_1="load_model_1_$(NewUUID)"
load_model_2="load_model_2_$(NewUUID)"
transform_model_1="transform_model_1_$(NewUUID)"
transform_model_2="transform_model_2_$(NewUUID)"
transform_model_3="transform_model_3_$(NewUUID)"
transform_model_4="transform_model_4_$(NewUUID)"

###############
# Execution 1 #
###############
echo -e "\nBeginning execution #1"

# ARRANGE
## Remove test models' directory, if exists
rm -rf $modelDirectory

## Create stub load models
echo " Creating stub LOAD models: load_model_1, load_model_2"
mkdir -p $loadModelDirectory
echo "load_model_1" > "$loadModelDirectory/$load_model_1.json"
echo "load_model_2" > "$loadModelDirectory/$load_model_2.json"

## Create stub transform models
echo " Creating stub TRANSFORM models: transform_model_1, transform_model_2, transform_model_3"
mkdir -p $transformModelDirectory
echo "transform_model_1" > "$transformModelDirectory/$transform_model_1.csv"
echo "transform_model_2" > "$transformModelDirectory/$transform_model_2.sql"
echo "transform_model_3" > "$transformModelDirectory/$transform_model_3.sql"

# ACT & ASSERT
iter1_expected_lastSuccessfulExecId="" # pass in empty string to skip test since we don't know the past state of the pipeline
iter1_expected_changedLoadModels="$load_model_1 $load_model_2"
iter1_expected_changedTransformModels="$transform_model_1 $transform_model_2 $transform_model_3"
ExecuteAndAssert "1" "$iter1_expected_lastSuccessfulExecId" "$iter1_expected_changedLoadModels" "$iter1_expected_changedTransformModels" iter1_execId

###############
# Execution 2 #
###############
echo -e "\nBeginning execution #2"

# ARRANGE
echo " Making no changes to any LOAD models"

echo " Modifying transform_model_2"
echo "Modified transform_model_2" > "$transformModelDirectory/$transform_model_2.sql"

echo " Deleting transform_model_3"
rm -f "$transformModelDirectory/$transform_model_3.sql"

echo " Adding transform_model_4"
echo "transform_model_4" > "$transformModelDirectory/$transform_model_4.sql"

# ACT & ASSERT
iter2_expected_lastSuccessfulExecId="$iter1_execId"
iter2_expected_changedLoadModels=""
iter2_expected_changedTransformModels="$transform_model_2 $transform_model_4"
ExecuteAndAssert "2" "$iter2_expected_lastSuccessfulExecId" "$iter2_expected_changedLoadModels" "$iter2_expected_changedTransformModels" iter2_execId
