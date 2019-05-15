from dpo.commands.BaseCommand import BaseCommand
from dpo import Shared


class CompleteStepCommand(BaseCommand):
    def __init__(self, db_connection_string, step_id, rows_processed, logger=None):
        super().__init__(db_connection_string, logger)
        self._step_id = step_id
        self._rows_processed = rows_processed
        self.logger.debug(f'step_id={self._step_id};'
                          f'rows_processed={self._rows_processed}')

    def execute(self):
        execution_step = self.repository.complete_execution_step(self._step_id, self._rows_processed)
        self.logger.debug('Completed Execution Step: ' + str(execution_step))

        total_execution_seconds = execution_step.execution_time_ms // 1000
        execution_hours = total_execution_seconds // 3600
        execution_minutes = (total_execution_seconds // 60) % 60
        execution_seconds = total_execution_seconds % 60
        execution_step_models = self.repository.get_execution_step_models(self._step_id)
        self.logger.info(f'Completed Execution Step: {execution_step.step_name}; '
                         f'Started On: {execution_step.started_on.isoformat()}; '
                         f'Completed On: {execution_step.completed_on.isoformat()}; '
                         f'Execution Time: {execution_hours}h {execution_minutes}m {execution_seconds}s; '
                         f'Models Processed: {Shared.safe_format_number(len(execution_step_models))}; '
                         f'Rows Processed: {Shared.safe_format_number(execution_step.rows_processed, "N/A")}.')
