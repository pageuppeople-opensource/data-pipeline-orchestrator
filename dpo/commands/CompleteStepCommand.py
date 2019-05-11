from dpo.commands.BaseCommand import BaseCommand


class CompleteStepCommand(BaseCommand):
    def __init__(self, db_connection_string, step_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._step_id = step_id

    def execute(self):
        execution_step = self.repository.complete_execution_step(self._step_id)
        self.logger.debug('Completed Execution Step: ' + str(execution_step))
