# Exit on failure
set -e

# Bootstrap
## Aliases
loadModels='./tests/integration/models/load'
mcd='pipenv run python mcd.py postgresql+psycopg2://postgres:travisci@localhost:5432/postgres'

## Create stub load models
echo 'Creating stub load models'
mkdir -p $loadModels
echo 'load_model_1' > "$loadModels/load_model_1.json"
echo 'load_model_2' > "$loadModels/load_model_2.json"

# Begin new execution
echo 'Beginning new execution #1'
executionId=$($mcd init)

# Compare load models
echo 'Comparing load models for execution #1'
changedModels=$($mcd compare $executionId load $loadModels *.json)
if [ $changedModels != '*' ]
then
    exit 1
fi

# Complete execution
echo 'Completing execution #1'
$mcd complete $executionId

# Get last successful execution
echo 'Asserting last successful execution ID for execution #1'
lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
if [ $lastSuccessfulExecutionId != $executionId ]
then
    exit 1
fi

# Begin new execution
echo 'Beginning new execution #2'
executionId=$($mcd init)

# Modify load_model_1
echo 'Modifying load_model_1'
echo '' > "$loadModels/load_model_1.json"

# Compare load models
echo 'Comparing load models from execution #1'
changedModels=$($mcd compare $executionId load $loadModels *.json)
if [ $changedModels != 'load_model_1' ]
then
    exit 1
fi

# Complete execution
echo 'Completing execution #2'
$mcd complete $executionId

# Get last successful execution
echo 'Asserting last successful execution ID for execution #2'
lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
if [ $lastSuccessfulExecutionId != $executionId ]
then
    exit 1
fi

# debug
rm -rf $loadModels