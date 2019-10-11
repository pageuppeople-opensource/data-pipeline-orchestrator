from dpo.commands.BaseCommand import BaseCommand


class InitialiseExecutionCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id=None, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        data_pipeline_execution = self.repository.initialise_execution(execution_id=self._execution_id)
        self.logger.debug('Initialised new data_pipeline_execution = ' + str(data_pipeline_execution))
        self.output(data_pipeline_execution.execution_id)

    def output(self, execution_id):
        print(str(execution_id))
