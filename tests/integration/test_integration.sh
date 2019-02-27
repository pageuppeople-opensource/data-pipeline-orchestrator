# Exit on failure
set -e

# Command alias for MCD
mcd='pipenv run python mcd.py postgresql+psycopg2://postgres:travisci@localhost:5432/postgres'

# Begin new execution
executionId=$($mcd init)

# Complete execution
$mcd complete $executionId

# Get last successful execution
lastSuccessfulExecutionId=$($mcd get-last-successful-execution)
if [ $lastSuccessfulExecutionId != $executionId ]
then
    exit 1
fi