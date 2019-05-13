from dpo.commands.BaseCommand import BaseCommand


class CompleteExecutionCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        execution = self.repository.complete_execution(self._execution_id)
        self.logger.debug('Completed Execution: ' + str(execution))
