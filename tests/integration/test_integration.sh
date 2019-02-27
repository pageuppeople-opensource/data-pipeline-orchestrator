# Exit on failure
set -e

# Bootstrap
## Aliases
loadModels='./tests/integration/models/load'
mcd='pipenv run python mcd.py postgresql+psycopg2://postgres:travisci@localhost:5432/postgres'

## Create stub load models
mkdir $loadModels
echo 'loadmodel1' > "$loadModels/load_model_1.json"

# Begin new execution
executionId=$($mcd init)

# Compare load models
$mcd compare $executionId load $loadModels **/*.json

# Complete execution
$mcd complete $executionId

# Get last successful execution
lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
if [ $lastSuccessfulExecutionId != $executionId ]
then
    exit 1
fi