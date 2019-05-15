from dpo.commands.BaseCommand import BaseCommand


class CompleteExecutionCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        execution = self.repository.complete_execution(self._execution_id)
        self.logger.debug('Completed Execution: ' + str(execution))

        total_execution_seconds = execution.execution_time_ms // 1000
        execution_hours = total_execution_seconds // 3600
        execution_minutes = (total_execution_seconds // 60) % 60
        execution_seconds = total_execution_seconds % 60
        self.logger.info(f'Completed Execution ID: {execution.execution_id}; '
                         f'Started On: {execution.started_on.isoformat()}; '
                         f'Completed On: {execution.completed_on.isoformat()}; '
                         f'Execution Time: {execution_hours}h {execution_minutes}m {execution_seconds}s.')
