#!/bin/sh

# Exit on failure
set -e

# Bootstrap
mcd="pipenv run python -m mcd postgresql+psycopg2://postgres:password@localhost:5432/postgres"

# Generate a pseudo UUID
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
    local actual=$1
    local expected=$2
    if [ "$actual" != "$expected" ]
    then
        LogErrorAndExit "ERROR: expected "$expected", actual "$actual""
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

    lastSuccessfulExecId=$(GetLastSuccessfulExecution)
    AssertAreEqual "$lastSuccessfulExecId" "$executionId"
}

modelDirectory="./tests/integration/models"
loadModelDirectory="$modelDirectory/load"
transformModelDirectory="$modelDirectory/transform"
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
echo "Creating stub LOAD models: load_model_1, load_model_2"
mkdir -p $loadModelDirectory
echo "load_model_1" > "$loadModelDirectory/$load_model_1.json"
echo "load_model_2" > "$loadModelDirectory/$load_model_2.json"

## Create stub transform models
echo "Creating stub TRANSFORM models: transform_model_1, transform_model_2, transform_model_3"
mkdir -p $transformModelDirectory
echo "transform_model_1" > "$transformModelDirectory/$transform_model_1.csv"
echo "transform_model_2" > "$transformModelDirectory/$transform_model_2.sql"
echo "transform_model_3" > "$transformModelDirectory/$transform_model_3.sql"

# ACT & ASSERT
iter1_execId=$(InitExecution)
echo " iter1_execId                                = $iter1_execId"

iter1_lastSuccessfulExecId=$(GetLastSuccessfulExecution)
echo " iter1_lastSuccessfulExecId                  = $iter1_lastSuccessfulExecId"

iter1_lastSuccessfulExecCompletionTimestamp=$(GetExecutionLastUpdatedTimestamp $iter1_lastSuccessfulExecId)
echo " iter1_lastSuccessfulExecCompletionTimestamp = $iter1_lastSuccessfulExecCompletionTimestamp"

PersistModels $iter1_execId LOAD $loadModelDirectory
iter1_changedLoadModels=$(CompareModels $iter1_lastSuccessfulExecId $iter1_execId LOAD)
echo " iter1_changedLoadModels                     = '$iter1_changedLoadModels'"

iter1_changedLoadModels_expected="$load_model_1 $load_model_2"
AssertAreEqual "$iter1_changedLoadModels" "$iter1_changedLoadModels_expected"

PersistModels $iter1_execId TRANSFORM $transformModelDirectory
iter1_changedTransformModels=$(CompareModels $iter1_lastSuccessfulExecId $iter1_execId TRANSFORM)
echo " iter1_changedTransformModels                = '$iter1_changedTransformModels'"

iter1_changedTransformModels_expected="$transform_model_1 $transform_model_2 $transform_model_3"
AssertAreEqual "$iter1_changedTransformModels" "$iter1_changedTransformModels_expected"

CompleteExecution $iter1_execId

###############
# Execution 2 #
###############
echo -e "\nBeginning execution #2"

# ARRANGE
echo "Making no changes to any LOAD models"

echo "Modifying transform_model_2"
echo "Modified transform_model_2" > "$transformModelDirectory/$transform_model_2.sql"

echo "Deleting transform_model_3"
rm -f "$transformModelDirectory/$transform_model_3.sql"

echo "Adding transform_model_4"
echo "transform_model_4" > "$transformModelDirectory/$transform_model_4.sql"

# ACT & ASSERT
iter2_execId=$(InitExecution)
echo " iter2_execId                                = $iter2_execId"

iter2_lastSuccessfulExecId=$(GetLastSuccessfulExecution)
echo " iter2_lastSuccessfulExecId                  = $iter2_lastSuccessfulExecId"
AssertAreEqual "$iter2_lastSuccessfulExecId" "$iter1_execId"

iter2_lastSuccessfulExecCompletionTimestamp=$(GetExecutionLastUpdatedTimestamp $iter2_lastSuccessfulExecId)
echo " iter2_lastSuccessfulExecCompletionTimestamp = $iter2_lastSuccessfulExecCompletionTimestamp"

PersistModels $iter2_execId LOAD $loadModelDirectory
iter2_changedLoadModels=$(CompareModels $iter2_lastSuccessfulExecId $iter2_execId LOAD)
echo " iter2_changedLoadModels                     = '$iter2_changedLoadModels'"

iter2_compareLoadModels_expected=""
AssertAreEqual "$iter2_changedLoadModels" "$iter2_compareLoadModels_expected"

PersistModels $iter2_execId TRANSFORM $transformModelDirectory
iter2_changedTransformModels=$(CompareModels $iter2_lastSuccessfulExecId $iter2_execId TRANSFORM)
echo " iter2_changedTransformModels                = '$iter2_changedTransformModels'"

iter2_compareTransformModels_expected="$transform_model_2 $transform_model_4"
AssertAreEqual "$iter2_changedTransformModels" "$iter2_compareTransformModels_expected"

CompleteExecution $iter2_execId
